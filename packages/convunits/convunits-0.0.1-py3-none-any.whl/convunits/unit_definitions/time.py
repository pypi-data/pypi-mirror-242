"""
Time quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'ns':
    Unit(symbols=['ns', 'nsec'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-09))]),
    'us':
    Unit(symbols=['us', 'usec'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-06))]),
    'ms':
    Unit(symbols=['ms', 'msec'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.001))]),
    's':
    Unit(symbols=['s', 'sec', 'second'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'min':
    Unit(symbols=['min', 'minute'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(60))]),
    'h':
    Unit(symbols=['h', 'hour', 'H'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(3600))]),
    'day':
    Unit(symbols=['day', 'Day', 'd', 'Days', 'days', 'DAYS'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(86400))]),
    'week':
    Unit(symbols=['week', 'Week', 'w'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(604800))]),
    'month':
    Unit(symbols=['month', 'Month', 'M'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(2628000))]),
    'year':
    Unit(symbols=[
        'year', 'years', 'Year', 'Years', 'yr', 'yrs', 'Yr', 'Yrs', 'Y', 'y'
    ],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(31536000))]),
}

Time = Quantity('Time', _units, [])

