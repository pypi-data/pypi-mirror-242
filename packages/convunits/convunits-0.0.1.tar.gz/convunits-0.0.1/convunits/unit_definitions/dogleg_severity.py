"""
Dogleg Severity quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'deg/m':
    Unit(symbols=['deg/m', 'dega/m'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'deg/ft':
    Unit(symbols=['deg/ft', 'dega/ft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(3.28084))]),
    'deg/100ft':
    Unit(symbols=['deg/100ft', 'dega/100ft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(328.084))]),
}

DoglegSeverity = Quantity('Dogleg Severity', _units, [])

