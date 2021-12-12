from __future__ import annotations
import argparse
from collections import Generator, defaultdict
from pathlib import Path
from typing import Optional, Union

import pytest
from support import timing

INPUT_TXT = Path(__file__).parent.joinpath('input.txt')



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

    return sum(
        n + 1
        for (x, y), n in tuple(coords.items())
        if all(coords[point] > n for point in adjacent(x, y))
    )


def test(input_data) -> None:
    assert compute(input_data, testing=True) == 15


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
