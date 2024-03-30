import pandas as pd
from game import BIOMES, SEASONS, WEATHER, TIME_OF_DAY

"""
Fish Pool = list of fish that are available to catch for a given biome, season, weather, time of day
"""

FISH_TIERS = [
    "Common",
    "Uncommon",
    "Rare",
    "Epic",
    "Legendary"
]


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

class FishList:

    def __init__(self, path = None):
        self.fish = []
        if path:
            self.get_fish_list(path)
    
    def get_fish_list(self, path):
        df = pd.read_csv(path)
        tiers = [0] * len(FISH_TIERS)



        for id, row in df.iterrows():
            self.fish.append(
                Fish(
                    id = row['ID'] + '-' + row['Tier'][0],
                    tier = row['Tier'],
                    biome = row['Biome'],
                    seasons = [seasons for seasons in  row['Seasons'].split(',')],
                    weather = [weather for weather in  row['Weather'].split(',')],
                    time_of_day = [time_of_day for time_of_day in  row['Time of Day'].split(',')],
                )
            )

    def get_fish_pool(self, biome, season, weather, time_of_day):
        fish_pool = []
        for fish in self.fish:
            if (fish.biome == biome and
                season in fish.seasons and 
                weather in fish.weather and 
                time_of_day in fish.time_of_day):
                fish_pool.append(fish)

        return fish_pool
    
    def to_df(self):
        column_mapping = {
            'id': 'Name',
            'tier': 'Tier',
            'biome': 'Biome',
            'seasons': 'Seasons',
            'weather': 'Weather',
            'time_of_day': 'Time of Day',
            'xp': 'XP',
            'common_rate': 'Common Rate',
            'catch_rate': 'Catch Rate',
            'break_rate': 'Break Rate',
            'gold_value': 'Gold Value'
        }
        columns = list(column_mapping.keys())
        fish_data = {attr: [getattr(fish, attr) for fish in self.fish] for attr in columns}
        df = pd.DataFrame(fish_data)

        for column in ['break_rate', 'catch_rate', 'common_rate']:
            df[column] = df[column].map(lambda x: '{:.0%}'.format(x))

        df = df.rename(columns=column_mapping)

        return df