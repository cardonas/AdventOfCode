from __future__ import annotations
import argparse
from pathlib import Path
from typing import Optional, Union

import pytest
from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")


def compute(s: Union[list[str], str], testing: Optional[bool] = None) -> int:
    lines = s if testing and type(s) == list[str] else s.splitlines()
    numbers = []
    for line in lines:
        _, end = line.split(" | ")
        numbers.extend(end.split())
    return sum(len(seg) in (2, 3, 4, 7) for seg in numbers)


def test(input_data) -> None:
    assert compute(input_data, testing=True) == 26


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
