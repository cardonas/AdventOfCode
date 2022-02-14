from __future__ import annotations

from collections import namedtuple

from pytest import fixture

DATA = namedtuple("DATA", ["input_str", "expected"])

CONDITIONS = [
    DATA(input_str=""">""", expected=2),
    DATA(input_str="""^>v<""", expected=4),
    DATA(input_str="""^v^v^v^v^v""", expected=2),
]


@fixture(params=CONDITIONS)
def input_data(request) -> DATA:
    return request.param
