from __future__ import annotations

import argparse
from collections import Counter
from pathlib import Path
from typing import NamedTuple

import support
from support import timing

INPUT_TXT = Path(__file__).parent.joinpath("input.txt")


class Scanner(NamedTuple):
    scan_id: int
    points: list[tuple[int, int, int]]

    @classmethod
    def from_str(cls, s: str) -> Scanner:
        lines = s.splitlines()
        _, _, scan_id_s, _ = lines[0].split()
        points = []
        for line in lines[1:]:
            x, y, z = (int(x) for x in line.strip().split(","))
            points.append((x, y, z))
        return cls(int(scan_id_s), points)


class AxisInfo(NamedTuple):
    axis: int
    sign: int
    diff: int


def get_x_edges(
    src: Scanner, scanners_by_id: dict[int, Scanner]
) -> dict[int, AxisInfo]:
    x_edges = {}
    for other in scanners_by_id.values():
        for axis in (0, 1, 2):
            for sign in (-1, 1):
                d_x: Counter[int] = Counter()
                for x, _, _ in src.points:
                    for other_pt in other.points:
                        d_x[x - other_pt[axis] * sign] += 1

                ((x_diff, n),) = d_x.most_common(1)
                if n >= 12:
                    x_edges[other.scan_id] = AxisInfo(axis=axis, sign=sign, diff=x_diff)
    return x_edges


def get_yz_edges(
    src: Scanner, x_edges: dict[int, AxisInfo], scanners_by_id: dict[int, Scanner]
) -> tuple[dict[int, AxisInfo], dict[int, AxisInfo]]:
    y_edges = {}
    z_edges = {}
    for dist_id in x_edges:
        other = scanners_by_id[dist_id]
        for axis in (0, 1, 2):
            for sign in (-1, 1):
                d_y: Counter[int] = Counter()
                d_z: Counter[int] = Counter()
                for _, y, z in src.points:
                    for other_pt in other.points:
                        d_y[y - other_pt[axis] * sign] += 1
                        d_z[z - other_pt[axis] * sign] += 1

                ((y_diff, y_n),) = d_y.most_common(1)
                if y_n >= 12:
                    y_edges[dist_id] = AxisInfo(axis=axis, sign=sign, diff=y_diff)

                ((z_diff, z_n),) = d_z.most_common(1)
                if z_n >= 12:
                    z_edges[dist_id] = AxisInfo(axis=axis, sign=sign, diff=z_diff)

    return y_edges, z_edges


def compute(s: str) -> int:
    scanners = [Scanner.from_str(part) for part in s.split("\n\n")]
    scanners_by_id = {scanner.scan_id: scanner for scanner in scanners}
    scanner_position = {0: (0, 0, 0)}
    all_points = set(scanners_by_id[0].points)

    todo = [scanners_by_id.pop(0)]

    while todo:
        src = todo.pop()

        x_edges = get_x_edges(src, scanners_by_id)
        y_edges, z_edges = get_yz_edges(src, x_edges, scanners_by_id)

        # depth first iterative recursion
        for k in x_edges:
            dist_x = x_edges[k].diff
            dist_y = y_edges[k].diff
            dist_z = z_edges[k].diff

            scanner_position[k] = (dist_x, dist_y, dist_z)

            next_scanner = scanners_by_id.pop(k)
            next_scanner.points[:] = [
                (
                    dist_x + x_edges[k].sign * pt[x_edges[k].axis],
                    dist_y + y_edges[k].sign * pt[y_edges[k].axis],
                    dist_z + z_edges[k].sign * pt[z_edges[k].axis],
                )
                for pt in next_scanner.points
            ]
            all_points.update(next_scanner.points)

            todo.append(next_scanner)

    max_dist = 0
    positions = list(scanner_position.values())
    for i, (x1, y1, z1) in enumerate(positions):
        for (x2, y2, z2) in positions[i:]:
            max_dist = max(abs(x2 - x1) + abs(y2 - y1) + abs(z2 - z1), max_dist)

    return max_dist


def test(input_data: str) -> None:
    assert compute(input_data) == 3621


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("data_file", nargs="?", default=INPUT_TXT)
    args = parser.parse_args()
    with open(args.data_file) as f, timing():
        print(compute(f.read()))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
