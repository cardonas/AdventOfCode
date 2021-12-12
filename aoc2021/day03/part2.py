from __future__ import annotations
import argparse
from pathlib import Path
from typing import Optional, Union
from statistics import multimode
from support import timing

INPUT_TXT = Path(__file__).parent.joinpath('input.txt')


def get_most_common(matrix, i):
    return str(max(multimode([row[i] for row in matrix])))


def get_least_common(matrix, i):
    col = [row[i] for row in matrix]
    modes = multimode(col)
    if len(modes) == 1 and modes == ['1']:
        return '0'
    elif len(modes) == 1 and modes == ['0']:
        return '1'
    elif len(modes) == 2 and (modes == ['0', '1'] or ['1', '0']):
        return '0'


def compute_ratings(matrix, rating_type: str):
    index = 0
    while index < len(matrix[0]) and len(matrix) > 1:
        mode_value = None
        if rating_type == 'oxy_gen':
            mode_value = get_most_common(matrix, index)
        elif rating_type == 'co2_scrub':
            mode_value = get_least_common(matrix, index)
        matrix = list(filter(lambda line: line[index] == mode_value, matrix))
        index += 1
    return ''.join(matrix[0])


def compute(s: Union[list[str], str], testing: Optional[bool] = None) -> int:
    co2_gen_rating = ''
    lines = s if testing else s.splitlines()
    matrix = [list(x) for x in lines]
    oxy_gen_rating = compute_ratings(matrix, 'oxy_gen')
    co2_scrub_rating = compute_ratings(matrix, 'co2_scrub')
    return int(oxy_gen_rating, 2) * int(co2_scrub_rating, 2)


def test(input_data) -> None:
    assert compute(input_data, testing=True) == 230


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
