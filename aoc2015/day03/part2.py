from __future__ import annotations

import argparse
from collections import namedtuple
from pathlib import Path

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")

# TODO: Complete part 2 of Day 3


def compute(input_str: str) -> int:
    lines = input_str.splitlines()
    coordinates = {"0x0"}
    for line in lines:
        tmp_coords = namedtuple("tmp_coords", ["x", "y"])

        current_loc = tmp_coords(x=0, y=0)
        for direction in line:
            if direction == "<":
                new_coords = tmp_coords(x=current_loc.x - 1, y=current_loc.y)
            elif direction == ">":
                new_coords = tmp_coords(x=current_loc.x + 1, y=current_loc.y)
            elif direction == "^":
                new_coords = tmp_coords(x=current_loc.x, y=current_loc.y + 1)
            elif direction == "v":
                new_coords = tmp_coords(x=current_loc.x, y=current_loc.y - 1)
            coordinates.add(f"{new_coords.x}x{new_coords.y}")
            current_loc = new_coords
    return len(coordinates)


def test(input_data) -> None:
    assert compute(input_data.input_str) == input_data.expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
