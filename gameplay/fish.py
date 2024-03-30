import random
import pandas as pd

from gameplay.game import BIOMES
from gameplay.game import SEASONS
from gameplay.game import WEATHER
from gameplay.game import TIME_OF_DAY

FISH_TIERS = ["Common", "Uncommon", "Rare", "Epic", "Legendary"]

class Fish:
    def __init__(self, id, tier, biome, seasons, weather, time_of_day):
        assert biome in BIOMES
        for season in seasons:
            assert season in SEASONS,  f"{season}"
        for w in weather:
            assert w in WEATHER,  f"{w}"
        for t in time_of_day:
            assert t in TIME_OF_DAY,  f"{t}"
        self.id = id
        self.tier = tier
        self.biome = biome
        self.seasons = seasons
        self.weather = weather
        self.time_of_day = time_of_day
        self.calculate_attributes()

    def calculate_attributes(self):
        tier_baseline = {
            "Common":       {"xp": 100, "catch_rate": 0.80, "break_rate": 0.05, "common_rate": 0.90, "gold_value": 100},
            "Uncommon":     {"xp": 150, "catch_rate": 0.60, "break_rate": 0.10, "common_rate": 0.75, "gold_value": 150},
            "Rare":         {"xp": 200, "catch_rate": 0.50, "break_rate": 0.15, "common_rate": 0.50, "gold_value": 200},
            "Epic":         {"xp": 300, "catch_rate": 0.35, "break_rate": 0.20, "common_rate": 0.40, "gold_value": 400},
            "Legendary":    {"xp": 500, "catch_rate": 0.20, "break_rate": 0.25, "common_rate": 0.30, "gold_value": 800}
        }

        biome_boost = {
            "Small Water Area": {"xp": 0,   "catch_rate":  0.00, "break_rate":  0.00, "common_rate":  0.00, "gold_value":  0.00},
            "Beach":            {"xp": 10,  "catch_rate":  0.05, "break_rate": -0.02, "common_rate":  0.02, "gold_value":  0.05},
            "Desert":           {"xp": 100, "catch_rate": -0.10, "break_rate":  0.02, "common_rate": -0.05, "gold_value":  0.20},
            "Cave (Leafy)":     {"xp": 25,  "catch_rate":  0.05, "break_rate":  0.05, "common_rate":  0.02, "gold_value": -0.05},
            "Cave (Ice)":       {"xp": 25,  "catch_rate":  0.05, "break_rate":  0.05, "common_rate":  0.02, "gold_value": -0.05},
            "Cave (Lava)":      {"xp": 50,  "catch_rate": -0.05, "break_rate":  0.02, "common_rate": -0.03, "gold_value":  0.10},
            "Cave (Ash)":       {"xp": 50,  "catch_rate": -0.05, "break_rate":  0.02, "common_rate": -0.03, "gold_value":  0.10}
        }

        assert self.tier in tier_baseline
        assert self.biome in biome_boost

        baseline = tier_baseline[self.tier]
        boost = biome_boost[self.biome]

        self.xp = int(baseline['xp'] + boost['xp'])
        self.catch_rate = round(baseline['catch_rate'] + boost['catch_rate'],2)
        self.break_rate = round(baseline['break_rate'] + boost['break_rate'],2)
        self.common_rate = round(baseline['common_rate'] + boost['common_rate'],2)
        self.gold_value = int(baseline['gold_value'] * (1 + boost['gold_value']))

def get_fish_pool(fish_list, biome, season, weather, time_of_day)
    assert isinstance(fish_list, list) and all(isinstance(fish, Fish) for fish in fish_list)
    fish_pool = []
    for fish in self.fish:
        if (fish.biome == biome and
            season in fish.seasons and 
            weather in fish.weather and 
            time_of_day in fish.time_of_day):
            fish_pool.append(fish)

    return fish_pool

def spawn_fish(fish_list):
    assert isinstance(fish_list, list) and all(isinstance(fish, Fish) for fish in fish_list)
    spawn_weights = [f.common_rate for f in fish_list]
    fish = random.choices(fish_list, weights = spawn_weights)
    return fish[0]