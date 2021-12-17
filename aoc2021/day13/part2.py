from __future__ import annotations

import argparse
from pathlib import Path

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")


def compute(s: str) -> str:
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
    max_x = max(x for x, _ in coords)
    max_y = max(y for _, y in coords)

    return "\n".join(
        "".join("#" if (x, y) in coords else " " for x in range(max_x + 1))
        for y in range(max_y + 1)
    )


EXPECTED_S = """\
#####
#   #
#   #
#   #
#####
"""


def test(input_data: str) -> None:
    assert compute(input_data) == EXPECTED_S.rstrip()


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
