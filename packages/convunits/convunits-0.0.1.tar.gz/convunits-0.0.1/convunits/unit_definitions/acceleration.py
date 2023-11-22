"""
Acceleration quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'g-force':
    Unit(symbols=['g-force'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(9.80665))]),
    'm/s2':
    Unit(symbols=['m/s2'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'ft/s2':
    Unit(symbols=['ft/s2'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.3047999902464003))]),
}

Acceleration = Quantity('Acceleration', _units, [])

