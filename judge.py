from collections import Counter


def judge_ryuiso(cards):
    """
    input -> str: the card set need to be reviewed
    output -> bool: ryuiso is satisfied or not.
    """
    return check_card(cards) and check_combination(cards)


def check_card(cards):
    """Check if all cards are in ryuiso card set."""
    legal_card = {'2', '3', '4', '6', '8', 'f'}
    return all(c in legal_card for c in cards)


def check_combination(cards):
    """
    Check if cards set is a legal combination for win.
    input -> str: the card set need to be reviewed
    output -> bool: legal or not
    """
    if len(cards) != 14:
        return False
    card_count = Counter(cards)
    legal_eyes = extract_eyes(card_count)
    if not legal_eyes:
        return False
    for eyes in legal_eyes:
        tmp = card_count.copy()
        tmp[eyes] -= 2
        if tmp[eyes] == 0:
            tmp.pop(eyes, None)
        if check_combination_without_eyes(tmp):
            return True
    return False


def check_combination_without_eyes(card_count):
    """
    Check if a card set exclude eyes is legal or not.
    input: -> dict: {card point: number of the card}
    output -> bool: legal or not
    """
    key_list = sorted(list(card_count.keys()))
    # if nothing left in card set, is legal
    if not card_count:
        return True

    # check by recursive
    # remove smallest Triplet
    if card_count[key_list[0]] >= 3:
        tmp = card_count
        tmp[key_list[0]] -= 3
        if tmp[key_list[0]] == 0:
            tmp.pop(key_list[0], None)
        return check_combination_without_eyes(tmp)

    # remove smallest Sequence
    elif len(key_list) >= 3 and\
            card_count[key_list[0]] > 0 and\
            card_count[key_list[1]] > 0 and\
            card_count[key_list[2]] > 0 and\
            key_list[1] == str(int(key_list[0])+1) and\
            key_list[2] == str(int(key_list[1])+1):
        tmp = card_count
        tmp[key_list[0]] -= 1
        tmp[key_list[1]] -= 1
        tmp[key_list[2]] -= 1
        for i in range(3):
            if tmp[key_list[i]] == 0:
                tmp.pop(key_list[i], None)
        return check_combination_without_eyes(tmp)
    else:
        return False


def extract_eyes(card_count):
    """
    input -> dict: {card point: number of the card}
    output -> list of str: legal eyes
    """
    legal_eyes = []
    for key in card_count:
        if card_count[key] >= 2:
            legal_eyes.append(key)
    legal_eyes.sort()
    return legal_eyes


if __name__ == "__main__":
    hand = "233334666888ff"
    print(judge_ryuiso(hand))
