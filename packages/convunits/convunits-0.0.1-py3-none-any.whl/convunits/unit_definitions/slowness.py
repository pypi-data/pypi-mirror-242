"""
Slowness quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    's/m':
    Unit(symbols=['s/m'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'min/m':
    Unit(symbols=['min/m'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(60))]),
    'min/km':
    Unit(symbols=['min/km'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.06))]),
    'ms/m':
    Unit(symbols=['ms/m'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.001))]),
    'us/m':
    Unit(symbols=['us/m'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-06))]),
    'ns/m':
    Unit(symbols=['ns/m'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-09))]),
    's/ft':
    Unit(symbols=['s/ft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(3.280839895013123))]),
    'min/mi':
    Unit(symbols=['min/mi'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.03728215223097112))]),
    'min/ft':
    Unit(symbols=['min/ft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(196.85039370078738))]),
    'ms/ft':
    Unit(symbols=['ms/ft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.003280839895013123))]),
    'us/ft':
    Unit(symbols=['us/ft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(3.280839895013123e-06))]),
    'ns/ft':
    Unit(symbols=['ns/ft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(3.2808398950131233e-09))]),
}

Slowness = Quantity('Slowness', _units, [])

