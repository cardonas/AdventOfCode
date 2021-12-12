from __future__ import annotations

import argparse
from collections import defaultdict
from collections import deque
from pathlib import Path

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath('input.txt')


def compute(s: str) -> int:
    edges = defaultdict(set)
    lines = s.splitlines()
    for line in lines:
        start, end = line.split('-')
        edges[start].add(end)
        edges[end].add(start)

    done = set()

    todo: deque[tuple[str, ...]]
    todo = deque([('start',)])
    while todo:
        path = todo.popleft()
        if path[-1] == 'end':
            done.add(path)
            continue
        for path_choice in edges[path[-1]]:
            if path_choice.isupper() or path_choice not in path:
                todo.append((*path, path_choice))

    return len(done)


def test(input_data: str) -> None:
    assert compute(input_data) == 10


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
