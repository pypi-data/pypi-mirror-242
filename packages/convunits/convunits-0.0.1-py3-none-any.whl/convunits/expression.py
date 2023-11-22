"""Expression module.

This module contains basic arithmetic expressions to help with the conversion
library.
"""

from abc import ABC, abstractmethod
from functools import singledispatch, update_wrapper
from typing import Any, Union

import numpy as np
import pandas as pd


def singledispatchmethod(func: Any) -> Any:
    """Single dispatch class method decorator.

    To support Python 3.7, I'm using a hack for `singledispatch`. See
    https://stackoverflow.com/questions/24601722/how-can-i-use-functools-singledispatch-with-instance-methods
    for the explanation on how single dispatch works here.

    Args:
        func (Callable): Callable function.

    Returns:
        Callable: Dispatched function.
    """
    dispatcher = singledispatch(func)
    def wrapper(*args, **kw):
        return dispatcher.dispatch(args[1].__class__)(*args, **kw)
    wrapper.register = dispatcher.register
    update_wrapper(wrapper, func)

    return wrapper


class NumEvaluator:
    """Evaluator helper class.

    The evaluator just handles different data types when evaluating different
    types in conversion.

    Raises:
        TypeError: Non-numeric type or unsupported type.
        NotImplementedError: Unsupported NumPy array.

    Returns:
        Any: The value evaluated as its native type or ndarray for lists.
    """

    @singledispatchmethod
    def evaluate(self, value: Any) -> Any:
        raise TypeError(f'Evaluation failed. Type {type(value)} is not a number or array-like')

    @evaluate.register(int)
    def _int_eval(self, value: int) -> int:
        return value

    @evaluate.register(float)
    def _float_eval(self, value: float) -> float:
        return value

    @evaluate.register(list)
    def _list_eval(self, value: list) -> np.ndarray:
        return self._array_eval(np.array(value))

    @evaluate.register(pd.Series)
    def _series_eval(self, value: pd.Series) -> pd.Series:
        return value

    @evaluate.register(np.ndarray)
    def _array_eval(self, value: np.ndarray) -> np.ndarray:
        if not np.issubdtype(value.dtype, np.number):
            raise TypeError('Evaluation failed. Cannot evaluate non-numeric type')

        if not value.ndim < 2:
            raise NotImplementedError('Evaluation failed. No support for arrays of dimensions > 2')

        return value


class Expression(ABC):
    """Base expression.

    This is an abstract base class that all other expressions should inherit.
    It should *not* be instantiated in code.
    """
    @abstractmethod
    def evaluate(self) -> Union[int, float, list, np.ndarray, pd.Series]:
        """Abstract evaluation method.

        Expressions should evaluate into a numerical type to some extent. Edge
        cases must be resolved in the subclass implementation.

        Returns:
            float: the expression evaluated.
        """
        pass

    @abstractmethod
    def __repr__(self) -> str:
        """Abstract "string-ify" dunder method.

        Returns:
            str: representation of the expression.
        """
        pass


class Num(Expression):
    """Number expression.

    This expression just contains a numerical value. NOTE: This expression
    class' name is kept for legacy reasons to match the codebase of the
    TypeScript library. It accepts numeric objects and also array-like objects.

    Attributes:
        value: the value of the expression
    """
    def __init__(self, value: Union[int, float, list, np.ndarray, pd.Series]) -> None:
        super().__init__()
        self.value = value

    def evaluate(self) -> Union[int, float, list, np.ndarray, pd.Series]:
        """Number evaluation.

        Raises:
            ValueError: Evaluation failed, the input is malformed.

        Returns:
            float: The value of the expression
        """
        return NumEvaluator().evaluate(self.value)

    def __repr__(self) -> str:
        """Value representation.

        Returns:
            str: The value
        """
        return str(self.value)


class Op(Expression):
    """Base operation expression.

    This is an abstract class for operation expressions. All expressions have
    the same __init__ functionality and this class helps register the that into
    the MRO. It should *not* be instantiated in code.

    Attributes:
        l: left expression
        r: right expression
    """
    def __init__(self, l: Expression, r: Expression) -> None:
        super().__init__()
        self.l = l
        self.r = r


class Add(Op):
    """Addition expression.

    This class inherits the Op class and has the same attributes.
    """
    def evaluate(self) -> Union[int, float, list, np.ndarray, pd.Series]:
        """Addition evaluation.

        Returns:
            float: the expression on the left plus the expression on the right
        """
        return self.l.evaluate() + self.r.evaluate()

    def __repr__(self) -> str:
        """Addition expression representation.

        Returns:
            str: this expression as ({left expression}+{right expression})
        """
        return f'({str(self.l)}+{str(self.r)})'


class Div(Op):
    """Division expression.

    This class inherits the Op class and has the same attributes.
    """
    def evaluate(self) -> Union[int, float, list, np.ndarray, pd.Series]:
        """Division evaluation.

        Returns:
            float: the expression on the left divided by the expression on the
                right
        """
        return self.l.evaluate() / self.r.evaluate()

    def __repr__(self) -> str:
        """Division expression representation.

        Returns:
            str: this expression as ({left expression}/{right expression})
        """
        return f'({str(self.l)}/{str(self.r)})'


class Mul(Op):
    """Multiplication expression.

    This class inherits the :py:class:`Op` class and has the same attributes.
    """
    def evaluate(self) -> Union[int, float, list, np.ndarray, pd.Series]:
        """Multiplication evaluation.

        Returns:
            float: the expression on the left multiplied by the expression on
                the right
        """
        return self.l.evaluate() * self.r.evaluate()

    def __repr__(self) -> str:
        """Multiplication expression representation.

        Returns:
            str: this expression as ({left expression}*{right expression})
        """
        return f'({str(self.l)}*{str(self.r)})'


class Sub(Op):
    """Subtraction expression.

    This class inherits the Op class and has the same attributes.
    """
    def evaluate(self) -> Union[int, float, list, np.ndarray, pd.Series]:
        """Substraction evaluation.

        Returns:
            float: the expression on the left minus the expression on the
                right
        """
        return self.l.evaluate() - self.r.evaluate()

    def __repr__(self) -> str:
        """Substraction expression representation.

        Returns:
            str: this expression as ({left expression}-{right expression})
        """
        return f'({str(self.l)}-{str(self.r)})'
