"""
Unit definitions compilation.
"""

from convunits.unit_definitions.acceleration import Acceleration
from convunits.unit_definitions.angle import Angle
from convunits.unit_definitions.angular_frequency import AngularFrequency
from convunits.unit_definitions.api_gravity import ApiGravity
from convunits.unit_definitions.apparent_power import ApparentPower
from convunits.unit_definitions.area import Area
from convunits.unit_definitions.charge import Charge
from convunits.unit_definitions.conductivity import Conductivity
from convunits.unit_definitions.current import Current
from convunits.unit_definitions.density import Density
from convunits.unit_definitions.dogleg_severity import DoglegSeverity
from convunits.unit_definitions.each import Each
from convunits.unit_definitions.energy import Energy
from convunits.unit_definitions.force import Force
from convunits.unit_definitions.frequency import Frequency
from convunits.unit_definitions.gamma_ray import GammaRay
from convunits.unit_definitions.illuminance import Illuminance
from convunits.unit_definitions.inverse_length import InverseLength
from convunits.unit_definitions.inverse_resistivity import InverseResistivity
from convunits.unit_definitions.length import Length
from convunits.unit_definitions.mass import Mass
from convunits.unit_definitions.mass_flow_rate import MassFlowRate
from convunits.unit_definitions.money import Money
from convunits.unit_definitions.money_per_energy import MoneyPerEnergy
from convunits.unit_definitions.pixels import Pixels
from convunits.unit_definitions.power import Power
from convunits.unit_definitions.pressure import Pressure
from convunits.unit_definitions.pressure_gradient import PressureGradient
from convunits.unit_definitions.productivity_index import ProductivityIndex
from convunits.unit_definitions.ratio import Ratio
from convunits.unit_definitions.reactive_energy import ReactiveEnergy
from convunits.unit_definitions.reactive_power import ReactivePower
from convunits.unit_definitions.resistivity import Resistivity
from convunits.unit_definitions.slowness import Slowness
from convunits.unit_definitions.temperature import Temperature
from convunits.unit_definitions.temperature_difference import TemperatureDifference
from convunits.unit_definitions.time import Time
from convunits.unit_definitions.torque import Torque
from convunits.unit_definitions.unitless import Unitless
from convunits.unit_definitions.velocity import Velocity
from convunits.unit_definitions.voltage import Voltage
from convunits.unit_definitions.volume import Volume
from convunits.unit_definitions.volume_ratio import VolumeRatio
from convunits.unit_definitions.volumetric_flow_rate import VolumetricFlowRate

DEFINITIONS = [
    Acceleration, Angle, AngularFrequency, ApiGravity, ApparentPower, Area,
    Charge, Conductivity, Current, Density, DoglegSeverity, Each, Energy,
    Force, Frequency, GammaRay, Illuminance, InverseLength, InverseResistivity,
    Length, Mass, MassFlowRate, Money, MoneyPerEnergy, Pixels, Power, Pressure,
    PressureGradient, ProductivityIndex, Ratio, ReactiveEnergy, ReactivePower,
    Resistivity, Slowness, Temperature, TemperatureDifference, Time, Torque,
    Unitless, Velocity, Voltage, Volume, VolumeRatio, VolumetricFlowRate
]
