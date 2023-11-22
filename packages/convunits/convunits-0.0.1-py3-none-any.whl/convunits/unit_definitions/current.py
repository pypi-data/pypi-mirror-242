"""
Current quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'A':
    Unit(symbols=['A'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'mA':
    Unit(symbols=['mA'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.001))]),
    'kA':
    Unit(symbols=['kA'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
    'MA':
    Unit(
        symbols=['MA'],
        system=UnitSystem.METRIC,
        transformations=[FactorOperation(Num(1000000))],
        note=
        ('symbol occurred in a DLIS file in the context of BHI where we have '
         'resistivity related data channels. Mega-ampère (MA) is the most plausible '
         'unit it represents.')),
}

Current = Quantity('Current', _units, [])

