from __future__ import annotations
import argparse
from math import prod
from pathlib import Path
from typing import Optional, Union

import pytest
from support import timing

INPUT_TXT = Path(__file__).parent.joinpath('input.txt')


def compute(s: Union[list[str], str], testing: Optional[bool] = None) -> int:
    lines = s if testing and type(s) == list[str] else s.splitlines()
    ribbon_lengths = []
    for line in lines:
        min_1, min_2, _ = sorted([int(x) for x in line.split('x')])
        ribbon_bow = prod([int(x) for x in line.split('x')])
        ribbon_length = min_1 * 2 + min_2 * 2
        ribbon_lengths.append(ribbon_bow+ribbon_length)
    return sum(ribbon_lengths)


def test(input_data) -> None:
    assert compute(input_data, testing=True) == 48


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
