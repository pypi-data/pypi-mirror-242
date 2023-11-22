"""
Resistivity quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'ohm.m':
    Unit(symbols=[
        'ohm.m', 'Ohm.m', 'OHMM', 'ohmm', 'Ohm.meter', 'ohm.meter', 'Ohm.Meter'
    ],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'ohm.cm':
    Unit(symbols=['ohm.cm'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.01))]),
    'ohm.mm':
    Unit(symbols=['ohm.mm'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.001))]),
    'ohm.um':
    Unit(symbols=['ohm.um'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-06))]),
    'ohm.nm':
    Unit(symbols=['ohm.nm'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-09))]),
    'ohm.ft':
    Unit(symbols=['ohm.ft', 'ohm.feet', 'ohmft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.3048000000012192))]),
}

Resistivity = Quantity('Resistivity', _units, [])

