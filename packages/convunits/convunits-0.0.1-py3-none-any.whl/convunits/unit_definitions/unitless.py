"""
Unitless quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'unitless':
    Unit(symbols=[
        'unitless', 'dimensionless', '', ' ', 'none', 'None', 'NONE', 'NoNe',
        '#'
    ],
         system=UnitSystem.METRIC,
         default=True,
         transformations=[FactorOperation(Num(1))]),
}

Unitless = Quantity(
    'Unitless', _units,
    ['Perforation Index', 'Poisson Ratio', 'Normalized', 'Saturation'])

