from enum import Enum
from functools import reduce
from collections import Counter
import random
class Industry(Enum):
    HOUSE = 1
    SMOKE = 2
    CORN = 3
    GREENLINE = 4
    WIFI = 5

class Country(Enum):
    US = 1
    CN = 2
    UK = 3
    EU = 4
    JP = 5

class Card:
    def __init__(self, points, industry, country):
        self.industry = industry
        self.points = points
        self.country = country

def calculateCardScore(cards, industry, country, numPlayers):
    score = 0
    matchNation = 0
    if numPlayers == 5:
        numPlayers = "5"
    else:
        numPlayers = "3-4"

    mappedValue = map(lambda card: card.points, cards)
    score = score + reduce(lambda bal,points: bal + points, mappedValue, 0)

    numNation = len(list(filter(lambda x: x.country == country, cards)))
    score = score + nationalization[numNation, numPlayers]
    
    industries = Counter(map(lambda card: card.industry, cards))
    score = score + monopolization[(industries[Industry.CORN], numPlayers)]
    score = score + monopolization[(industries[Industry.SMOKE], numPlayers)]
    score = score + monopolization[(industries[Industry.HOUSE], numPlayers)]
    score = score + monopolization[(industries[Industry.WIFI], numPlayers)]
    score = score + monopolization[(industries[Industry.GREENLINE], numPlayers)]

    industries[industry] = industries[industry] + 1
    industries = list(industries.values())
    numAll5 = 0
    numAll4 = 0
    numAll3 = 0
    if len(industries) == 5:
        numAll5 = min(industries)
        industries = list(map(lambda x: x - numAll5, industries))
        industries.remove(min(industries))
    if len(industries) >= 4:
        numAll4 = min(industries)
        industries = list(map(lambda x: x - numAll4, industries))
        industries.remove(min(industries))
    if len(industries) >= 3:
        numAll3 = min(industries)
    
    if numPlayers == "3-4":
        score = score + numAll3 * 6 + numAll4 * 10
    else:
        score = score + numAll3 * 10 + numAll4 * 15 + numAll5 * 21
    

    return score


Countries4Player = [Country.US, Country.CN, Country.EU, Country.JP]
Countries5Player = [Country.US, Country.CN, Country.UK, Country.EU, Country.JP]
Industries4Player = [Industry.CORN, Industry.HOUSE, Industry.SMOKE, Industry.GREENLINE]
Industries5Player =  [Industry.CORN, Industry.HOUSE, Industry.SMOKE, Industry.GREENLINE, Industry.WIFI]

#numMatch, PlayerCount
nationalization = {
    (0,"3-4"): 0,
    (0,"5"): 0,
    (1,"3-4"): 1,
    (1,"5"): 1,
    (2,"3-4"): 3,
    (2,"5"): 6,
    (3,"3-4"): 6,
    (3,"5"): 10,
    (4,"3-4"): 10,
}

#numMatch, PlayerCount
monopolization = {
    (0,"3-4"): 0,
    (0,"5"): 0,
    (1,"3-4"): 0,
    (1,"5"): 0,
    (2,"3-4"): 3,
    (2,"5"): 6,
    (3,"3-4"): 6,
    (3,"5"): 10,
    (4,"3-4"): 10,
    (4,"5"): 16,
}
Cards4Player = [
    Card(1, Industry.SMOKE, Country.CN),
    Card(1, Industry.CORN, Country.EU),
    Card(1, Industry.HOUSE, Country.US),
    Card(1, Industry.GREENLINE, Country.JP),
    Card(2, Industry.HOUSE, Country.EU),
    Card(2, Industry.CORN, Country.CN),
    Card(2, Industry.SMOKE, Country.JP),
    Card(2, Industry.GREENLINE, Country.US),
    Card(3, Industry.HOUSE, Country.CN),
    Card(3, Industry.GREENLINE, Country.EU),
    Card(3, Industry.CORN, Country.JP), 
    Card(3, Industry.SMOKE, Country.US),
    Card(4, Industry.GREENLINE, Country.CN),
    Card(4, Industry.SMOKE, Country.EU),
    Card(4, Industry.HOUSE, Country.JP),
    Card(4, Industry.CORN, Country.US),
]

Cards5Player = [
    Card(2, Industry.HOUSE, Country.EU),
    Card(2, Industry.CORN, Country.CN),
    Card(2, Industry.SMOKE, Country.JP),
    Card(2, Industry.GREENLINE, Country.US),
    Card(2, Industry.WIFI, Country.UK),
    Card(3, Industry.HOUSE, Country.CN),
    Card(3, Industry.GREENLINE, Country.EU),
    Card(3, Industry.SMOKE, Country.US),
    Card(3, Industry.WIFI, Country.JP),
    Card(3, Industry.CORN, Country.UK),
    Card(4, Industry.SMOKE, Country.EU),
    Card(4, Industry.HOUSE, Country.JP),
    Card(4, Industry.CORN, Country.US),
    Card(4, Industry.GREENLINE, Country.UK),
    Card(4, Industry.WIFI, Country.CN),
]


def getShuffledDecks(numPlayers):
    random.seed()
    bidDeck = []
    industries = []
    countries = []
    if numPlayers == 3 or numPlayers == 4:
        bidDeck = random.sample(Cards4Player, len(Cards4Player))
        industries = random.sample(Industries4Player, len(Industries4Player))
        countries = random.sample(Countries4Player, len(Industries4Player))
    else:
        bidDeck = random.sample(Cards5Player, len(Cards5Player))
        industries = random.sample(Industries5Player, len(Industries5Player))
        countries = random.sample(Countries5Player, len(Countries5Player))
    return (bidDeck, industries, countries)

