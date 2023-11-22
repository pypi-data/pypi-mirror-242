"""
Conductivity quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'S/m':
    Unit(symbols=['S/m'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'mS/m':
    Unit(symbols=['mS/m'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.001))]),
    'uS/m':
    Unit(symbols=['uS/m'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-06))]),
    'nS/m':
    Unit(symbols=['nS/m'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-09))]),
    'S/ft':
    Unit(symbols=['S/ft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(3.28084))]),
    'mS/ft':
    Unit(symbols=['mS/ft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.00328084))]),
    'uS/ft':
    Unit(symbols=['uS/ft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(3.28084e-06))]),
    'nS/ft':
    Unit(symbols=['nS/ft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(3.28084e-09))]),
}

Conductivity = Quantity('Conductivity', _units, [])

