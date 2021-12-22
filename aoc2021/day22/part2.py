from __future__ import annotations

import argparse
from pathlib import Path
from typing import NamedTuple

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")


class Cube(NamedTuple):
    x0: int
    x1: int
    y0: int
    y1: int
    z0: int
    z1: int

    @property
    def size(self) -> int:
        return (self.x1 - self.x0) * (self.y1 - self.y0) * (self.z1 - self.z0)

    def intersects(self, other: Cube) -> bool:
        return (
            self.x0 <= other.x1 - 1
            and self.x1 - 1 >= other.x0
            and self.y0 <= other.y1 - 1
            and self.y1 - 1 >= other.y0
            and self.z0 <= other.z1 - 1
            and self.z1 - 1 >= other.z0
        )

    def contains(self, other: Cube) -> bool:
        return (
            self.x0 <= other.x0
            and self.x1 >= other.x1
            and self.y0 <= other.y0
            and self.y1 >= other.y1
            and self.z0 <= other.z0
            and self.z1 >= other.z1
        )

    def subtract(self, other: Cube) -> list[Cube]:
        if not self.intersects(other):
            return [self]
        elif other.contains(self):
            return []

        xs = sorted((self.x0, self.x1, other.x0, other.x1))
        ys = sorted((self.y0, self.y1, other.y0, other.y1))
        zs = sorted((self.z0, self.z1, other.z0, other.z1))

        ret = []
        for x0, x1 in zip(xs, xs[1:]):
            for y0, y1 in zip(ys, ys[1:]):
                for z0, z1 in zip(zs, zs[1:]):
                    cube = Cube(x0, x1, y0, y1, z0, z1)
                    if self.contains(cube) and not cube.intersects(other):
                        ret.append(cube)
        return ret

    @classmethod
    def parse(cls, x: str, y: str, z: str) -> Cube:
        x_0_s, x_1_s = x.split("..")
        y_0_s, y_1_s = y.split("..")
        z_0_s, z_1_s = z.split("..")
        return cls(
            int(x_0_s),
            int(x_1_s) + 1,
            int(y_0_s),
            int(y_1_s) + 1,
            int(z_0_s),
            int(z_1_s) + 1,
        )


class Reboot(NamedTuple):
    status: bool
    cube: Cube

    @classmethod
    def parse(cls, s: str):
        status, rest = s.split()
        x_range, y_range, z_range = rest.split(",")
        x, y, z = x_range[2:], y_range[2:], z_range[2:]

        return cls(status=status == "on", cube=Cube.parse(x, y, z))


def compute(s: str) -> int:
    lines = s.splitlines()
    reboots = [Reboot.parse(line) for line in lines]

    cubes: list[Cube] = []
    for step in reboots:
        cubes = [part for cube in cubes for part in cube.subtract(step.cube)]
        if step.status:
            cubes.append(step.cube)

    return sum(cube.size for cube in cubes)


def test(input_data2: str) -> None:
    assert compute(input_data2) == 2758514936282235


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
