"""
Reactive Energy quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'VARh':
    Unit(symbols=['VARh'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'mVARh':
    Unit(symbols=['mVARh'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.001))]),
    'kVARh':
    Unit(symbols=['kVARh'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
    'MVARh':
    Unit(symbols=['MVARh'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000))]),
    'GVARh':
    Unit(symbols=['GVARh'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000000))]),
}

ReactiveEnergy = Quantity('Reactive Energy', _units, [])

