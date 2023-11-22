"""
Inverse Resistivity quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    '1/(ohm.m)':
    Unit(symbols=['1/(ohm.m)'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    '1/(ohm.cm)':
    Unit(symbols=['1/(ohm.cm)'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(100))]),
    '1/(ohm.mm)':
    Unit(symbols=['1/(ohm.mm)'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
    '1/(ohm.um)':
    Unit(symbols=['1/(ohm.um)'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000))]),
    '1/(ohm.nm)':
    Unit(symbols=['1/(ohm.nm)'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000000))]),
    '1/(ohm.pm)':
    Unit(symbols=['1/(ohm.pm)'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000000000))]),
    '1/(ohm.fm)':
    Unit(symbols=['1/(ohm.fm)'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000000000000))]),
    '1/(ohm.ft)':
    Unit(symbols=['1/(ohm.ft)'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(3.280839895))]),
}

InverseResistivity = Quantity('Inverse Resistivity', _units, [])

