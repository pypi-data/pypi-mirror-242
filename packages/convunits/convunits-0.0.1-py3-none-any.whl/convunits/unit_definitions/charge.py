"""
Charge quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'c':
    Unit(symbols=['c'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'mC':
    Unit(symbols=['mC'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.001))]),
    'μC':
    Unit(symbols=['μC'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-06))]),
    'nC':
    Unit(symbols=['nC'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-09))]),
    'pC':
    Unit(symbols=['pC'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-12))]),
}

Charge = Quantity('Charge', _units, [])

