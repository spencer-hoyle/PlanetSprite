import pandas as pd

ROD_TIERS = ["Default", "Bronze", "Iron", "Silver", "Gold"]

class Rod:
    def __init__(self, id, tier, catch_booster, break_booster):
        assert tier in ROD_TIERS
        assert catch_booster <= 1 and catch_booster >= -1
        assert break_booster <= 1 and break_booster >= -1

        self.id = id
        self.tier = tier
        self.catch_booster = catch_booster
        self.break_booster = break_booster

def get_rod_list(path):
    rod_list = []
    df = pd.read_csv(path)
    for idx, row in df.iterrows():
        rod = Rod(
            id = row['Rod'],
            tier= row['Tier'],
            catch_booster= round(int(row['Catch Booster'].replace('%', ''))/100, 2),
            break_booster= round(int(row['Break Booster'].replace('%', ''))/100, 2),
        )
        rod_list.append(rod)
    return rod_list