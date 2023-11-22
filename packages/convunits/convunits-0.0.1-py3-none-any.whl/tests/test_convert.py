import math

import numpy as np
import pandas as pd
import pytest
from pandas.testing import assert_series_equal
from numpy.testing import assert_array_equal

from convunits import Convert
from convunits.errors import ConversionNotSupportedError, UnitNotFoundError


def test_convert_pass():
    assert math.isclose(Convert(5, 'ft').to('m').evaluate(), 1.524, abs_tol=1e-7)


def test_convert_list_array_pass():
    a1 = Convert([1, 2, 3], 'm').to('ft').evaluate()
    a2 = np.array([3.28084, 6.56168, 9.84252])
    assert_array_equal(a1, a2)


def test_convert_np_array_pass():
    a1 = Convert(np.array([1, 2, 3]), 'm').to('ft').evaluate()
    a2 = np.array([3.28084, 6.56168, 9.84252])
    assert_array_equal(a1, a2)


def test_convert_series_pass():
    s1 = Convert(pd.Series([1, 2, 3], name='Test'), 'm').to('ft').evaluate()
    s2 = pd.Series([3.28084, 6.56168, 9.84252], name='Test')
    assert_series_equal(s1, s2)


def test_convert_wrong_quantity():
    with pytest.raises(ConversionNotSupportedError):
        Convert(5, 'km').to('kg')


def test_convert_invalid_source_quantity():
    with pytest.raises(UnitNotFoundError):
        Convert(5, 'whatever').to('km')


def test_convert_invalid_target_quantity():
    with pytest.raises(UnitNotFoundError):
        Convert(5, 'km').to('whatever')
