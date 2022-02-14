from __future__ import annotations
import argparse
from collections import Generator, defaultdict
from math import prod
from pathlib import Path
from typing import Optional, Union

import pytest
from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")


def adjacent(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    yield x + 1, y
    yield x - 1, y
    yield x, y + 1
    yield x, y - 1


def compute(s: Union[list[str], str], testing: Optional[bool] = None) -> int:
    coords = defaultdict(lambda: 9)

    lines = s if testing and type(s) == list[str] else s.splitlines()
    for y, line in enumerate(lines):
        for x, char in enumerate(line):
            coords[x, y] = int(char)

    minimums = [
        (x, y)
        for (x, y), n in coords.items()
        if all(coords.get(point, 9) > n for point in adjacent(x, y))
    ]

    largest_minimum: list[int] = []
    for x, y in minimums:
        viewed = set()
        todo = [(x, y)]

        while todo:
            x, y = todo.pop()
            viewed.add((x, y))

            for point in adjacent(x, y):
                if point not in viewed and coords[point] != 9:
                    todo.append(point)

        if len(largest_minimum) < 3:
            largest_minimum.append(len(viewed))
        else:
            for maximum in sorted(largest_minimum):
                if len(viewed) > maximum:
                    largest_minimum[largest_minimum.index(maximum)] = len(viewed)
                    break

    return prod(largest_minimum)


def test(input_data) -> None:
    assert compute(input_data, testing=True) == 1134


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
