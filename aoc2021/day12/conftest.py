from __future__ import annotations

from pytest import fixture


@fixture()
def input_data() -> str:
    return """start-A
start-b
A-c
A-b
b-d
A-end
b-end"""
