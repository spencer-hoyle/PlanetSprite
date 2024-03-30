import random
import csv
import pandas as pd

from game import WEATHER
from game import WEATHER_PROBABILITY
from fish import Fish
from fish import FishList
from bait import Bait
from bait import get_catch_booster
from rod import Rod

MAX_LEVEL = 100

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

def spawn_fish(fish_pool):
    spawn_weights = [f.common_rate for f in fish_pool]
    return random.choices(fish_pool, weights = spawn_weights)[0]

def get_weather(season):
    weights = WEATHER_PROBABILITY.get(season)
    weather = random.choices(WEATHER, weights=weights)
    return weather[0]

def simulate_fish_attempt(fish: Fish, rod: Rod, bait: Bait):
    time_to_fish = 0

    # cast line
    time_to_fish += CAST_LINE_TIMER

    # fish moves to bait
    time_to_fish += FISH_MOVE_TIMER

    # loop until fish bites
    fish_bite_odds = fish.catch_rate + rod.catch_booster + get_catch_booster(fish, bait)
    while random.random() > fish_bite_odds:
        time_to_fish += round(random.uniform(MIN_DELAY_BEFORE_ATTEMPTING_ANOTHER_BITE, MAX_DELAY_BEFORE_ATTEMPTING_ANOTHER_BITE),1)

    # fish bites
    time_to_fish += DELAY_FISH_BITE_TIMER

    # idle fishing game
    progress_bar = PROGRESS_BAR_START
    break_rate = fish.break_rate + rod.break_booster

    while progress_bar > PROGRESS_BAR_MIN and progress_bar < PROGRESS_BAR_MAX:
        time_to_fish += IDLE_FISHING_TIMER
        
        if random.random() > break_rate:
            progress_bar += BREAK_FAIL_ATTEMPT_PROGRESS_ADDITION
        else:
            progress_bar -= BREAK_SUCCESS_ATTEMPT_PROGRESS_DEDUCTION

        # did fish get caught?
        caught = progress_bar >= PROGRESS_BAR_MAX
        if caught:
            time_to_fish += FISH_CAUGHT_TIMER
        
    return caught, time_to_fish

def simulate(biome, season, rod, bait):
    time_of_day = 'Day'
    weather = get_weather(season)

    fish_list = FishList('data/fish.csv')
    fish_pool = fish_list.get_fish_pool(biome, season, weather, time_of_day)
    fish = None
    xp = 0
    gold = 0
    days = 0
    seconds = 0

    while xp < MAX_LEVEL:

        if fish is None:
            fish = spawn_fish(fish_pool)

        caught, time_to_fish = simulate_fish_attempt(fish, rod, bait)
        
        if caught:
            xp += fish.xp
            gold += fish.gold

        # change time of day and weather
        seconds += time_to_fish
        if seconds >= 900:
            time_of_day = 'Night'
            fish_pool = fish_pool = fish_list.get_fish_pool(biome, season, weather, time_of_day)
        if seconds >= 1800:
            time_of_day = 'Day'
            seconds -= 1800
            days += 1
            weather = get_weather(season)
            fish_pool = fish_list.get_fish_pool(biome, season, weather, time_of_day)

    total_seconds = days * 1800 + seconds
    print(xp)
    hours = round(total_seconds / 60 / 60, 2)
    xp_per_hour = round(xp/hours)
    gold_per_hour = round(gold/hours)
    return xp_per_hour, gold_per_hour
