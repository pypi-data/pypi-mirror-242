"""
Torque quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'Nm':
    Unit(symbols=['Nm'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'lbf.ft':
    Unit(symbols=['lbf.ft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1.355818))]),
    'klbf.ft':
    Unit(symbols=['klbf.ft', '1000lbf.ft', 'klb-ft', '1000lb-ft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1355.818))]),
}

Torque = Quantity('Torque', _units, [])

