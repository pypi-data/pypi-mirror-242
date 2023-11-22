"""
Illuminance quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'lx':
    Unit(symbols=['lx'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'ft-cd':
    Unit(symbols=['ft-cd'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(10.76391))]),
}

Illuminance = Quantity('Illuminance', _units, [])

