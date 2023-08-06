"""Implements the PRECIS profile classes."""

import re

from precis_i18n.baseclass import FreeFormClass, IdentifierClass, raise_error
from precis_i18n.bidi import bidi_rule, has_rtl

# pylint: disable=no-self-use


class Profile:
    """Base class for a PRECIS profile.

    Subclasses should override the `*_rule` methods.

    Args:
        base (BaseClass): Base string class.
        name (str): Name of profile.
        casemap (Optional[str]): Case mapping function: 'fold' or 'lower'.
    """
    def __init__(self, base, name, casemap=None):
        self._base = base
        self._name = name
        # casemap can be either None, 'fold', or 'lower'.
        if casemap is None:
            self._casemap = None
        elif casemap == 'fold':
            self._casemap = _casefold
        elif casemap == 'lower':
            self._casemap = _caselower
        else:
            raise ValueError('Unknown casemap value: %s' % casemap)

    @property
    def base(self):
        """Base string class."""
        return self._base

    @property
    def name(self):
        """Profile name."""
        return self._name

    def enforce(self, value):
        """Ensure that all characters in `value` are allowed by the profile.

        If `value` is bytes, it's first decoded as UTF-8 to a string.

        Args:
            value (Union[str, bytes]): String value to enforce.

        Returns:
            str: Enforced value.

        Raises:
            UnicodeEncodeError: Value is disallowed by the profile.
            ValueError: `value` not a string or bytes.
        """
        # If we get called with a byte string, decode it first.
        if isinstance(value, bytes):
            value = value.decode('utf-8')
        elif not isinstance(value, str):
            raise ValueError('not a string')
        temp = self.apply_five_rules(value)
        temp = self.idempotence_check(temp)
        # Make sure the resulting value is not empty.
        if not temp:
            raise_error(self.name, value, -1, 'empty')
        # Apply behavioral rules from the base string class last.
        return self.base.enforce(temp, self.name)

    def apply_five_rules(self, value):
        """Apply the five rules specified by RFC 8264 in order.

        Args:
            value (str): Value to enforce.

        Returns:
            str: Enforced value.
        """
        temp = self.width_mapping_rule(value)
        temp = self.additional_mapping_rule(temp)
        temp = self.case_mapping_rule(temp)
        temp = self.normalization_rule(temp)
        return self.directionality_rule(temp)

    def width_mapping_rule(self, value):
        """Apply width mapping rule.

        Args:
            value (str): Value to enforce.

        Returns:
            str: Enforced value.
        """
        return value

    def additional_mapping_rule(self, value):
        """Apply additional mapping rule.

        Args:
            value (str): Value to enforce.

        Returns:
            str: Enforced value.
        """
        return value

    def case_mapping_rule(self, value):
        """Apply case mapping rule.

        Args:
            value (str): Value to enforce.

        Returns:
            str: Enforced value.
        """
        if self._casemap:
            return self._casemap(value)
        return value

    def normalization_rule(self, value):
        """Apply normalization rule.

        Args:
            value (str): Value to enforce.

        Returns:
            str: Enforced value.
        """
        return self.base.ucd.normalize('NFC', value)

    def directionality_rule(self, value):
        """Apply directionality rule.

        Args:
            value (str): Value to enforce.

        Returns:
            str: Enforced value.
        """
        return value

    def idempotence_check(self, value):
        """Check that profile result is idempotent.

        Profiles that are not idempotent should override this method.

        Args:
            value (str): Value to enforce.

        Returns:
            str: Enforced value.
        """
        new_value = self.apply_five_rules(value)
        if new_value != value:
            raise_error(self.name, value, -1, 'not_idempotent')
        return value


