from tipsql.core.operator.eq_operator import EqOperator
from tipsql.core.operator.not_eq_operator import NotEqOperator
from tipsql.core.operator.order_operator import OrderOperator
from tipsql.core.relation.column import ColumnType


class Bigint(
    ColumnType[int],
    EqOperator[int, int],
    OrderOperator[int, int],
    NotEqOperator[int, int],
):
    __slots__ = ()


class Precision:
    def __init__(self, precision: int, /):
        self.value = precision


class Scale:
    def __init__(self, scale: int, /):
        self.value = scale
