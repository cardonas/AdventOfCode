from __future__ import annotations

import argparse
from collections import defaultdict
from pathlib import Path

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")


def parse_coords_hash(s: str) -> set[tuple[int, int]]:
    coords = set()
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            if c == "#":
                coords.add((x, y))
    return coords


def to_int(coords: dict[tuple[int, int], int], x: int, y: int) -> int:
    numbers = [
        coords[x - 1, y - 1],
        coords[x, y - 1],
        coords[x + 1, y - 1],
        coords[x - 1, y],
        coords[x, y],
        coords[x + 1, y],
        coords[x - 1, y + 1],
        coords[x, y + 1],
        coords[x + 1, y + 1],
    ]
    return int("".join(str(int(n)) for n in numbers), 2)


def compute(s: str) -> int:
    p1, p2 = s.split("\n\n")

    part1 = defaultdict(int)
    for i, c in enumerate(p1.strip()):
        if c == "#":
            part1[i] = 1

    part2_coords_s = parse_coords_hash(p2)
    part2_coords_d = defaultdict(
        int,
        dict.fromkeys(part2_coords_s, 1),
    )

    invert = int(part1[0] == 1 and part1[511] == 0)

    minx = min(x for x, _ in part2_coords_d)
    maxx = max(x for x, _ in part2_coords_d)
    miny = min(y for _, y in part2_coords_d)
    maxy = max(y for _, y in part2_coords_d)

    for _ in range(1):
        coords1 = defaultdict(
            lambda: invert,
            {
                (x, y): part1[to_int(part2_coords_d, x, y)]
                for y in range(miny - 1, maxy + 2)
                for x in range(minx - 1, maxx + 2)
            },
        )
        part2_coords_d = defaultdict(
            int,
            {
                (x, y): part1[to_int(coords1, x, y)]
                for y in range(miny - 2, maxy + 3)
                for x in range(minx - 2, maxx + 3)
            },
        )
        minx -= 2
        miny -= 2
        maxx += 2
        maxy += 2

    return sum(part2_coords_d.values())


def test(input_data: str) -> None:
    assert compute(input_data) == 35


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
