import streamlit as st
import pandas as pd

from gameplay.game import BIOMES, SEASONS, WEATHER, TIME_OF_DAY
from gameplay.fish import FISH_TIERS, get_fish_list, get_fish_pools
from gameplay.rod import get_rod_list
from gameplay.bait import get_bait_list
from gameplay.simulation import simulate_biome_season

# python -m streamlit run app.py

st.set_page_config(page_title="PlanetSprite", page_icon=":fish:", layout = "wide")

st.title(':fish: PlanetSprite Fishing')

def get_fish_df(fish_list):
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
    fish_data = {attr: [getattr(fish, attr) for fish in fish_list] for attr in columns}
    df = pd.DataFrame(fish_data)

    for column in ['break_rate', 'catch_rate', 'common_rate']:
        df[column] = df[column].map(lambda x: '{:.0%}'.format(x))

    df = df.rename(columns=column_mapping)

    return df

def get_fish_pools_df(fish_pools):
    df = pd.DataFrame(fish_pools)
    df['Fish Pool'] = [[fish.id for fish in fish_list] for fish_list in df['Fish Pool']]
    return df

t1, t2, t3 = st.tabs(['Fishing Objects', 'Fish Pools', 'Simulation'])
with t1:
    fish_list = get_fish_list('data/fish.csv')
    rod_list = get_rod_list('data/rods.csv')
    bait_list = get_bait_list('data/bait.csv', fish_list)
    fish_pools = get_fish_pools(fish_list)

    fish_df = get_fish_df(fish_list)
    rod_df = pd.read_csv('data/rods.csv')
    bait_df = pd.read_csv('data/bait.csv')


    st.subheader('Fish')
    st.dataframe(fish_df, hide_index=True)

    st.subheader('Rods')
    st.dataframe(rod_df, hide_index=True)

    st.subheader('Bait')
    st.dataframe(bait_df, hide_index=True)

with t2:
    st.subheader('Fish Pools')
    st.write('Fish Pool are fish available to catch for a given biome, season, weather, and time of day')
    fish_pools_df = get_fish_pools_df(fish_pools)
    
    c1,c2,c3,c4,c5 = st.columns(5)
    biome = c1.multiselect('Biome', BIOMES)
    season = c2.multiselect('Season', SEASONS)
    weather = c3.multiselect('Weather', WEATHER)
    time_of_day = c4.multiselect('Time of Day', TIME_OF_DAY)
    fish_tier = c5.multiselect('Fish Tier', FISH_TIERS)
    
    if biome:
        fish_pools_df = fish_pools_df[fish_pools_df['Biome'].isin(biome)]
    if season:
        fish_pools_df = fish_pools_df[fish_pools_df['Season'].isin(season)]
    if weather:
        fish_pools_df = fish_pools_df[fish_pools_df['Weather'].isin(weather)]
    if time_of_day:
        fish_pools_df = fish_pools_df[fish_pools_df['Time Of Day'].isin(time_of_day)]
    if fish_tier:
        fish_pools_df = fish_pools_df[fish_pools_df['Fish Pool'].apply(lambda fish_list: any(fish_id[-1] in [tier[0] for tier in fish_tier] for fish_id in fish_list))]
    
    st.dataframe(fish_pools_df, hide_index= True, use_container_width=True)

#rod = rod_list[0]
#bait = bait_list[0]
#biome = BIOMES[0]
#season = SEASONS[0]

#data = simulate_biome_season(biome, season, rod, bait)
#print(data)
