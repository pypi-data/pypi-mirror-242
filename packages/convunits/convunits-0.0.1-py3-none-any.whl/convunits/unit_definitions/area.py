"""
Area quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'nm2':
    Unit(symbols=['nm2', 'nm^2'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-18))]),
    'um2':
    Unit(symbols=['um2', 'um^2'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-12))]),
    'mm2':
    Unit(symbols=['mm2', 'mm^2'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-06))]),
    'cm2':
    Unit(symbols=['cm2', 'cm^2'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.0001))]),
    'm2':
    Unit(symbols=['m2', 'm^2'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'ha':
    Unit(symbols=['ha'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(10000))]),
    'km2':
    Unit(symbols=['km2', 'km^2'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000))]),
    'D':
    Unit(symbols=['D', 'Darcy', 'darcy'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(9.869232999999999e-13))]),
    'mD':
    Unit(symbols=['mD', 'md', 'Millidarcy', 'millidarcy'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(9.869232999999999e-16))]),
    'uD':
    Unit(symbols=['uD', 'ud', 'Microdarcy', 'microdarcy'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(9.869233e-19))]),
    'nD':
    Unit(symbols=['nD', 'nd', 'Nanodarcy', 'nanodarcy'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(9.869233e-22))]),
    'in2':
    Unit(symbols=['in2', 'in^2'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.0006451606243503233))]),
    'yd2':
    Unit(symbols=['yd2'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.836128169158019))]),
    'ft2':
    Unit(symbols=['ft2', 'ft^2'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.09290312990644656))]),
    'ac':
    Unit(symbols=['ac'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(4046.860338724812))]),
    'mi2':
    Unit(symbols=['mi2'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(2589990.6167838797))]),
}

Area = Quantity('Area', _units, ['Permeability'])

