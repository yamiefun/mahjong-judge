from judge import judge_ryuiso
from collections import defaultdict
from ryuiso_checker import RyuisoChecker


def main():
    # sea = defaultdict(int)
    # hand = defaultdict(int)

    ryuiso = RyuisoChecker()
    while True:
        val = input("Input: ")
        ryuiso.parse_input(val)


if __name__ == "__main__":
    main()
