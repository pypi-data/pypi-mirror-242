"""
Volumetric Flow Rate quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'mm3/s':
    Unit(symbols=['mm3/s'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-09))]),
    'cm3/s':
    Unit(symbols=['cm3/s'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-06))]),
    'ml/s':
    Unit(symbols=['ml/s'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-06))]),
    'cl/s':
    Unit(symbols=['cl/s'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-05))]),
    'dl/s':
    Unit(symbols=['dl/s'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.0001))]),
    'l/s':
    Unit(symbols=['l/s'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.001))]),
    'l/min':
    Unit(symbols=['l/min', 'lpm', 'LPM'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1.6666666666666667e-05))]),
    'l/h':
    Unit(symbols=['l/h'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(2.7777777777777776e-07))]),
    'kl/s':
    Unit(symbols=['kl/s'], system=UnitSystem.METRIC, transformations=[]),
    'kl/min':
    Unit(symbols=['kl/min'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.016666666666666666))]),
    'kl/h':
    Unit(symbols=['kl/h'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.0002777777777777778))]),
    'm3/s':
    Unit(symbols=['m3/s'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'm3/min':
    Unit(symbols=['m3/min'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.016666666666666666))]),
    'm3/h':
    Unit(symbols=['m3/h'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.0002777777777777778))]),
    'km3/s':
    Unit(symbols=['km3/s'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000000))]),
    'tsp/s':
    Unit(symbols=['tsp/s'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(4.9289215940186454e-06))]),
    'Tbs/s':
    Unit(symbols=['Tbs/s'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1.4786764782055937e-05))]),
    'in3/s':
    Unit(symbols=['in3/s'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1.638698846677003e-05))]),
    'in3/min':
    Unit(symbols=['in3/min'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(2.7311647444616716e-07))]),
    'in3/h':
    Unit(symbols=['in3/h'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(4.551941240769452e-09))]),
    'fl-oz/s':
    Unit(symbols=['fl-oz/s'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(2.9573529564111874e-05))]),
    'fl-oz/min':
    Unit(symbols=['fl-oz/min'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(4.928921594018645e-07))]),
    'fl-oz/h':
    Unit(symbols=['fl-oz/h'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(8.214869323364409e-09))]),
    'cup/s':
    Unit(symbols=['cup/s'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.000236588236512895))]),
    'pnt/s':
    Unit(symbols=['pnt/s'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.00047317647302579))]),
    'pnt/min':
    Unit(symbols=['pnt/min'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(7.886274550429832e-06))]),
    'pnt/h':
    Unit(symbols=['pnt/h'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1.3143790917383054e-07))]),
    'qt/s':
    Unit(symbols=['qt/s'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.00094635294605158))]),
    'gal/s':
    Unit(symbols=['gal/s'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.00378541178420632))]),
    'gal/min':
    Unit(symbols=['gal/min'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(6.309019640343866e-05))]),
    'galUS/min':
    Unit(symbols=['galUS/min'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(5.253357806982644e-05))]),
    'gal/h':
    Unit(symbols=['gal/h'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1.0515032733906443e-06))]),
    'ft3/s':
    Unit(symbols=['ft3/s'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.028316831998814504))]),
    'ft3/min':
    Unit(symbols=['ft3/min'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.0004719471999802417))]),
    'ft3/h':
    Unit(symbols=['ft3/h'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(7.865786666337362e-06))]),
    'yd3/s':
    Unit(symbols=['yd3/s'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.764555587762115))]),
    'yd3/min':
    Unit(symbols=['yd3/min'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.012742593129368584))]),
    'yd3/h':
    Unit(symbols=['yd3/h'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.00021237655215614306))]),
    'STBPD':
    Unit(symbols=[
        'STBPD', 'STB/DAY', 'B/D', 'BPD', 'bpd', 'stbpd', 'BarrelsPerDay',
        'StdBarrelPerDay', 'StockTankBarrelPerDay', 'RB/DAY'
    ],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1.842233734980409e-06))]),
    'MSTBPD':
    Unit(symbols=[
        'MSTBPD', 'MSTB/d', 'MSTB/DAY', 'Mstbpd', 'ThousandBarrelsPerDay',
        'ThousandStdBarrelPerDay', 'ThousandStockTankBarrelPerDay'
    ],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.001842233734980409))]),
    'SCFD':
    Unit(symbols=[
        'SCFD', 'SCF/d', 'cfd', 'scf/day', 'scfd', 'ft3/day',
        'StdCubicFeetPerDay', 'CubicFeetPerDay'
    ],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(3.27741280556e-07))]),
    'MSCFD':
    Unit(symbols=[
        'MSCFD', 'MSCF/d', 'MSCF/DAY', 'Mcfd', 'Mscfd',
        'ThousandStdCubicFeetPerDay', 'ThousandCubicFeetPerDay'
    ],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.000327741280556))]),
    'MMSCFD':
    Unit(symbols=[
        'MMSCFD', 'MMSCFPD', 'MMSCF/d', 'MMcfd', 'MMscfd', 'Mmscfd',
        'Millionft3/day', 'mmscf/day', 'MillionStdCubicFeetPerDay',
        'MillionCubicFeetPerDay'
    ],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.327741280556))]),
}

VolumetricFlowRate = Quantity('Volumetric Flow Rate', _units, [])

