"""
Frequency quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'mHz':
    Unit(symbols=['mHz'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.001))]),
    'Hz':
    Unit(symbols=['Hz', 'hz', 'Herz', 'herz', '1/s', 's-1', 's^-1'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'kHz':
    Unit(symbols=['kHz'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
    'MHz':
    Unit(symbols=['MHz'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000))]),
    'GHz':
    Unit(symbols=['GHz'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000000))]),
    'THz':
    Unit(symbols=['THz'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000000000))]),
}

Frequency = Quantity('Frequency', _units, [])

