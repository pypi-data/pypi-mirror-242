"""
Force quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'N':
    Unit(symbols=['N'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'kN':
    Unit(symbols=['kN'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
    'kgf':
    Unit(symbols=['kgf', 'Kg.f', 'kg.f', 'KGF', 'Kgf'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(9.80665))]),
    'lbf':
    Unit(symbols=['lbf'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(4.44822))]),
    'klbf':
    Unit(symbols=['klbf'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(4448.22))]),
}

Force = Quantity('Force', _units, [])

