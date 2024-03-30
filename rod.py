import pandas as pd
from dataclasses import dataclass

ROD_TIERS = ["Default", "Bronze", "Iron", "Silver", "Gold"]

@dataclass
class Rod:
    id: str
    tier: str
    catch_booster: float
    break_booster: float

def get_rod_list():
    rod_list = []
    df = pd.read_csv('data/rod.csv')
    for idx, row in df.iterrows():
        rod = Rod(
            id = row['Rod'],
            tier= row['Tier'],
            catch_booster= round(int(row['Catch Booster'].replace('%', ''))/100, 2),
            break_booster= round(int(row['Break Booster'].replace('%', ''))/100, 2),
        )
        rod_list.append(rod)
    return rod_list