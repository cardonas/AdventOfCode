from __future__ import annotations

import argparse
import heapq
from pathlib import Path
from typing import Generator

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")


def next_p(x: int, y: int) -> Generator[tuple[int, int], None, None]:
    yield x - 1, y
    yield x, y - 1
    yield x + 1, y
    yield x, y + 1


def compute(s: str) -> int:
    coords = {}
    for y, line in enumerate(s.splitlines()):
        for x, c in enumerate(line):
            coords[(x, y)] = int(c)

    last_x, last_y = max(coords)
    best_at: dict[tuple[int, int], int] = {}

    todo = [(0, (0, 0))]

    while todo:
        cost, last_coord = heapq.heappop(todo)

        if last_coord in best_at and cost >= best_at[last_coord]:
            continue
        else:
            best_at[last_coord] = cost

        if last_coord == (last_x, last_y):
            return cost

        for cand in next_p(*last_coord):
            if cand in coords:
                heapq.heappush(todo, (cost + coords[cand], cand))
    return best_at[(last_x, last_y)]


def test(input_data: str) -> None:
    assert compute(input_data) == 40


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
