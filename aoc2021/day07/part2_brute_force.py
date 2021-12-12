from __future__ import annotations
import argparse
import statistics
from pathlib import Path
from typing import Optional, Union

import pytest
from support import timing

INPUT_TXT = Path(__file__).parent.joinpath('input.txt')


def compute(s: Union[list[str], str], testing: Optional[bool] = None) -> int:
    lines = s if testing and type(s) == list[str] else s.split(',')
    crabs = [int(line) for line in lines]

    def get_val(n: int) -> int:
        return sum(abs(crab - n) * (abs(crab - n) + 1) // 2 for crab in crabs)

    return min(get_val(i) for i in range(min(crabs), max(crabs) + 1))


def test(input_data) -> None:
    assert compute(input_data, testing=True) == 168


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
