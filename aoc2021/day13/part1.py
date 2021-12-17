from __future__ import annotations

import argparse
from pathlib import Path

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")


def compute(s: str) -> int:
    coords = set()
    points, instruction = s.split("\n\n")
    for line in points.splitlines():
        x, y = line.split(",")
        coords.add((int(x), int(y)))

    for line in instruction.splitlines():
        start, end = line.split("=")
        direction = start[-1]
        value = int(end)

        if direction == "x":
            coords = {(x if x < value else value - (x - value), y) for x, y in coords}
        else:
            coords = {(x, y if y < value else value - (y - value)) for x, y in coords}
        break

    return len(coords)


def test(input_data: str) -> None:
    assert compute(input_data) == 17


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
