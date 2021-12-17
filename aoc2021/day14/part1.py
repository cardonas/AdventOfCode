from __future__ import annotations

import argparse
from pathlib import Path

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")


def compute(s: str) -> int:
    start, lines = s.split("\n\n")

    pattern = {}
    for line in lines.splitlines():
        pair, between = line.split(" -> ")
        pattern[pair] = between

    for _ in range(10):
        next_str: list[str] = []
        for j, c in enumerate(start):
            cand = start[j : j + 2]
            if cand in pattern:
                next_str.extend((c, pattern[cand]))
            else:
                next_str.append(c)
        start = "".join(next_str)

    counts = {k: start.count(k) for k in set(pattern.values())}
    s_counts = sorted(v for k, v in counts.items())
    return s_counts[-1] - s_counts[0]


def test(input_data: str) -> None:
    assert compute(input_data) == 1588


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
