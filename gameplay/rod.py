import pandas as pd

ROD_TIERS = ["Default", "Bronze", "Iron", "Silver", "Gold"]

class Rod:
    def __init__(self, id, tier, catch_booster, break_booster):
        assert tier in ROD_TIERS
        assert catch_booster <= 1 and catch_booster >= 0
        assert break_booster <= 1 and break_booster >= 0

        self.id = id
        self.tier = tier
        self.catch_booster = catch_booster
        self.break_booster = break_booster

