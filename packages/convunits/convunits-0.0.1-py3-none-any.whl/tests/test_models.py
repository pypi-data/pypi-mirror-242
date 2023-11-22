import pytest

from convunits.expression import Num
from convunits.models import FactorOperation, Quantity, ShiftOperation, Unit, UnitSystem


@pytest.fixture
def torque():
    _units = {
        'Nm': Unit(symbols=['Nm'], default=True, system=UnitSystem.METRIC, transformations=[]),
        'lbf.ft': Unit(symbols=['lbf.ft'], system=UnitSystem.IMPERIAL, transformations=[FactorOperation(Num(1.355818))]),
        'klbf.ft': Unit(symbols=['klbf.ft', '1000lbf.ft', 'klb-ft', '1000lb-ft'], system=UnitSystem.IMPERIAL, transformations=[FactorOperation(Num(1355.818))]),
    }

    return Quantity('Torque', _units, [])


@pytest.fixture
def factor_op_two():
    return FactorOperation(Num(2))


@pytest.fixture
def shift_op_two():
    return ShiftOperation(Num(2))


def test_find_default_unit(torque):
    assert torque.find_default_unit() == 'Nm'


def test_factor_operation_apply(factor_op_two):
    assert factor_op_two.apply(Num(3)).evaluate() == 6


def test_factor_operation_unapply(factor_op_two):
    assert factor_op_two.unapply(Num(3)).evaluate() == 1.5


def test_shift_operation_apply(shift_op_two):
    assert shift_op_two.apply(Num(3)).evaluate() == 5


def test_shift_operation_unapply(shift_op_two):
    assert shift_op_two.unapply(Num(3)).evaluate() == 1
