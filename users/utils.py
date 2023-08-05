import math


def calculate_level(score: int) -> int:
    return math.ceil(math.log(1 + 0.005 * score, 1.5))
