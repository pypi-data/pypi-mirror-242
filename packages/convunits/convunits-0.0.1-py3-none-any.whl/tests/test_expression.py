import pytest

import numpy as np
import pandas as pd

from convunits.expression import Num, Add, Div, Mul, Sub


@pytest.fixture
def expr_add_one_two():
    return Add(Num(1), Num(2))


@pytest.fixture
def expr_div_one_two():
    return Div(Num(1), Num(2))


@pytest.fixture
def expr_mul_one_two():
    return Mul(Num(1), Num(2))


@pytest.fixture
def expr_sub_one_two():
    return Sub(Num(1), Num(2))


def test_num_evaluate():
    assert Num(1).evaluate() == 1


def test_num_evaluate_malformed():
    with pytest.raises(TypeError):
        Num('hello').evaluate()


def test_add_nums_evaluate(expr_add_one_two):
    assert expr_add_one_two.evaluate() == 3


def test_add_num_expr_evaluate(expr_add_one_two):
    assert Add(Num(1), expr_add_one_two).evaluate() == 4


def test_add_expr_expr_evaluate(expr_add_one_two):
    assert Add(expr_add_one_two, expr_add_one_two).evaluate() == 6


def test_div_nums_evaluate(expr_div_one_two):
    assert expr_div_one_two.evaluate() == 0.5


def test_div_num_expr_evaluate(expr_div_one_two):
    assert Div(Num(1), expr_div_one_two).evaluate() == 2


def test_div_expr_expr_evaluate(expr_div_one_two):
    assert Div(expr_div_one_two, expr_div_one_two).evaluate() == 1


def test_mul_nums_evaluate(expr_mul_one_two):
    assert expr_mul_one_two.evaluate() == 2


def test_mul_num_expr_evaluate(expr_mul_one_two):
    assert Mul(Num(1), expr_mul_one_two).evaluate() == 2


def test_mul_expr_expr_evaluate(expr_mul_one_two):
    assert Mul(expr_mul_one_two, expr_mul_one_two).evaluate() == 4


def test_sub_nums_evaluate(expr_sub_one_two):
    assert expr_sub_one_two.evaluate() == -1


def test_sub_num_expr_evaluate(expr_sub_one_two):
    assert Sub(Num(1), expr_sub_one_two).evaluate() == 2


def test_sub_expr_expr_evaluate(expr_sub_one_two):
    assert Sub(expr_sub_one_two, expr_sub_one_two).evaluate() == 0


def test_num_evaluate_dict_fails():
    with pytest.raises(TypeError):
        Num({}).evaluate()


def test_num_int_evaluates_as_int():
    assert isinstance(Num(1).evaluate(), int)


def test_num_float_evaluates_as_float():
    assert isinstance(Num(1.0).evaluate(), float)


def test_num_float_nan_evaluates_as_float():
    assert isinstance(Num(float('nan')).evaluate(), float)


def test_num_list_evaluates_as_array():
    assert isinstance(Num([0, 1, 2]).evaluate(), np.ndarray)


def test_num_list_evaluates_consistent_elements():
    assert np.all(Num([0, 1, 2]).evaluate() == np.array([0, 1, 2]))


def test_num_series_evaluates_as_series():
    assert isinstance(Num(pd.Series([0, 1, 2], name='yo')).evaluate(), pd.Series)


def test_num_array_evaluates_as_array():
    assert isinstance(Num(np.array([0, 1, 2])).evaluate(), np.ndarray)


def test_num_array_evaluate_non_numeric_fails():
    with pytest.raises(TypeError):
        Num(['a', 'b', 'c']).evaluate()


def test_num_array_evaluate_non_1d_fails():
    with pytest.raises(NotImplementedError):
        Num([[1, 2, 3]]).evaluate()
