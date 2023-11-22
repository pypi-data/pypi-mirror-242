"""
Density quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'kg/m3':
    Unit(symbols=['kg/m3', 'Kg/m3', 'KG/m3', 'KG/M3'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'kg/cm3':
    Unit(symbols=['kg/cm3', 'Kg/cm3', 'KG/cm3', 'KG/CM3'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000))]),
    'g/cm3':
    Unit(symbols=['g/cm3', 'gram/cm3', 'g/cc', 'G/cm3', 'G/CM3', 'G/C3'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
    'g/m3':
    Unit(symbols=['g/m3', 'G/m3', 'G/M3'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.001))]),
    'kg/l':
    Unit(symbols=['kg/l', 'Kg/l', 'KG/l', 'KG/L'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
    'g/l':
    Unit(symbols=['g/l', 'G/l', 'G/L'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000))]),
    'mg/l':
    Unit(symbols=['mg/l'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000000))]),
    't/m3':
    Unit(symbols=['t/m3'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
    'lb/cu-ft':
    Unit(symbols=['lb/cu-ft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(16.018463367839058))]),
    'lb/gal':
    Unit(symbols=['lb/gal', 'PPG', 'ppg'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(99.77644536795012))]),
    'lb/galUS':
    Unit(symbols=['lb/galUS'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(119.8265141265246))]),
    'lb/bbl':
    Unit(symbols=['lb/bbl'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(5032.709928654399))]),
    'oz/cu-in':
    Unit(symbols=['oz/cu-in'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1729.9940435882186))]),
    'lb/cu-yd':
    Unit(symbols=['lb/cu-yd'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.5932764210310761))]),
}

Density = Quantity('Density', _units, [])

