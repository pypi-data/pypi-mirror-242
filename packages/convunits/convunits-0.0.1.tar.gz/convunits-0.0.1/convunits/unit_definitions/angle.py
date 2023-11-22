"""
Angle quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'rad':
    Unit(symbols=['rad', 'radian', 'RAD'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(57.29577951308232))]),
    'deg':
    Unit(symbols=['deg', 'degrees', 'degree', 'DEG', 'dega'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'grad':
    Unit(symbols=['grad'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.9))]),
    'arcmin':
    Unit(symbols=['arcmin'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.016666666666666666))]),
    'arcsec':
    Unit(symbols=['arcsec'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.0002777777777777778))]),
}

Angle = Quantity('Angle', _units, [])

