"""
Apparent Power quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'VA':
    Unit(symbols=['VA'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'mVA':
    Unit(symbols=['mVA'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.001))]),
    'kVA':
    Unit(symbols=['kVA'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
    'MVA':
    Unit(symbols=['MVA'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000))]),
    'GVA':
    Unit(symbols=['GVA'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000000))]),
}

ApparentPower = Quantity('Apparent Power', _units, [])

