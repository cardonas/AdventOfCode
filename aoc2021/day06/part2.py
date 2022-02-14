from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import Optional, Union

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")


def compute(s: Union[list[str], str], days: int, testing: Optional[bool] = None) -> int:
    lines = s if testing and type(s) == list[str] else s.split(",")

    counts = Counter([int(x) for x in lines])
    for _ in range(days):
        counts2 = Counter({6: counts[0], 8: counts[0]})
        counts2.update({k - 1: v for k, v in counts.items() if k > 0})
        counts = counts2
    return sum(counts.values())


def test(input_data) -> None:
    assert compute(input_data, 256, testing=True) == 26984457539


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read(), 256))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
