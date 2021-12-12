from __future__ import annotations
import argparse
from pathlib import Path
from typing import Optional, Union
from statistics import mode

import pytest
from support import timing

INPUT_TXT = Path(__file__).parent.joinpath('input.txt')


def convert_esp_map(number: str):
    convert_map = {
        "1": "0",
        "0": "1"
    }
    return convert_map.get(number)


def compute(s: Union[list[str], str], testing: Optional[bool] = None) -> int:
    result_gamma = ''
    result_esp = ''
    lines = s if testing else s.splitlines()
    matrix = [list(s) for s in lines]
    column = [str(mode([int(row[i]) for row in matrix])) for i in range(len(lines[0]))]
    result_gamma = result_gamma.join(column)
    result_esp = result_esp.join([convert_esp_map(x) for x in result_gamma])

    return int(result_gamma, 2) * int(result_esp, 2)


def test(input_data) -> None:
    assert compute(input_data, testing=True) == 198


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
