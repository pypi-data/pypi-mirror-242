"""
Conversion functionality.

NOTE: The `Convert` class does not follow the original structure of the TS code
for some reasons:
    - the TS code has a `.from()` method which we cannot implement as it
    clashes with a keyword,
    - a trade-off is more ideal to harmonize the new library and the legacy
    implementations of the `Family` class (particularly, in the drilling DS
    code),
    - this has fewer working parts.
"""

from typing import Union

import numpy as np
import pandas as pd

from convunits.definitions import find_quantity_by, find_unit_standard
from convunits.expression import Expression, Num
from convunits.errors import UnitNotFoundError, ConversionNotSupportedError


class Convert:
    """Converter class.

    This class converts a value from one unit to another.

    Attributes:
        value: the original value pre-conversion.
        result: the result of the conversion.
        quantity: the quantity of the units.
        from_unit: the unit to convert from.
        result: the unit to convert into.
    """
    def __init__(self, value: Union[int, float, list, np.ndarray, pd.Series], from_unit: str) -> None:
        """Conversion constructor.

        Args:
            value (Numberlike): Numeric value or numeric strings.
            from_unit (str): The units to convert from.

        Raises:
            UnitNotFoundError: If a unit does not exist in the registry.
        """
        self.value = Num(value)
        self.result = Num(value)
        self.quantity = None
        self.from_unit = None
        self.to_unit = None

        unit_key = find_unit_standard(from_unit)
        if not unit_key:
            raise UnitNotFoundError(f'Unit {from_unit} not found')

        quantity = find_quantity_by(unit_key)
        self.quantity = quantity
        self.from_unit = quantity.units[unit_key]
        for operation in self.from_unit.transformations:
            self.result = operation.apply(self.result)

    def to(self, unit_symbol: str) -> Expression:
        """Perform conversion into another unit.

        Args:
            unit_symbol (str): The unit to convert into.

        Raises:
            UnitNotFoundError: If a unit does not exist in the registry.
            ConversionNotSupportedError: If the target unit is not of the same quantity.

        Returns:
            Expression: The resulting conversion.
        """
        unit_key = find_unit_standard(unit_symbol)
        if not unit_key:
            raise UnitNotFoundError(f'Unit {unit_symbol} not found')

        quantity = find_quantity_by(unit_key)
        if quantity.name != self.quantity.name:  # HACK: Names assumed to be unique.
            raise ConversionNotSupportedError(f'Quantities {self.quantity.name} and {quantity.name} are not the same.')

        self.to_unit = quantity.units[unit_key]
        for operation in reversed(self.to_unit.transformations):
            self.result = operation.unapply(self.result)
        return self.result
