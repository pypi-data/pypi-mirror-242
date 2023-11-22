"""
Energy quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'Wh':
    Unit(symbols=['Wh'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(3600))]),
    'mWh':
    Unit(symbols=['mWh'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(3.6))]),
    'kWh':
    Unit(symbols=['kWh'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(3600000))]),
    'MWh':
    Unit(symbols=['MWh'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(3600000000))]),
    'GWh':
    Unit(symbols=['GWh'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(3600000000000))]),
    'J':
    Unit(symbols=['J'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'kJ':
    Unit(symbols=['kJ'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
    'ft.lbf':
    Unit(symbols=['ft.lbf'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1.3558179))]),
    'kft.lbf':
    Unit(symbols=['kft.lbf'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1355.8179))]),
    'BTU':
    Unit(symbols=['BTU', 'British Thermal Unit'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1055.0558526))]),
    'BOE':
    Unit(symbols=['BOE', 'Barrel Oil Equivalent'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(6117863200.0))]),
    'MBOE':
    Unit(symbols=['MBOE', 'M BOE', 'Thousand Barrel Oil Equivalent'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(6117863200000.0))]),
    'MMBOE':
    Unit(symbols=['MMBOE', 'MM BOE', 'Million Barrel Oil Equivalent'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(6117863200000000.0))]),
}

Energy = Quantity('Energy', _units, [])

