from __future__ import annotations

import argparse
import itertools
from pathlib import Path

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")


def cycle_board(n: int) -> int:
    while n > 10:
        n -= 10
    return n


def compute(s: str) -> int:
    lines = s.splitlines()
    p1_location = int(lines[0].split()[-1])
    p2_location = int(lines[1].split()[-1])

    die_count = 0
    die = itertools.cycle(range(1, 101))
    p1_score = p2_score = 0  # set both scores to 0

    while True:
        p1_location = cycle_board(p1_location + next(die) + next(die) + next(die))
        die_count += 3
        p1_score += p1_location

        if p1_score >= 21:
            break

        p2_location = cycle_board(p2_location + next(die) + next(die) + next(die))
        die_count += 3
        p2_score += p2_location

        if p2_score >= 21:
            break

    return die_count * min(p1_score, p2_score)


def test(input_data: str) -> None:
    assert compute(input_data) == 739785


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
