"""Models module.

This module contains utility classes to define operations on units and the
overarching unit class.
"""

from abc import ABC, abstractmethod
from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Optional

from convunits.expression import Expression, Num, Add, Div, Mul, Sub


class UnitSystem(Enum):
    IMPERIAL = 'imperial'
    METRIC = 'metric'


class IOperation(ABC):
    """Base invertible operation.

    This is an abstract base class that other operations should inherit. It has
    two methods to be implemented: apply and unapply which are, respectively,
    their forward operation and inverse operation. This class should *not* be
    instantiated in code.
    """
    @abstractmethod
    def apply(self, value: Expression) -> Expression:
        pass

    @abstractmethod
    def unapply(self, value: Expression) -> Expression:
        pass


@dataclass
class Unit:
    """Unit container class

    This class will be used by units which are contained within the quantity
    definitions.

    Args:
        transformations (List[IOperation]): the transformation required to
            convert from the base unit to this unit.
        symbols (Set[str]): the set of string representations of this unit
        system (UnitSystem): the system to which the unit belongs.
        default (Optional[bool]): true if this unit is the default (i.e. from
            which all other units are transformed).
        quantity_name (Optional[str]): name of the quantity to which this unit
            belongs.
        note (Optional[str]): Extra notes regarding the unit.
    """
    transformations: List[IOperation]
    symbols: List[str]
    system: UnitSystem
    default: Optional[bool] = None
    quantity_name: Optional[str] = None
    note: Optional[str] = None


@dataclass
class Quantity:
    """Quantity container class.

    This class will be used by quantities which are a single file in the
    definitions and acts like a unit family.

    Args:
        name (str): unit name.
        units (Dict[str, Unit]): mapping between representative unit string to
            the unit object.
        subquantities (List[str]): list of other quantity names that employ
            this unit.
    """
    name: str
    units: Dict[str, Unit]
    subquantities: List[str]

    def find_default_unit(self) -> Optional[str]:
        unit_symbols = next(v.symbols for v in self.units.values() if v.default)
        return next(iter(unit_symbols))


class FactorOperation(IOperation):
    """Reversible factor operation.

    Attributes:
        op_value (Num): the value on which the is applied.
    """
    def __init__(self, factor_value: Num) -> None:
        self.op_value = factor_value

    def apply(self, value: Expression) -> Expression:
        """Multiply the input (left) operand by the (instance) operand.

        Args:
            value (Expression): left operand expression.
        """
        return Mul(value, self.op_value)

    def unapply(self, value: Expression) -> Expression:
        """Divide the input (left) operand by the (instance) operand.

        Args:
            value (Expression): left operand expression.
        """
        return Div(value, self.op_value)


class ShiftOperation(IOperation):
    """Reversible shift operation.

    Attributes:
        op_value (Num): the value on which the operation is to be left-applied.
    """
    def __init__(self, shift_value: Num) -> None:
        self.op_value = shift_value

    def apply(self, value: Expression) -> Expression:
        """Add the input (left) operand by the (instance) operand.

        Args:
            value (Expression): left operand expression.
        """
        return Add(value, self.op_value)

    def unapply(self, value: Expression) -> Expression:
        """Subtract the input (left) operand by the (instance) operand.

        Args:
            value (Expression): left operand expression.
        """
        return Sub(value, self.op_value)
