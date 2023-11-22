"""
Productivity Index quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'm3/s/Pa':
    Unit(symbols=['m3/s/Pa'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'STB/D/psia':
    Unit(symbols=[
        'STB/D/psia', 'STB/D/PSIA', 'STB/D/P', 'stbpd/psi', 'STBPD/PSI'
    ],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(2.66888e-10))]),
}

ProductivityIndex = Quantity('Productivity Index', _units, [])

