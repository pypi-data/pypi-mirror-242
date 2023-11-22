"""
Temperature quantity module.
"""

from convunits.models import FactorOperation, Quantity, ShiftOperation, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'C':
    Unit(symbols=['C', 'degC', 'Celsius', '°C'],
         system=UnitSystem.METRIC,
         transformations=[ShiftOperation(Num(273.15))]),
    'K':
    Unit(symbols=['K', 'degK', 'Kelvin', '°K'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'F':
    Unit(symbols=['F', 'degF', 'Fahrenheit', '°F'],
         system=UnitSystem.IMPERIAL,
         transformations=[
             ShiftOperation(Num(459.67)),
             FactorOperation(Num(0.55555555555))
         ]),
    'R':
    Unit(symbols=['R', 'degR', 'Rankine', '°R'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.55555555555))]),
}

Temperature = Quantity('Temperature', _units, [])

