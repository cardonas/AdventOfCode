from __future__ import annotations

from pytest import fixture


@fixture()
def input_data() -> str:
    return """\
1163751742
1381373672
2136511328
3694931569
7463417111
1319128137
1359912421
3125421639
1293138521
2311944581
"""
