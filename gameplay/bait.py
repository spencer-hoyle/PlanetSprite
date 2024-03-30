import pandas as pd

from gameplay.fish import Fish

class Bait:
    def __init__(self, id, fish_list, catch_booster, common_booster):
        assert isinstance(fish_list, list) and all(isinstance(fish, Fish) for fish in fish_list)
        assert catch_booster <= 1 and catch_booster >= 0
        assert common_booster <= 1 and common_booster >= 0
        
        self.id = id
        self.fish_list = fish_list
        self.catch_booster = catch_booster
        self.common_booster = common_booster

    def get_catch_booster(self, fish):
        return self.catch_booster if fish in bait.fish_list else 0