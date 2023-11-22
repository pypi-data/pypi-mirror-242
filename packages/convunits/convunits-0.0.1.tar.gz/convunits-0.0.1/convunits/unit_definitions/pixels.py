"""
Pixels quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'pixel':
    Unit(symbols=['pixel', 'Pixel', 'px', 'Px', 'Pixels', 'pixels'],
         system=UnitSystem.METRIC,
         default=True,
         transformations=[FactorOperation(Num(1))]),
}

Pixels = Quantity('Pixels', _units, [])

