"""
Game Assumptions:

- 7 Biomes
- 4 Seasons
- Each season is 7 days longs (switches on sundays)
- A single day in the game is 15 minutes real time
- Daytime starts at 6:00 and Night starts at 20:00
- Each day has a specific weather, determined at the start of Daytime (6:00):
    - Spring: 75% Clear, 25% Rain
    - Summer: 85% Clear, 15% Rain
    - Autumn: 75% Clear, 25% Rain
    - Winter: 100% Clear, 0% Rain
"""

BIOMES = [
    "Small Water Area", 
    "Beach", 
    "Desert", 
    "Cave (Leafy)", 
    "Cave (Ice)", 
    "Cave (Lava)", 
    "Cave (Ash)"
]

SEASONS = [
    "Spring",
    "Summer",
    "Autumn",
    "Winter"
]

WEATHER = [
    "Rainy", 
    "Clear"
]

TIME_OF_DAY = [
    "Day", 
    "Night"
]

# [Rainy, Clear]
WEATHER_PROBABILITY = {
    "Spring": [0.25, 0.75],
    "Summer": [.15, .85],
    "Autumn": [.25, .75],
    "Winter": [0, 1]
}
