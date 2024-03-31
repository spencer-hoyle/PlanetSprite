import random

from gameplay.fish import Fish
from gameplay.fish import FISH_TIERS
from gameplay.fish import get_fish_pools
from gameplay.fish import get_fish_pool
from gameplay.fish import spawn_fish
from gameplay.rod import Rod
from gameplay.bait import Bait
from gameplay.game import get_weather
from gameplay.level import STARTING_XP
from gameplay.level import MAX_XP

CAST_LINE_TIMER = 1
FISH_MOVE_TIMER = 0.2

MIN_DELAY_BEFORE_ATTEMPTING_ANOTHER_BITE = 2
MAX_DELAY_BEFORE_ATTEMPTING_ANOTHER_BITE = 4
DELAY_FISH_BITE_TIMER = 1

IDLE_FISHING_TIMER = 0.2
PROGRESS_BAR_START = 10
PROGRESS_BAR_MIN = 0
PROGRESS_BAR_MAX = 100
BREAK_FAIL_ATTEMPT_PROGRESS_ADDITION = 10
BREAK_SUCCESS_ATTEMPT_PROGRESS_DEDUCTION = 10

FISH_CAUGHT_TIMER = 1
FISH_DISAPPEAR_PROBABILITY = 0.5

def simulate_fish_attempt(fish: Fish, rod: Rod, bait: Bait):
    """
    Simulate a single player fishing, given a fish is near

    Returns:
        caught (boolean) - Whether or not the fish was caught
        time (int) - Number of seconds it took to fish
    """
    time = 0

    # cast line
    time += CAST_LINE_TIMER

    # fish moves to bait
    time += FISH_MOVE_TIMER

    # loop until fish bites
    fish_bite_odds = min(fish.catch_rate + rod.catch_booster + bait.get_catch_booster(fish), 1)
    while random.random() > fish_bite_odds:
        time += round(random.uniform(MIN_DELAY_BEFORE_ATTEMPTING_ANOTHER_BITE, MAX_DELAY_BEFORE_ATTEMPTING_ANOTHER_BITE),1)

    # fish bites
    time += DELAY_FISH_BITE_TIMER

    # idle fishing game
    progress_bar = PROGRESS_BAR_START
    break_rate = max(fish.break_rate + rod.break_booster, 0)

    while progress_bar > PROGRESS_BAR_MIN and progress_bar < PROGRESS_BAR_MAX:
        time += IDLE_FISHING_TIMER
        
        if random.random() > break_rate:
            progress_bar += BREAK_FAIL_ATTEMPT_PROGRESS_ADDITION
        else:
            progress_bar -= BREAK_SUCCESS_ATTEMPT_PROGRESS_DEDUCTION

        # did fish get caught?
        caught = progress_bar >= PROGRESS_BAR_MAX
        if caught:
            time += FISH_CAUGHT_TIMER
        
    return caught, time

def simulate_biome_season(fish_list, biome, season, rod, bait):
    """
    Simulates fishing experience for a single biome and season, for a given rod and bait.
    Ends when player reaches max level

    Returns:
        hours (float) - Number of hours the simulation took
        xp_per_hour (int) - XP per hour gained
        gold_per_hour (int) - Gold per hour gained
        fish_tiers (dict) - Number of fish caught per tier
    """
    assert isinstance(rod, Rod), f"{rod} must be a Rod object"
    assert isinstance(bait, Bait), f"{bait} must be a Bait object"

    fish_tiers = {tier: 0 for tier in FISH_TIERS}
    time_of_day = 'Day'
    weather = get_weather(season)
    fish_pools = get_fish_pools(fish_list)
    fish_pool = get_fish_pool(fish_pools, biome, season, weather, time_of_day)
    fish = None
    xp = STARTING_XP
    gold = 0
    days = 0
    seconds = 0

    while xp < MAX_XP:

        # spawn fish if it doesn't exist
        if fish is None:
            fish = spawn_fish(fish_pool, bait)
            

        caught, time_to_fish = simulate_fish_attempt(fish, rod, bait)
        
        if caught:
            xp += fish.xp
            gold += fish.gold_value
            fish_tiers[fish.tier] += 1
            fish = None

        else:
            if random.random() <= FISH_DISAPPEAR_PROBABILITY:
                fish = None

        # change time of day and weather
        seconds += time_to_fish
        if seconds >= 900:
            time_of_day = 'Night'
            fish_pool = fish_pool = get_fish_pool(fish_pools, biome, season, weather, time_of_day)

        if seconds >= 1800:
            time_of_day = 'Day'
            seconds -= 1800
            days += 1
            weather = get_weather(season)
            fish_pool = get_fish_pool(fish_pools, biome, season, weather, time_of_day)

    total_seconds = days * 1800 + seconds
    hours = round(total_seconds / 60 / 60, 2)
    xp_per_hour = round(xp/hours)
    gold_per_hour = round(gold/hours)
    return hours, xp_per_hour, gold_per_hour, fish_tiers