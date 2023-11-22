"""
Length quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'nm':
    Unit(symbols=['nm', 'nanometer', 'Nanometer'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-09))]),
    'um':
    Unit(symbols=['um', 'micrometer', 'Micrometer'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-06))]),
    'mm':
    Unit(symbols=['mm', 'milimeter', 'Milimeter'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.001))]),
    'cm':
    Unit(symbols=['cm', 'centimeter', 'Centimeter'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.01))]),
    'm':
    Unit(
        symbols=['m', 'meter', 'Meter', 'meters', 'Meters', 'METERS', 'METER'],
        default=True,
        system=UnitSystem.METRIC,
        transformations=[]),
    'km':
    Unit(symbols=['km', 'kilometer', 'Kilometer', 'Kilometers', 'KM', 'Km'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
    'in':
    Unit(symbols=['in', 'inch', 'Inch', 'IN', 'inches', 'Inches'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.025399999187200026))]),
    '0.1in':
    Unit(symbols=['0.1in', '0.1inch', '0.1Inch', '0.1 in', '_01in', '01in'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.0025399999187200027))]),
    '64thsin':
    Unit(symbols=[
        '64thsin', '64ths in', '64ths_in', '64thsInch', '64thsIn', '1/64 in',
        '1/64_in', '1/64in', '64ths inch', '64ths inches', '1/64ths inch',
        '1/64ths inches'
    ],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.0003968749873))]),
    'yd':
    Unit(symbols=['yd', 'yard', 'Yard'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.914399970739201))]),
    'ft-us':
    Unit(symbols=['ft-us', 'feetUS', 'feet-US', 'foot-us', 'USfeet'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.3048005998463808))]),
    'ft':
    Unit(symbols=['ft', 'FT', 'Ft', 'feet', 'Feet', 'foot', 'FEET'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.3047999902464003))]),
    'fathom':
    Unit(symbols=['fathom'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1.828799941478402))]),
    'mi':
    Unit(symbols=['mi', 'mile', 'miles', 'Miles'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1609.3439485009937))]),
    'nMi':
    Unit(symbols=['nMi', 'nmi', 'nmile', 'nauticalmiles', 'nauticalMiles'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1852.0013167359577))]),
}

Length = Quantity('Length', _units, [])

