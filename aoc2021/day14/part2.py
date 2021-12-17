from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")


def compute(s: str) -> int:
    start, lines = s.split("\n\n")

    counts: Counter[str] = Counter()
    for i in range(len(start) - 1):
        counts[start[i : i + 2]] += 1

    pattern = {}
    for line in lines.splitlines():
        pair, between = line.split(" -> ")
        pattern[pair] = between

    for _ in range(40):
        counts_2: Counter[str] = Counter()
        new_counts: Counter[str] = Counter()
        for k, v in counts.items():
            new_counts[f"{k[0]}{pattern[k]}"] += v
            new_counts[f"{pattern[k]}{k[1]}"] += v
            counts_2[k[0]] += v
            counts_2[pattern[k]] += v
        counts = new_counts

    counts_2[start[-1]] += 1
    s_counts = sorted(iter(counts_2.values()))
    return s_counts[-1] - s_counts[0]


def test(input_data: str) -> None:
    assert compute(input_data) == 2188189693529


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
