"""
Voltage quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'V':
    Unit(symbols=['V'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'mV':
    Unit(symbols=['mV'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.001))]),
    'kV':
    Unit(symbols=['kV'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
}

Voltage = Quantity('Voltage', _units, [])

