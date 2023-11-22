"""
Each quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'ea':
    Unit(symbols=['ea'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'dz':
    Unit(symbols=['dz'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(12))]),
}

Each = Quantity('Each', _units, [])

