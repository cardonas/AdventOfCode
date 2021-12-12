from __future__ import annotations
import argparse
from pathlib import Path
from typing import Optional, Union

import pytest
from support import timing

INPUT_TXT = Path(__file__).parent.joinpath('input.txt')


def compute(s: Union[list[str], str], testing: Optional[bool] = None) -> int:
    lines = s if testing and type(s) == list[str] else s.splitlines()
    square_feet = []
    for line in lines:
        l, w, h = [int(x) for x in line.split('x')]
        areas = [l*w, w*h, h*l]
        areas_min = min(areas)
        surface_area = sum(2*area for area in areas)
        square_feet.append(surface_area+areas_min)
    return sum(square_feet)


def test(input_data) -> None:
    assert compute(input_data, testing=True) == 101


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
