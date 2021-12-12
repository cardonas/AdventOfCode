from __future__ import annotations
import argparse
import statistics
from collections import Counter
from pathlib import Path
from typing import Optional, Union

import pytest
from support import timing

INPUT_TXT = Path(__file__).parent.joinpath('input.txt')


def get_bracket_score(bracket: str) -> int:
    bracket_map = {
        ')': 1,
        ']': 2,
        '}': 3,
        '>': 4
    }
    return bracket_map.get(bracket)


def compute(s: Union[list[str], str], testing: Optional[bool] = None) -> int:
    lines = s if testing and type(s) == list[str] else s.splitlines()
    counter = Counter({')': 0, ']': 0, '}': 0, '>': 0})
    forward_brackets = {'(': ')', '[': ']', '{': '}', '<': '>'}
    reversed_brackets = {v: k for k, v in forward_brackets.items()}
    reversed_left_overs = []
    totals = []
    for line in lines:
        bracket_stack = []
        corrupted = False
        for c in line:
            if c in forward_brackets:
                bracket_stack.append(c)
            elif c in reversed_brackets:
                if reversed_brackets[c] == bracket_stack[-1]:
                    bracket_stack.pop()
                else:
                    corrupted = True
                    break
        if not corrupted:
            bracket_stack.reverse()
            reversed_left_overs.append([forward_brackets.get(c) for c in bracket_stack])

    for left_over in reversed_left_overs:
        total = 0
        for c in left_over:
            total *= 5
            total += get_bracket_score(c)
        totals.append(total)
    return statistics.median(totals)


def test(input_data) -> None:
    assert compute(input_data, testing=True) == 288957


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
