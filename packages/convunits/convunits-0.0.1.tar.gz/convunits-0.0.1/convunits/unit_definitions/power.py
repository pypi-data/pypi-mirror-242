"""
Power quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'W':
    Unit(symbols=['W'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'mW':
    Unit(symbols=['mW'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.001))]),
    'kW':
    Unit(symbols=['kW'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
    'MW':
    Unit(symbols=['MW'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000))]),
    'GW':
    Unit(symbols=['GW'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000000))]),
    'HP':
    Unit(symbols=['HP'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(745.699872))]),
    'BOE/d':
    Unit(symbols=['BOE/d', 'BOEPD', 'Barrel Oil Equivalent Per Day'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(70810.1851852))]),
    'MBOE/d':
    Unit(symbols=[
        'MBOE/d', 'M BOE/d', 'MBOEPD', 'M BOEPD',
        'Thousand Barrel Oil Equivalent Per Day'
    ],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(70810185.1852))]),
    'MMBOE/d':
    Unit(symbols=[
        'MMBOE/d', 'MM BOE/d', 'MMBOEPD', 'MM BOEPD',
        'Million Barrel Oil Equivalent Per Day'
    ],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(70810185185.2))]),
    'BTU/DAY':
    Unit(symbols=['BTU/DAY'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.01221129459))]),
}

Power = Quantity('Power', _units, [])

