from __future__ import annotations
import argparse
from pathlib import Path
import pytest
from support import timing

INPUT_TXT = Path(__file__).parent.joinpath('input.txt')


def compute(s: str) -> int:
    numbers = [int(line) for line in s.splitlines()]
    for _ in numbers:
        pass

    lines = s.splitlines()
    for line in lines:
        pass
    # TODO: implement solution here!
    return 0


INPUT_S = '''\

'''


@pytest.mark.parametrize(
    'input_s', 'expected', (
            (INPUT_S, 1)
    )
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', defult=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
