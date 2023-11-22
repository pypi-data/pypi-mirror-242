"""
Gamma Ray quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'gAPI':
    Unit(symbols=['gAPI', 'GAPI'],
         system=UnitSystem.METRIC,
         default=True,
         transformations=[FactorOperation(Num(1))]),
}

GammaRay = Quantity('Gamma Ray', _units, [])

