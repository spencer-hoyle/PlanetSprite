def get_fish_list(self, path):
    fish_list = []
    df = pd.read_csv(path)
    for id, row in df.iterrows():
        fish = Fish(
            id = row['ID'] + '-' + row['Tier'][0],
            tier = row['Tier'],
            biome = row['Biome'],
            seasons = [seasons for seasons in  row['Seasons'].split(',')],
            weather = [weather for weather in  row['Weather'].split(',')],
            time_of_day = [time_of_day for time_of_day in  row['Time of Day'].split(',')],
        )
        fish_list.append(fish)
    
    return fish_list

def get_bait_list(path, fish_list):
    bait_list = []
    df = pd.read_csv('data/bait.csv')
    for idx, row in df.iterrows():
        bait = Bait(
            id= row['Bait'],
            fish_list= fish_list if row['Fish'] == 'All' else [f for f in fish_list if f.tier == row['Fish']],
            catch_booster= round(int(row['Catch Booster'].replace('%', ''))/100, 2),
            common_booster= round(int(row['Common Booster'].replace('%', ''))/100, 2),
        )
        bait_list.append(bait)

    return bait_list

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