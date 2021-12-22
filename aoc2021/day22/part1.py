from __future__ import annotations

import argparse
from pathlib import Path
from typing import NamedTuple

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")


class Reboot(NamedTuple):
    status: bool
    x: tuple[int, int]
    y: tuple[int, int]
    z: tuple[int, int]

    @classmethod
    def parse(cls, s: str):
        status, rest = s.split()
        x_range, y_range, z_range = rest.split(",")
        x_range, y_range, z_range = x_range[2:], y_range[2:], z_range[2:]
        x_0, x_1 = (int(x) for x in x_range.split(".."))
        y_0, y_1 = (int(y) for y in y_range.split(".."))
        z_0, z_1 = (int(z) for z in z_range.split(".."))
        return cls(status=status == "on", x=(x_0, x_1), y=(y_0, y_1), z=(z_0, z_1))


def compute(s: str) -> int:
    lines = s.splitlines()
    reboots = [Reboot.parse(line) for line in lines]

    coords = set()
    for step in reboots:
        new_coords = {
            (x, y, z)
            for x in range(max(step.x[0], -50), min(step.x[1], 50) + 1)
            for y in range(max(step.y[0], -50), min(step.y[1], 50) + 1)
            for z in range(max(step.z[0], -50), min(step.z[1], 50) + 1)
        }

        if step.status:
            coords |= new_coords
        else:
            coords -= new_coords
    return len(coords)


def test(input_data: str) -> None:
    assert compute(input_data) == 590784


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
