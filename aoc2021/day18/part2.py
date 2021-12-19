from __future__ import annotations

import argparse
import ast
import math
import re
from pathlib import Path
from typing import Any
from typing import Match

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")

PAIR_RE = re.compile(r"\[(\d+),(\d+)\]")
NUM_LEFT_RE = re.compile(r"\d+(?!.*\d)")
NUM_RE = re.compile(r"\d+")
GT_10 = re.compile(r"\d\d+")


def add_number(s1: str, s2: str) -> str:
    return f"[{s1},{s2}]"


def reduce_number(s: str) -> str:
    while True:
        continue_outer = False
        for pair in PAIR_RE.finditer(s):
            before = s[: pair.start()]
            if before.count("[") - before.count("]") >= 4:

                def left_cb(match: Match[str]) -> str:
                    return str(int(match[0]) + int(pair[1]))

                def right_cb(match: Match[str]) -> str:
                    return str(int(match[0]) + int(pair[2]))

                start = NUM_LEFT_RE.sub(left_cb, s[: pair.start()], count=1)
                end = NUM_RE.sub(right_cb, s[pair.end() :], count=1)
                s = f"{start}0{end}"

                continue_outer = True
                break

        if continue_outer:
            continue

        gt_10_match = GT_10.search(s)
        if gt_10_match:

            def match_cb(match: Match[str]) -> str:
                val = int(match[0])
                return f"[{math.floor(val / 2)},{math.ceil(val / 2)}]"

            s = GT_10.sub(match_cb, s, count=1)
            continue

        return s


def compute_sum(s: str) -> int:
    def compute_val(v: int | Any) -> int:
        if isinstance(v, int):
            return v
        else:
            assert len(v) == 2
            return 3 * compute_val(v[0]) + 2 * compute_val(v[1])

    return compute_val(ast.literal_eval(s))


def compute(s: str) -> int:
    lines = s.splitlines()

    maximum = 0
    for i, line in enumerate(lines):
        for other in lines[i + 1 :]:
            maximum = max(
                maximum,
                compute_sum(reduce_number(add_number(line, other))),
            )
            maximum = max(
                maximum,
                compute_sum(reduce_number(add_number(other, line))),
            )

    return maximum


def test(input_data: str) -> None:
    assert compute(input_data) == 3993


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
