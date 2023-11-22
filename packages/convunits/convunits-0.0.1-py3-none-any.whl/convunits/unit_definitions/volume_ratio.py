"""
Volume Ratio quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'v/v':
    Unit(symbols=['v/v', 'vol/vol', 'volume/volume'],
         system=UnitSystem.METRIC,
         transformations=[]),
    '%v/v':
    Unit(
        symbols=['%v/v', 'vol/vol percent', 'volume/volume percentage'],
        system=UnitSystem.METRIC,
        transformations=[FactorOperation(Num(0.01))],
        note=(
            'Necessary to allow volume ratio percentage (keeping distiction from a ratio '
            'without specified quantities). Symbol from: '
            'https://www.thoughtco.com/definition-of-volume-volume-percentage-605945#:~:text=Volume%2Fvolume%20percentage%20(v%2F,v%20percent)%20of%2012%20percent.'  # pylint: disable=line-too-long
        )),
    'l/l':
    Unit(symbols=['l/l', 'liters/liters'],
         system=UnitSystem.METRIC,
         transformations=[]),
    'ft3/ft3':
    Unit(symbols=['ft3/ft3', 'cf/cf', 'scf/scf', 'SCF/SCF'],
         system=UnitSystem.IMPERIAL,
         transformations=[]),
    'm3/m3':
    Unit(symbols=['m3/m3', 'M3/M3'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'STB/STB':
    Unit(symbols=['STB/STB', 'stb/stb'],
         system=UnitSystem.IMPERIAL,
         transformations=[]),
    'scf/stb':
    Unit(symbols=[
        'scf/stb', 'cf/stb', 'SCF/STB', 'StdCubicFeetPerStockTankBarrel',
        'StdCubicFeetPerStdBarrel'
    ],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.17810760667903525))]),
    'stb/scf':
    Unit(symbols=[
        'stb/scf', 'stb/cf', 'STB/SCF', 'StockTankBarrelPerStdCubicFoot',
        'StdBarrelPerStdCubicFoot'
    ],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(5.614583333333334))]),
    'stb/Mscf':
    Unit(symbols=[
        'stb/Mscf', 'stb/Mcf', 'STB/MSCF',
        'StockTankBarrelPerThousandStdCubicFeet',
        'StdBarrelPerThousandStdCubicFeet'
    ],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(0.005614583333333333))]),
    'Mscf/stb':
    Unit(symbols=[
        'Mscf/stb', 'Mcf/stb', 'MSCF/STB',
        'ThousandStdCubicFeetPerStockTankBarrel',
        'ThousandStdCubicFeetPerStdBarrel'
    ],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(178.10760667903526))]),
}

VolumeRatio = Quantity('Volume Ratio', _units, [])

