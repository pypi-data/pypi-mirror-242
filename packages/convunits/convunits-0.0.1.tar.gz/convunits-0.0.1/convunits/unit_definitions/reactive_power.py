"""
Reactive Power quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'VAR':
    Unit(symbols=['VAR'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'mVAR':
    Unit(symbols=['mVAR'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.001))]),
    'kVAR':
    Unit(symbols=['kVAR'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
    'MVAR':
    Unit(symbols=['MVAR'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000))]),
    'GVAR':
    Unit(symbols=['GVAR'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000000))]),
}

ReactivePower = Quantity('Reactive Power', _units, [])

