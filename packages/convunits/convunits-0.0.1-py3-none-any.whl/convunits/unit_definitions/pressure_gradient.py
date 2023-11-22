"""
Pressure Gradient quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'Pa/m':
    Unit(symbols=['Pa/m'],
         default=True,
         system=UnitSystem.METRIC,
         transformations=[]),
    'kPa/m':
    Unit(symbols=['kPa/m'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000))]),
    'MPa/m':
    Unit(symbols=['MPa/m'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000))]),
    'GPa/m':
    Unit(symbols=['GPa/m'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(1000000000))]),
    'Pa/ft':
    Unit(symbols=['Pa/ft'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(3.28084))]),
    'kPa/ft':
    Unit(symbols=['kPa/ft'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(3280.84))]),
    'MPa/ft':
    Unit(symbols=['MPa/ft'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(3280840))]),
    'GPa/ft':
    Unit(symbols=['GPa/ft'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(3280840000))]),
    'bar/m':
    Unit(symbols=['bar/m'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(100000))]),
    'bar/ft':
    Unit(symbols=['bar/ft'],
         system=UnitSystem.METRIC,
         transformations=[FactorOperation(Num(328084))]),
    'psi/ft':
    Unit(symbols=['psi/ft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(22620.5948))]),
    'kpsi/ft':
    Unit(symbols=['kpsi/ft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(22620594.8))]),
    'Mpsi/ft':
    Unit(symbols=['Mpsi/ft'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(22620594800))]),
    'psi/m':
    Unit(symbols=['psi/m'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(6894.757074407773))]),
    'kpsi/m':
    Unit(symbols=['kpsi/m'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(6894757.074407774))]),
    'Mpsi/m':
    Unit(symbols=['Mpsi/m'],
         system=UnitSystem.IMPERIAL,
         transformations=[FactorOperation(Num(6894757074.407773))]),
}

PressureGradient = Quantity('Pressure Gradient', _units, [])

