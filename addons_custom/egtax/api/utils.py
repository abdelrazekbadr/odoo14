from datetime import datetime
from typing import Any, List, Optional, TypeVar, Callable, Type, cast
import dateutil.parser

from collections import defaultdict, Counter

T = TypeVar("T")


def sum_group_by(dataset, group_by_key, sum_value_keys):
    dic = defaultdict(Counter)

    for item in dataset:
        key = item[group_by_key]
        vals = {k: item[k] for k in sum_value_keys}
        dic[key].update(vals)
    return dic


def from_str(x: Any) -> str:
    assert isinstance(x, str)
    return x


def from_datetime(x: Any) -> datetime:
    if x:
        return dateutil.parser.parse(x)



def from_float(x: Any) -> float:
    assert isinstance(x, (float, int)) and not isinstance(x, bool)
    return float(x)


def to_float(x: Any) -> float:
    if not isinstance(x, float):
        print(x)
    assert isinstance(x, float),x
    return x


def from_int(x: Any) -> int:
    assert isinstance(x, int) and not isinstance(x, bool)
    return x


def from_list(f: Callable[[Any], T], x: Any) -> List[T]:
    assert isinstance(x, list)
    return [f(y) for y in x]


def to_class(c: Type[T], x: Any) -> dict:
    assert isinstance(x, c)
    return cast(Any, x).to_dict()


def from_none(x: Any) -> Any:
    assert x is None , f"{x} is null"
    return x


def from_union(fs, x):
    for f in fs:
        try:
            return f(x)
        except :
            pass
    assert False, x


def is_type(t: Type[T], x: Any) -> T:
    assert isinstance(x, t)
    return x
