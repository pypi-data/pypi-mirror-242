"""
Unit definitions and lookup functions.
"""

from functools import lru_cache
from typing import List, Optional

from convunits.models import Quantity
from convunits.unit_definitions import DEFINITIONS


@lru_cache(maxsize=1024)
def find_quantity_by(unit_key: str) -> Optional[Quantity]:
    """Retrieve a quantity object given a unit symbol key.

    Args:
        unit_key (str): unit key string.

    Returns:
        Optional[Quantity]: the related `Quantity` object or `None`.
    """
    for quantity in DEFINITIONS:
        if quantity.units.get(unit_key):
            return quantity

    return None


@lru_cache(maxsize=1024)
def find_unit_standard(unit_symbol: str) -> Optional[str]:
    """Retrieve the canonical unit symbol for a unit.

    Args:
        unit_symbol (str): unit symbol string.

    Returns:
        Optional[str]: the canonical unit symbol or `None`.
    """
    for defn in DEFINITIONS:
        for unit_key, unit in defn.units.items():
            if unit_symbol in unit.symbols:
                return unit_key

    return None


@lru_cache(maxsize=1024)
def find_units_by_quantity(quantity_name: str) -> List[str]:
    """Retrieve all (key) units given a quantity.

    For example, given `Velocity`, expect to retrieve a list of units
    `['m/s', 'km/h', 'm/h', 'knot', 'ft/s', 'ft/min', 'ft/h']`.

    Args:
        quantity_name (str): name of the quantity (case-sensitive).

    Returns:
        List[str]: the list of (key) units related to the quantity.
    """
    for quantity in DEFINITIONS:
        if quantity.name == quantity_name:
            return list(quantity.units)

    return []


@lru_cache(maxsize=1024)
def find_quantity_by_unit_symbol(unit_symbol: str) -> Optional[Quantity]:
    """Retrieve a quantity object given unit symbol.

    For example, given `'km/h'`, expect to retrieve the `Velocity` unit.

    Args:
        unit_symbol (str): unit symbol.

    Returns:
        Optional[Quantity]: the related `Quantity` object or `None`.
    """
    for quantity in DEFINITIONS:
        for _, unit in quantity.units.items():
            if unit_symbol in unit.symbols:
                return quantity

    return None
