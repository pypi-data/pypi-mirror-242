"""
Error definitions.
"""

class UnitNotFoundError(Exception):
    """Raised when a unit is not found.

    Checks against all units across all quantities.
    """
    pass


class ConversionNotSupportedError(Exception):
    """Raised when a conversion is attempted across two quantities."""
    pass


class NotANumberError(Exception):
    """Raised when a user input is not a valid `Numberlike`."""
    pass
