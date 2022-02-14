from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Optional, Union

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")


def compute(s: Union[list[str], str], testing: Optional[bool] = None) -> int:
    lines = s if testing and type(s) == list[s] else s.splitlines()
    points: Counter[tuple[int, int]] = Counter()
    for line in lines:
        start, end = line.split(" -> ")
        point_x1, point_y1 = start.split(",")
        point_x2, point_y2 = end.split(",")
        x1, y1, x2, y2 = int(point_x1), int(point_y1), int(point_x2), int(point_y2)

        if x1 < x2:
            x_diff = 1
        elif x1 > x2:
            x_diff = -1
        else:
            x_diff = 0

        if y1 < y2:
            y_diff = 1
        elif y1 > y2:
            y_diff = -1
        else:
            y_diff = 0

        x, y = x1, y1
        while (x, y) != (x2 + x_diff, y2 + y_diff):
            points[(x, y)] += 1
            x, y = x + x_diff, y + y_diff

    return sum(number >= 2 for number in points.values())


def test(input_data) -> None:
    assert compute(input_data, testing=True) == 12


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
