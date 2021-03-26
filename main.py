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
        # if val[0] == 'r':
        #     sea, hand = defaultdict(int), defaultdict(int)
        # elif val[0] == 's':
        #     sea[val[2]] += 1
        # elif val[0] == 'h':
        #     hand[val[2]] += 1
        # else:
        #     print("Not legal input.")
        #     continue
        # print("Sea: ", sea)
        # print("Hand:", hand)
        

if __name__ == "__main__":
    main()