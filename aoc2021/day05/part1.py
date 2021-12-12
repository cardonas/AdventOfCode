from __future__ import annotations
import argparse
from collections import Counter, namedtuple
from pathlib import Path
from typing import List, Optional, Union

import pytest
from support import timing

INPUT_TXT = Path(__file__).parent.joinpath('input.txt')
Point = namedtuple('Point', ['x', 'y'])


def join_lists(coordinates):
    joined_list = []
    for x in coordinates:
        joined_list.extend(x)
    return joined_list


def compute(s: Union[list[str], str], testing: Optional[bool] = None) -> int:
    lines = s if testing and type(s) == list[s] else s.splitlines()
    coordinates = [[Point(*point.split(',')) for point in line.split(' -> ')] for line in lines]
    updated_coordinates = get_missing_points(coordinates)
    joined_lists = join_lists(updated_coordinates)
    count = Counter(joined_lists)
    return sum(number >= 2 for number in count.values())


def get_missing_points(coordinates):
    new_coordinates = []
    for coord_set in coordinates:
        x1, y1 = [int(x) for x in coord_set[0]]
        x2, y2 = [int(x) for x in coord_set[1]]
        if x1 == x2:
            lowest = int(min([y1, y2]))
            for i in range(1, abs(y1 - y2)):
                coord_set.append(Point(str(x1), str(lowest + i)))
        elif y1 == y2:
            lowest = int(min([x1, x2]))
            for i in range(1, abs(x1 - x2)):
                coord_set.append(Point(str(lowest + i), str(y1)))
        else:
            continue
        new_coordinates.append(coord_set)
    return new_coordinates


def test(input_data) -> None:
    assert compute(input_data, testing=True) == 5


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
