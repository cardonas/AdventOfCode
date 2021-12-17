from __future__ import annotations

import argparse
from pathlib import Path

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")


def compute(s: str) -> int:
    lines = s.splitlines()
    for line in lines:
        pass
    # TODO: implement solution here!
    return 0


def test(input_data: str) -> None:
    assert compute(input_data) == 150


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
