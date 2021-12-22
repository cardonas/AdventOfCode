from __future__ import annotations

import argparse
import functools
import itertools
from collections import Counter
from pathlib import Path

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")


def cycle_board(n: int) -> int:
    while n > 10:
        n -= 10
    return n


def compute(s: str) -> int:
    lines = s.splitlines()
    p1 = int(lines[0].split()[-1])
    p2 = int(lines[1].split()[-1])

    die_rolls = Counter(
        sum(pt) for pt in itertools.product((1, 2, 3), (1, 2, 3), (1, 2, 3))
    )  # neat way to use Counter.

    # recursive function
    @functools.lru_cache(maxsize=None)
    def compute_wins(
        p1_loc: int, p1_score: int, p2_loc: int, p2_score: int
    ) -> tuple[int, int]:
        p1_wins = p2_wins = 0
        for k, ct in die_rolls.items():
            new_p1_loc = cycle_board(p1_loc + k)
            new_p1_score = p1_score + new_p1_loc
            if new_p1_score >= 21:
                p1_wins += ct
            else:
                tmp_p2_wins, tmp_p1_wins = compute_wins(
                    p2_loc, p2_score, new_p1_loc, new_p1_score
                )
                p1_wins += tmp_p1_wins * ct
                p2_wins += tmp_p2_wins * ct
        return p1_wins, p2_wins

    return max(compute_wins(p1, 0, p2, 0))


def test(input_data: str) -> None:
    assert compute(input_data) == 444356092776315


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
