from __future__ import annotations

from pytest import fixture


@fixture()
def input_data() -> str:
    return """\
Player 1 starting position: 4
Player 2 starting position: 8"""
