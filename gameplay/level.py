STARTING_LEVEL = 1
MAX_LEVEL = 100

STARTING_XP = 0
NEXT_LEVEL_XP = 100
NEXT_LEVEL_XP_PERCENT_ADDITION = 0.1

def get_xp(level):
    assert level >= STARTING_LEVEL and level <= MAX_LEVEL
    if level == STARTING_LEVEL:
        return STARTING_LEVEL
    return int(NEXT_LEVEL_XP * (1 + NEXT_LEVEL_XP_PERCENT_ADDITION)**(level-1))

MAX_XP = get_xp(MAX_LEVEL)