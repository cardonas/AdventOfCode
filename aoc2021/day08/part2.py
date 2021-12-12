from __future__ import annotations
import argparse
from pathlib import Path
from typing import Optional, Union

import pytest
from support import timing

INPUT_TXT = Path(__file__).parent.joinpath('input.txt')


# TODO: Clean up code to be more readable adn make sense.
def compute(s: Union[list[str], str], testing: Optional[bool] = None) -> int:
    lines = s if testing and type(s) == list[str] else s.splitlines()
    total = 0
    for line in lines:
        start, end = line.split(' | ')
        sorted_end = [''.join(sorted(part)) for part in end.split()]
        digits = {*start.split(), *sorted_end}
        digits = {''.join(sorted(part)) for part in digits}
        one, = (s for s in digits if len(s) == 2)
        seven, = (s for s in digits if len(s) == 3)
        four, = (s for s in digits if len(s) == 4)
        eight, = (s for s in digits if len(s) == 7)
        six, = (s for s in digits if len(s) == 6 and len(set(s) & set(one)) == 1)
        r_top, = set(eight) - set(six)
        r_bot, = set(one) - set(r_top)
        five, = (s for s in digits if len(s) == 5 and r_top not in s)
        two, = (s for s in digits if len(s) == 5 and r_bot not in s)
        l_top, = set(eight) - set(two) - set(r_bot)
        nine = ''.join(sorted(str(s) for s in set.union(set(five), set(r_top))))
        three = ''.join(sorted(str(s) for s in set(nine) - set(l_top)))
        middle = ''.join(sorted(str(s) for s in set(four) - set(one) - set(l_top)))
        zero = ''.join(sorted(str(s) for s in set(eight) - set(middle)))

        digits = {
            zero: 0,
            one: 1,
            two: 2,
            three: 3,
            four: 4,
            five: 5,
            six: 6,
            seven: 7,
            eight: 8,
            nine: 9
        }

        total += sum(10 ** (3 - i) * digits[sorted_end[i]] for i in range(4))

    return total


def test(input_data) -> None:
    assert compute(input_data, testing=True) == 61229


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))


if __name__ == '__main__':
    raise SystemExit(main())
