"""
Pressure quantity module.
"""

from convunits.models import FactorOperation, Quantity, ShiftOperation, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'Pa':
    Unit(
        symbols=['Pa', 'PA', 'pa', 'pascales', 'pascal', 'Pascal', 'Pascales'],
        system=UnitSystem.METRIC,
        default=True,
        transformations=[]),
    'kPa':
    Unit(symbols=['kPa'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
    'MPa':
    Unit(symbols=['MPa'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000))]),
    'GPa':
    Unit(symbols=['GPa'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000000))]),
    'hPa':
    Unit(symbols=['hPa'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(100))]),
    'bar':
    Unit(symbols=['bar', 'Bar', 'BAR'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(100000))]),
    'barg':
    Unit(symbols=['barg', 'BARG', 'Barg', 'BarGauge'],
         system=UnitSystem.METRIC,
         transformations=[
             ShiftOperation(Num(1.01325)),
             FactorOperation(Num(100000))
         ]),
    'torr':
    Unit(symbols=['torr'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(133.32236842105263))]),
    'psi':
    Unit(
        symbols=[
            'psi', 'PoundsPerSquareInch', 'PSI', 'Psi', 'lb/in2', 'psia',
            'PoundsPerSquareInchAbsolute', 'PsiAbsolute', 'PSIA', 'Psia'
        ],
        system=UnitSystem.IMPERIAL,
        transformations=[FactorOperation(Num(6894.76000045014))],
        note=
        ('After debate we have established that, in the domain of the oil&gas industry, '
         'the unit symbol PSI refers to PSIA (0 at full vaccuum) as opposed to PSIG (0 '
         'at sea level atmospheric pressure), where [PSIG] = [PSIA] - 14.7.')),
    'kpsi':
    Unit(symbols=[
        'kpsi', 'Kpsi', 'ksi', 'KPSI', 'kpsia', 'Kpsia', 'ksia', 'KPSIA'
    ],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(6894760.00045014))]),
    'Mpsi':
    Unit(symbols=['Mpsi', 'MPSI', 'Mpsia', 'MPSIA'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(6894760000.45014))]),
    'psig':
    Unit(symbols=['psig', 'PSIG', 'Psig', 'PsiGauge'],
         system=UnitSystem.IMPERIAL,
         transformations=[
             ShiftOperation(Num(14.695948775)),
             FactorOperation(Num(6894.76000045014))
         ]),
    'kpsig':
    Unit(symbols=['kpsig', 'Kpsig', 'ksig', 'KPSIG'],
         system=UnitSystem.IMPERIAL,
         transformations=[
             ShiftOperation(Num(0.014695948775)),
             FactorOperation(Num(6894760.00045014))
         ]),
    'Mpsig':
    Unit(symbols=['Mpsig', 'MPSIG'],
         system=UnitSystem.IMPERIAL,
         transformations=[
             ShiftOperation(Num(1.4695948775e-05)),
             FactorOperation(Num(6894760000.45014))
         ]),
    'atm':
    Unit(symbols=[
        'atm', 'atmosphere', 'standard atmosphere', 'reference atmosphere',
        'Atm', 'ATM'
    ],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(101325))]),
}

Pressure = Quantity('Pressure', _units, [])

