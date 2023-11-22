"""
Volume quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'nm3':
    Unit(symbols=['nm3', 'nm^3'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-27))]),
    'um3':
    Unit(symbols=['um3', 'um^3'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-18))]),
    'mm3':
    Unit(symbols=['mm3', 'mm^3'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-09))]),
    'cm3':
    Unit(symbols=['cm3', 'cm^3'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-06))]),
    'ml':
    Unit(symbols=['ml'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-06))]),
    'cl':
    Unit(symbols=['cl'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-05))]),
    'dl':
    Unit(symbols=['dl'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.0001))]),
    'l':
    Unit(symbols=['l', 'Litres', 'Liters', 'litres', 'liter', 'liters', 'L'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.001))]),
    'kl':
    Unit(symbols=['kl'], system=UnitSystem.METRIC, transformations=[]),
    'm3':
    Unit(symbols=['m3', 'm^3', 'v', 'meter3'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'km3':
    Unit(symbols=['km3', 'km^3'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000000))]),
    'krm':
    Unit(symbols=['krm'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1e-06))]),
    'tsk':
    Unit(symbols=['tsk'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(5e-06))]),
    'msk':
    Unit(symbols=['msk'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1.4999999999999999e-05))]),
    'kkp':
    Unit(symbols=['kkp'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.00015))]),
    'glas':
    Unit(symbols=['glas'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.0002))]),
    'kanna':
    Unit(symbols=['kanna'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(0.002617))]),
    'tsp':
    Unit(symbols=['tsp'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(4.928921608595207e-06))]),
    'Tbs':
    Unit(symbols=['Tbs'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1.4786764825785619e-05))]),
    'in3':
    Unit(symbols=['in3', 'in^3'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(1.638698851523214e-05))]),
    'fl-oz':
    Unit(symbols=['fl-oz'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(2.9573529651571238e-05))]),
    'cup':
    Unit(symbols=['cup'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.0002365882372125699))]),
    'pnt':
    Unit(symbols=['pnt'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.0004731764744251398))]),
    'qt':
    Unit(symbols=['qt'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.0009463529488502796))]),
    'gal':
    Unit(symbols=['gal', 'Gal', 'Galon', 'galon'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.0037854117954011185))]),
    'galUS':
    Unit(symbols=['galUS', 'GalUS', 'GalonUS', 'galonUS'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.0031520146935112067))]),
    'yd3':
    Unit(symbols=['yd3'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.7645555900231757))]),
    'bbl':
    Unit(
        symbols=[
            'bbl', 'barrel', 'STB', 'StandardBarrel', 'StdBarrel',
            'StockTankBarrel', 'RB', 'ReservoirBarrel', 'rb'
        ],
        system=UnitSystem.IMPERIAL,
        transformations=[FactorOperation(Num(0.15898711796566906))],
        note=
        ('reservoir or standard are not the unit itself (which is barrel or bbl) and '
         'are only information about the conditions in which that unit was measured '
         '(the unit itself is independent of conditions). Therefore, to not loose this '
         'information, we decided to keep track of the original unit symbol, meaning '
         'rb, RB or ReservoirBarrel and display it along with the data so that the '
         'client (UI or user) knows where that number comes from. We should however '
         'bear this in mind if we make conversions from rb to any other unit, because '
         'the reservoir detail will be ignored.')),
    'ft3':
    Unit(symbols=['ft3', 'ft^3', 'SCF'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.028316832082557367))]),
    'MSCF':
    Unit(symbols=['MSCF', 'ThousandStandardCubicFeet', 'ThousandStdCubicFeet'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(28.31683208255737))]),
    'MMSCF':
    Unit(symbols=[
        'MMSCF', 'MillionStandardCubicFeet', 'MillionStandardCubicFeet'
    ],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(28316.83208255737))]),
    'BSCF':
    Unit(symbols=[
        'BSCF', 'BillionStandardCubicFeet', 'BillionStandardCubicFeet'
    ],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(28316832.082557365))]),
    'MSTB':
    Unit(symbols=[
        'MSTB', 'ThousandStandardBarrel', 'ThousandStdBarrel',
        'ThousandStockTankBarrel'
    ],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(158.98711796566906))]),
    'MMSTB':
    Unit(symbols=[
        'MMSTB', 'MillionStandardBarrel', 'MillionStdBarrel',
        'MillionStockTankBarrel'
    ],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(158987.11796566905))]),
}

Volume = Quantity('Volume', _units, [])

