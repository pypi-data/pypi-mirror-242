"""
Mass Flow Rate quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'kg/s':
    Unit(symbols=['kg/s', 'Kg/s', 'KG/S', 'kg/sec'],
         system=UnitSystem.METRIC,
         default=True,
         transformations=[]),
    'kg/h':
    Unit(symbols=['kg/h', 'Kg/h', 'KG/H', 'kg/hour'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.0002777777777777778))]),
    'kg/d':
    Unit(symbols=['kg/d', 'Kg/d', 'KG/D', 'kg/day'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.006666666666666667))]),
    'kg/y':
    Unit(symbols=['kg/y', 'Kg/y', 'KG/Y', 'kg/year'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(2.433333333333333))]),
    't/y':
    Unit(symbols=['t/y', 'ton/y', 'ton/year', 't/year'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(2433.3333333333335))]),
    'kt/y':
    Unit(symbols=[
        'kt/y', 'kiloton/y', 'kiloton/year', 'ThousandTon/Year', "MT'000 p.a.",
        "M.T. '000 p.a.", 'MT000 p.a.', 'Thousand Metric Tonnes Per Annum'
    ],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(2433333.3333333335))]),
}

MassFlowRate = Quantity('Mass Flow Rate', _units, [])

