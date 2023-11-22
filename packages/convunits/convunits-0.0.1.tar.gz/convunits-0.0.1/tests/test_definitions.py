from convunits.models import Quantity
from convunits.definitions import DEFINITIONS, find_quantity_by, find_quantity_by_unit_symbol, find_unit_standard, find_units_by_quantity


def test_valid_find_quantity_by():
    quantity = find_quantity_by('m/s')
    assert isinstance(quantity, Quantity)
    assert quantity.name == 'Velocity'


def test_invalid_find_quantity_by():
    quantity = find_quantity_by('whatever')
    assert quantity is None


def test_valid_find_quantity_by_unit_symbol():
    accelaration = find_quantity_by_unit_symbol('m/s2')
    angle = find_quantity_by_unit_symbol('RAD')
    length = find_quantity_by_unit_symbol('ft')
    pressure = find_quantity_by_unit_symbol('MPa')
    pressureTwo = find_quantity_by_unit_symbol('MPa')  # Repeated to test caching.
    assert isinstance(accelaration, Quantity)
    assert isinstance(angle, Quantity)
    assert isinstance(length, Quantity)
    assert isinstance(pressure, Quantity)
    assert isinstance(pressureTwo, Quantity)
    assert accelaration.name == 'Acceleration'
    assert angle.name == 'Angle'
    assert length.name == 'Length'
    assert pressure.name == 'Pressure'
    assert pressureTwo.name == 'Pressure'


def test_invalid_find_quantity_by_unit_symbol():
    quantity = find_quantity_by_unit_symbol('whatever')
    assert quantity is None


def test_valid_find_unit_standard():
    length_unit_standard = find_unit_standard('inch')
    power_flow_rate_unit_standard = find_unit_standard('ThousandStdCubicFeetPerDay')
    power_unit_standard = find_unit_standard('GW')
    velocity_standard = find_unit_standard('m/h')
    accelation_standard = find_unit_standard('m/s2')

    assert length_unit_standard == 'in'
    assert power_flow_rate_unit_standard == 'MSCFD'
    assert power_unit_standard == 'GW'
    assert velocity_standard == 'm/h'
    assert accelation_standard == 'm/s2'


def test_invalid_find_unit_standard():
    unit = find_unit_standard('whatever')
    assert unit is None


def test_quantity_has_exactly_one_default_unit():
    for quantity in DEFINITIONS:
        default_count = len([unit for unit in quantity.units.values() if unit.default])
        assert default_count == 1


def test_valid_find_units_by_quantity():
    velocity_unit_symbols = ['m/s', 'km/h', 'm/h', 'knot', 'ft/s', 'ft/min', 'ft/h']
    units = find_units_by_quantity('Velocity')
    assert len(units) > 0
    for symbol in velocity_unit_symbols:
        assert symbol in units


def test_invalid_find_units_by_quantity():
    units = find_units_by_quantity('whatever')
    assert len(units) == 0
