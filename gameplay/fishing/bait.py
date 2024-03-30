from dataclasses import dataclass
import pandas as pd

@dataclass
class Bait:
    id: str
    fish_list: list #list of fish objects
    catch_booster: float
    common_booster: float
    
def get_catch_booster(fish, bait):
    return bait.catch_booster if fish in bait.fish_list else 0

def get_bait_list(fish_list):
    df = pd.read_csv('data/bait.csv')
    bait_list = []
    for idx, row in df.iterrows():
        bait = Bait(
            id= row['Bait'],
            fish_list= fish_list if row['Fish'] == 'All' else [f for f in fish_list if f.tier == row['Fish']],
            catch_booster= round(int(row['Catch Booster'].replace('%', ''))/100, 2),
            common_booster= round(int(row['Common Booster'].replace('%', ''))/100, 2),
        )
        bait_list.append(bait)

    return bait_list