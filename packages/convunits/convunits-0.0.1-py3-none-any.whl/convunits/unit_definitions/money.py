"""
Money quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'USD':
    Unit(symbols=['USD', 'Usd', 'usd', '$', 'dollar', 'US dollar'],
         system=UnitSystem.METRIC,
         default=True,
         transformations=[]),
    'Thousand USD':
    Unit(symbols=['Thousand USD', 'M USD'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
    'Million USD':
    Unit(symbols=['Million USD', 'MM USD'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000))]),
}

Money = Quantity('Money', _units, ['Cost', 'Capital', 'Cash', 'Finance'])

