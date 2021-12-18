from __future__ import annotations

from collections import namedtuple

from pytest import fixture


@fixture()
def input_data() -> str:
    return """\
8A004A801A8002F478
"""


DATA = namedtuple("DATA", ["input", "expected"])

COLLECTION = [
    DATA("C200B40A82", 3),
    DATA("04005AC33890", 54),
    DATA("880086C3E88112", 7),
    DATA("CE00C43D881120", 9),
    DATA("D8005AC2A8F0", 1),
    DATA("F600BC2D8F", 0),
    DATA("9C005AC2F8F0", 0),
    DATA("9C0141080250320F1802104A08", 1),
]


@fixture(params=COLLECTION)
def input_data2(request) -> str:
    return request.param
