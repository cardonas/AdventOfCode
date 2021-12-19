from __future__ import annotations

from pytest import fixture


@fixture()
def input_data() -> str:
    return """\
target area: x=20..30, y=-10..-5
"""
