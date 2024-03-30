import random

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

WEATHER_PROBABILITY = {
    "Spring": {
        "Rainy": 0.25, 
        "Clear": 0.75
        },
    "Summer": {
        "Rainy": 0.15, 
        "Clear": 0.85
        },
    "Autumn": {
        "Rainy": 0.25, 
        "Clear": 0.75
        },

    "Winter": {
        "Rainy": 0, 
        "Clear": 1
        }
}

def get_weather(season):
    probabilities = WEATHER_PROBABILITY.get(season)
    options = probabilities.keys()
    weights = probabilities.items()
    weather = random.choices(options, weights=weights)
    return weather[0]