class Username(Profile):
    """Concrete class for Username profile.

    Reference:
        Name:  UsernameCasePreserved | UsernameCaseMapped

        Base Class:  IdentifierClass.

        Applicability:  Usernames in security and application protocols.

        Replaces:  The SASLprep profile of stringprep.

        Width-Mapping Rule:  Map fullwidth and halfwidth characters to their
           decomposition mappings.

        Additional Mapping Rule:  None.

        Case-Mapping Rule:  None | Map uppercase and titlecase characters to
           lowercase.

        Normalization Rule:  NFC.

        Directionality Rule:  The "Bidi Rule" defined in RFC 5893 applies.

        Enforcement:  To be defined by security or application protocols that
           use this profile.

        Specification:  RFC 8265, Section 3.3.

    Args:
        ucd (UnicodeData): Unicode character database.
        name (str): Name of profile.
        casemap (Optional[str]): Case mapping function: 'fold' or 'lower'.
    """
    def __init__(self, ucd, name, casemap=None):
        super().__init__(IdentifierClass(ucd), name, casemap)

    def width_mapping_rule(self, value):
        # Override
        return self.base.ucd.width_map(value)

    def directionality_rule(self, value):
        # Override
        # Only apply the "bidi rule" if the string contains RTL characters.
        if has_rtl(value, self.base.ucd):
            if not bidi_rule(value, self.base.ucd):
                raise_error(self.name, value, -1, 'bidi_rule')
        return value


class OpaqueString(Profile):
    """Concrete class for OpaqueString profile.

    Reference:
        Name:  OpaqueString.

        Base Class:  FreeformClass.

        Applicability:  Passwords and other opaque strings in security and
           application protocols.

        Replaces:  The SASLprep profile of stringprep.

        Width-Mapping Rule:  None.

        Additional Mapping Rule:  Map non-ASCII space characters to ASCII
           space.

        Case-Mapping Rule:  None.

        Normalization Rule:  NFC.

        Directionality Rule:  None.

        Enforcement:  To be defined by security or application protocols that
           use this profile.

        Specification:  RFC 8265, Section 4.2.

    Args:
        ucd (UnicodeData): Unicode character database.
        name (str): Name of profile.
    """
    def __init__(self, ucd, name):
        super().__init__(FreeFormClass(ucd), name, casemap=None)

    def additional_mapping_rule(self, value):
        # Override
        return self.base.ucd.map_nonascii_space_to_ascii(value)


class Nickname(Profile):
    """Concrete class for Nickname profile.

    Reference:
        Name:  Nickname.

        Base Class:  FreeformClass.

        Applicability:  Nicknames in messaging and text conferencing
           technologies; petnames for devices, accounts, and people; and
           other uses of nicknames or petnames.

        Replaces:  None.

        Width Mapping Rule:  None (handled via NFKC).

        Additional Mapping Rule:  Map non-ASCII space characters to ASCII
           space, strip leading and trailing space characters, map interior
           sequences of multiple space characters to a single ASCII space.

        Case Mapping Rule:  Map uppercase and titlecase characters to
           lowercase using Unicode Default Case Folding.

        Normalization Rule:  NFKC.

        Directionality Rule:  None.

        Enforcement:  To be specified by applications.

        Specification:  RFC 8266

    Args:
        ucd (UnicodeData): Unicode character database.
        name (str): Name of profile.
        casemap (Optional[str]): Case mapping function: 'fold' or 'lower'.
    """
    def __init__(self, ucd, name, casemap=None):
        super().__init__(FreeFormClass(ucd), name, casemap)

    def additional_mapping_rule(self, value):
        # Override
        temp = self.base.ucd.map_nonascii_space_to_ascii(value)
        return re.sub(r'  +', ' ', temp.strip())

    def normalization_rule(self, value):
        # Override
        return self.base.ucd.normalize('NFKC', value)

    def idempotence_check(self, value):
        # Override
        # Nickname profile is not idempotent due to ordering of additional
        # and case mapping rules, so we apply them again.
        value = self.apply_five_rules(value)
        return super().idempotence_check(value)


def _casefold(s):
    return s.casefold()


def _caselower(s):
    return s.lower()
