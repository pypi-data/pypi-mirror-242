"""
Weight quantity module.
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
    'mt':
    Unit(symbols=['mt'],
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
    't':
    Unit(symbols=['t'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(907.184))]),
}

Weight = Quantity('Weight', _units, [])

