"""
Ratio quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'fraction':
    Unit(symbols=['fraction', 'Fraction', 'FRACTION'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'pct':
    Unit(symbols=['pct', '%', 'percent'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.01))]),
    'ppm':
    Unit(symbols=['ppm', 'PPM'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-06))]),
    'ppb':
    Unit(symbols=['ppb', 'PPB'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-09))]),
    'ppt':
    Unit(symbols=['ppt', 'PPT'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-12))]),
    'ppq':
    Unit(symbols=['ppq', 'PPQ'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-15))]),
}

Ratio = Quantity('Ratio', _units, [])

