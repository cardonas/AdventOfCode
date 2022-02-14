def parse_input() -> list[int]:
    with open("input.txt", "r") as f:
        return [int(x) for x in f.read().splitlines()]


def process_part1(inputs) -> int:
    count = 0
    for i, x in enumerate(inputs, start=1):
        try:
            if inputs[i] > x:
                count += 1
        except IndexError:
            continue
    return count


def process_part2(inputs):
    count = 0
    prev = 0
    for i, x in enumerate(inputs, start=2):
        try:
            current = inputs[i] + inputs[i - 1] + x
            if prev != 0 and prev < current:
                count += 1
            prev = current
        except IndexError:
            continue
    return count


def part2(inputs) -> int:
    return process_part2(inputs)


def part1(inputs) -> int:

    return process_part1(inputs)


def main(inputs):
    print(part1(inputs))
    print(part2(inputs))


if __name__ == "__main__":
    sample = False
    sample_inputs = [199, 200, 208, 210, 200, 207, 240, 269, 260, 263]
    inputs = sample_inputs if sample else parse_input()
    raise SystemExit(main(inputs))
