"""
API Gravity quantity module.
"""

from convunits.models import FactorOperation, Quantity, Unit, UnitSystem
from convunits.expression import Num

_units = {
    'API':
    Unit(
        symbols=['API', '°API', 'API degrees', 'API grade', 'API gravity'],
        system=UnitSystem.METRIC,
        default=True,
        transformations=[FactorOperation(Num(1))],
        note=
        ('[do not confuse with \'gAPI\' Gamma Ray unit in radioactivity]. American '
         'Petroleum Institute (API) gravity, aka API Gravity. Measure of how heavy or '
         'light a petroleum liquid is compared to water: if its API gravity is greater '
         'than 10, it is lighter and floats on water; if less than 10, it is heavier '
         'and sinks. Calculated as an inverse function of Specific Gravity (SG) of the '
         'liquid: API gravity= 141.5/SG - 131.5 see: '
         'https://en.wikipedia.org/wiki/API_gravity Light crude oil has an API gravity '
         'higher than 31.1° (less than 870 kg/m3); Medium oil has an API gravity '
         'between 22.3 and 31.1° (870 to 920 kg/m3); Heavy crude oil has an API gravity '
         'below 22.3° (920 to 1000 kg/m3); Extra heavy oil has an API gravity below '
         '10.0° (greater than 1000 kg/m3)')),
}

ApiGravity = Quantity('API Gravity', _units, [])

