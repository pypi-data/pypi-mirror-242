"""
Velocity quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'm/s':
    Unit(symbols=['m/s', 'meter/second', 'meter/sec', 'm/sec'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'km/h':
    Unit(symbols=['km/h', 'km/hour', 'kph'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.277778))]),
    'm/h':
    Unit(symbols=['m/h', 'MPH', 'mph', 'miles/hour'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.4470410016946879))]),
    'knot':
    Unit(symbols=['knot'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.514444471537777))]),
    'ft/s':
    Unit(symbols=['ft/s', 'feet/second', 'feet/sec', 'ft/sec'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.3047999902464003))]),
    'ft/min':
    Unit(symbols=['ft/min'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.00508000999743968))]),
    'ft/h':
    Unit(symbols=['ft/h'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(8.466666158666683e-05))]),
}

Velocity = Quantity('Velocity', _units, [])

