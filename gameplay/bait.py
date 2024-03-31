import pandas as pd

from gameplay.fish import Fish

class Bait:
    def __init__(self, id, fish_list, catch_booster, common_booster):
        assert isinstance(fish_list, list) and all(isinstance(fish, Fish) for fish in fish_list)
        assert catch_booster <= 1 and catch_booster >= -1
        assert common_booster <= 1 and common_booster >= -1
        
        self.id = id
        self.fish_list = fish_list
        self.catch_booster = catch_booster
        self.common_booster = common_booster

    def get_catch_booster(self, fish):
        return self.catch_booster if fish in self.fish_list else 0

    def get_common_booster(self, fish):
        return self.common_booster if fish in self.fish_list else 0
    
def get_bait_list(path, fish_list):
    assert isinstance(fish_list, list) and all(isinstance(fish, Fish) for fish in fish_list)
    bait_list = []
    df = pd.read_csv(path)
    for idx, row in df.iterrows():
        bait = Bait(
            id= row['Bait'],
            fish_list= fish_list if row['Fish'] == 'All' else [f for f in fish_list if f.tier == row['Fish']],
            catch_booster= round(int(row['Catch Booster'].replace('%', ''))/100, 2),
            common_booster= round(int(row['Common Booster'].replace('%', ''))/100, 2),
        )
        bait_list.append(bait)

    return bait_list