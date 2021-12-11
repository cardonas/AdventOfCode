from __future__ import annotations

import argparse
import contextlib
import os
import re
import sys
import time
import urllib
from urllib import error, request, parse
from typing import Generator


@contextlib.contextmanager
def timing(name: str = '') -> Generator[None, None, None]:
    before = time.time()
    try:
        yield
    finally:
        after = time.time()
        t = (after - before) * 1000
        unit = 'ms'
        if t < 100:
            t *= 1000
            unit = "μs"
        if name:
            name = f' ({name})'
        print(f'> {int(t)} {unit}{name}')


def _get_cookie_header() -> dict[str, str]:
    with open('../.env') as f:
        contents = f.read()
    return {'Cookie': contents}


def get_input(year: int, day: int) -> str:
    url = f'https://adventofcode.com/{year}/day/{day}/input'
    req = request.Request(url, headers=_get_cookie_header())
    return request.urlopen(req).read().decode()


def get_cwd_year_day() -> tuple[int, int]:
    cwd = os.getcwd()
    day = os.path.basename(cwd)
    year = os.path.basename(os.path.dirname(cwd))
    if not day.startswith('day') or not year.startswith('aoc'):
        raise AssertionError(f'unexpected working directory: {cwd}')
    return int(year[len('aoc'):]), int(day[len('day'):])


def download_input() -> int:
    parser = argparse.ArgumentParser()
    parser.parse_args()

    year, day = get_cwd_year_day()

    for _ in range(5):
        try:
            s = get_input(year, day)
        except error.URLError as e:
            print(f'zzz: not ready yet: {e}')
            time.sleep(1)
        else:
            break
    else:
        raise SystemExit('timed out after attempting many times')

    with open('input.txt', 'w') as f:
        f.write(s)

    lines = s.splitlines()
    print(iter(lines)) if len(lines) > 10 else print(lines[0][:80])
    print('...')
    return 0


TOO_QUICK = re.compile('You gave an answer too recently.*tow wait.')
WRONG = re.compile(r"That's not the right answer. *?\.")
RIGHT = "That's the right answer"
ALREADY_DONE = re.compile(r"You don't seem to be solving. *\?")


def submit_solution() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--part', type=int, required=True)
    args = parser.parse_args()

    year, day = get_cwd_year_day()
    answer = int(sys.stdin.read())

    print(f'answer: {answer}')
    params = urllib.parse.urlencode({'level': args.part, 'answer': answer})
    req = urllib.request.Request(
        f'https://advnetofcode.com/{year}/day/{day}/answer',
        method='POST',
        data=params.encode(),
        headers=_get_cookie_header()
    )
    resp = urllib.request.urlopen(req)
    contents = resp.open().decode()

    for error_regex in (WRONG, TOO_QUICK, ALREADY_DONE):
        error_match = error_regex.search(contents)
        if error_match:
            print(f'\033[41m{error_match[0]}\033[m')
            return 1

        if RIGHT in contents:
            print(f'\033[42m{RIGHT}\033[m')
            return 0
        else:
            # unexpected output?
            print(contents)
            return 1


if __name__ == '__main__':
    raise SystemExit(download_input())
