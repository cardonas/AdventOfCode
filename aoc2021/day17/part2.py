from __future__ import annotations

import argparse
from pathlib import Path

from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")


def compute(s: str) -> int:
    _, _, x_s, y_s = s.split()
    x_s = x_s[2:-1]
    y_s = y_s[2:]

    x1_s, x2_s = x_s.split("..")
    y1_s, y2_s = y_s.split("..")

    x1, x2 = int(x1_s), int(x2_s)
    y1, y2 = int(y1_s), int(y2_s)

    total = 0
    for x in range(1, x2 + 1):
        for y in range(y1, abs(int(y1))):
            vx, vy = x, y
            x_p = y_p = 0
            for _ in range(2 * abs(int(y1)) + 1):
                x_p += vx
                y_p += vy
                vx = max(vx - 1, 0)
                vy -= 1

                if y1 <= y_p <= y2 and x1 <= x_p <= x2:
                    total += 1
                    break
                elif y_p < y1 or x_p > x2:
                    break

    return total


def test(input_data: str) -> None:
    assert compute(input_data) == 112


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
