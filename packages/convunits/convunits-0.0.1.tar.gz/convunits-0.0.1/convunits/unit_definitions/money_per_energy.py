"""
Money Per Energy quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'USD/J':
    Unit(symbols=['USD/J', '$/J'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'USD/kWh':
    Unit(symbols=['USD/kWh', '$/kWh'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(2.77777778e-07))]),
    'USD/BOE':
    Unit(symbols=['USD/BOE', '$/BOE'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1.6345576e-10))]),
}

MoneyPerEnergy = Quantity('Money Per Energy', _units, [
    'Production Cost', 'Lifting Cost', 'Unit Technical Cost',
    'Production Revenue'
])

