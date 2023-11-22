"""
Inverse Length quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    '1/nm':
    Unit(symbols=['1/nm'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000000))]),
    '1/um':
    Unit(symbols=['1/um'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000))]),
    '1/mm':
    Unit(symbols=['1/mm'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
    '1/cm':
    Unit(symbols=['1/cm'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(100))]),
    '1/m':
    Unit(symbols=['1/m'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    '1/km':
    Unit(symbols=['1/km'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.001))]),
    '1/in':
    Unit(symbols=['1/in'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(39.37008))]),
    '10/in':
    Unit(symbols=['10/in'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(393.7008))]),
    '1/yd':
    Unit(symbols=['1/yd'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1.0936133333333333))]),
    '1/ft-us':
    Unit(symbols=['1/ft-us'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(3.280833438333123))]),
    '1/ft':
    Unit(symbols=['1/ft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(3.28084))]),
    '1/mi':
    Unit(symbols=['1/mi'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.0006213712121212121))]),
    '1/nMi':
    Unit(symbols=['1/nMi'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.0005399564195572175))]),
    '1/fathom':
    Unit(symbols=['1/fathom'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.54680666666))]),
}

InverseLength = Quantity('Inverse Length', _units, [])

