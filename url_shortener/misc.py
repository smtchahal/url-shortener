import string

ALPHA_MAP = list(string.ascii_letters + string.digits)
BASE = len(ALPHA_MAP)


def id_to_alias(num):
    digits = []
    while num:
        remainder = num % BASE
        digits.append(remainder)
        num = num // BASE
    digits = digits[::-1]
    return ''.join([ALPHA_MAP[i] for i in digits])


def alias_to_id(alias):
    digits = [ALPHA_MAP.index(c) for c in alias][::-1]
    num = 0
    for i in range(len(digits)):
        num += digits[i] * BASE**i
    return num
