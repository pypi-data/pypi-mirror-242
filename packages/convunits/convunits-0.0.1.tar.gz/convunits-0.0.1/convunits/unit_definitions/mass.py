"""
Mass quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'ug':
    Unit(symbols=['ug'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(9.999999999999999e-10))]),
    'mg':
    Unit(symbols=['mg'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-06))]),
    'g':
    Unit(symbols=['g'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.001))]),
    'kg':
    Unit(symbols=['kg'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    't':
    Unit(symbols=['t', 'mt', 'metric ton'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
    'oz':
    Unit(symbols=['oz'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.0283495))]),
    'lb':
    Unit(symbols=['lb'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.453592))]),
    'us-t':
    Unit(symbols=['us-t', 'short ton', 'US ton', 'american ton'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(907.184))]),
    'uk-t':
    Unit(symbols=['uk-t', 'long ton', 'UK ton', 'english ton', 'british ton'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1016.05))]),
}

Mass = Quantity('Mass', _units, ['Weight'])

