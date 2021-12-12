from __future__ import annotations
import argparse
from collections import namedtuple
from pathlib import Path
from typing import NamedTuple, Optional, Union

import pytest
from support import timing

INPUT_TXT = Path(__file__).parent.joinpath('input.txt')

direction = namedtuple("direction", ['direction', 'amount'])


def compute(s: Union[list[str], str], testing: Optional[bool] = None) -> int:
    forward_distance, depth = 0, 0
    if testing:
        numbers = [direction(*line.split(' ')) for line in s]
    else:
        numbers = [direction(*line.split(' ')) for line in s.splitlines()]
    for number in numbers:
        distance = int(number.amount)
        if number.direction == 'down':
            depth += distance
        elif number.direction == 'forward':
            forward_distance += distance
        elif number.direction == 'up':
            depth -= distance
    return forward_distance * depth


@pytest.fixture()
def input_data():
    return [
        "forward 5",
        "down 5",
        "forward 8",
        "up 3",
        "down 8",
        "forward 2",
    ]


def test(input_data) -> None:
    assert compute(input_data, testing=True) == 150


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
