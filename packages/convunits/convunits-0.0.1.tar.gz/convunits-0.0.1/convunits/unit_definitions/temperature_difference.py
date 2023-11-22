"""
Temperature Difference quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'deltaC':
    Unit(symbols=['deltaC', 'delta_degC', 'deltaCelsius', 'delta°C'],
         system=UnitSystem.METRIC,
         transformations=[]),
    'deltaK':
    Unit(symbols=['deltaK', 'delta_degK', 'deltaKelvin', 'delta°K'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'deltaF':
    Unit(symbols=['deltaF', 'delta_degF', 'deltaFahrenheit', 'delta°F'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.55555555555))]),
    'deltaR':
    Unit(symbols=['deltaR', 'delta_degR', 'deltaRankine', 'delta°R'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.55555555555))]),
}

TemperatureDifference = Quantity('Temperature Difference', _units, [])

