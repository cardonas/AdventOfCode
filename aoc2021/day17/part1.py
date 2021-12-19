from __future__ import annotations

import argparse
from pathlib import Path

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")


def compute(s: str) -> int:
    _, _, x, y = s.split()
    x = x[2:-1]
    y = y[2:]
    y1, _ = y.split("..")
    y0 = abs(int(y1)) - 1

    return y0 * y0 - (y0 - 1) * y0 // 2


def test(input_data: str) -> None:
    assert compute(input_data) == 45


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
