from __future__ import annotations
import argparse
from collections import defaultdict
from pathlib import Path
from typing import Generator, Optional, Union

import pytest
from support import timing

INPUT_TXT = Path(__file__).parent.joinpath('input.txt')


def adjacent(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    for x_d in {-1, 0, 1}:
        for y_d in {-1, 0, 1}:
            if x_d == y_d == 0:
                continue
            yield x + x_d, y + y_d


def compute(s: Union[list[str], str], testing: Optional[bool] = None) -> int:
    coords = {}
    lines = s if testing and type(s) == list[str] else s.splitlines()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            coords[(x, y)] = int(char)

    flashes = 0
    for _ in range(100):
        todo = []
        for point, value in coords.items():
            coords[point] += 1
            if value == 9:
                todo.append(point)
        while todo:
            flashing = todo.pop()
            if coords[flashing] == 0:
                continue
            coords[flashing] = 0
            flashes += 1
            for point in adjacent(*flashing):
                if point in coords and coords[point] != 0:
                    coords[point] += 1
                    if coords[point] > 9:
                        todo.append(point)
    return flashes


def test(input_data) -> None:
    assert compute(input_data, testing=True) == 1656


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
