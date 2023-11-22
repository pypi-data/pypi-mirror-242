"""
Angular Frequency quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'rad/s':
    Unit(symbols=[
        'rad/s', 'radian/s', 'radians/s', 'rad/sec', 'radian/sec',
        'radians/sec'
    ],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'rpm':
    Unit(symbols=['rpm', 'RPM', 'rotation/min', 'cycle/min'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.10471975512))]),
    'cps':
    Unit(symbols=[
        'cps', 'CPS', 'cycle/s', 'cycle/sec', 'rotation/s', 'rotation/sec'
    ],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(6.28318530725))]),
    'deg/s':
    Unit(symbols=['deg/s', 'degree/s', 'degree/sec', 'deg/sec'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.01745329251))]),
}

AngularFrequency = Quantity('Angular Frequency', _units, [])

