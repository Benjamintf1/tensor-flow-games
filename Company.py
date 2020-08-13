from enum import Enum
from functools import reduce
from collections import Counter
import random
class Industry(Enum):
    HOUSING = 1
    MANUFACTURING = 2
    AGRICULTURE = 3
    FINANCE = 4
    GOVERNMENT = 5

class Country(Enum):
    US = 1
    CN = 2
    UK = 3
    EU = 4
    JP = 5

class Company:
    def __init__(self, points, industry, country):
        self.industry = industry
        self.points = points
        self.country = country

def calculateCompanyScore(companies, industry, country, numPlayers):
    score = 0
    matchNation = 0
    if numPlayers == 5:
        numPlayers = "5"
    else:
        numPlayers = "3-4"

    mappedValue = map(lambda company: company.points, companies)
    score = score + reduce(lambda bal,points: bal + points, mappedValue, 0)

    numNation = len(list(filter(lambda x: x.country == country, companies)))
    score = score + nationalization[numNation, numPlayers]
    
    industries = Counter(map(lambda company: company.industry, companies))
    score = score + monopolization[(industries[Industry.AGRICULTURE], numPlayers)]
    score = score + monopolization[(industries[Industry.MANUFACTURING], numPlayers)]
    score = score + monopolization[(industries[Industry.HOUSING], numPlayers)]
    score = score + monopolization[(industries[Industry.GOVERNMENT], numPlayers)]
    score = score + monopolization[(industries[Industry.FINANCE], numPlayers)]

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

def getShuffledDecks(numPlayers):
    random.seed()
    companies = []
    industries = []
    countries = []
    if numPlayers == 3 or numPlayers == 4:
        companies = random.sample(Companies4Player, len(Companies4Player))
        industries = random.sample(Industries4Player, len(Industries4Player))
        countries = random.sample(Countries4Player, len(Industries4Player))
    else:
        companies = random.sample(Companies5Player, len(Companies5Player))
        industries = random.sample(Industries5Player, len(Industries5Player))
        countries = random.sample(Countries5Player, len(Countries5Player))
    return (companies, industries, countries)

Countries4Player = [Country.US, Country.CN, Country.EU, Country.JP]
Countries5Player = [Country.US, Country.CN, Country.UK, Country.EU, Country.JP]
Industries4Player = [Industry.AGRICULTURE, Industry.HOUSING, Industry.MANUFACTURING, Industry.FINANCE]
Industries5Player =  [Industry.AGRICULTURE, Industry.HOUSING, Industry.MANUFACTURING, Industry.FINANCE, Industry.GOVERNMENT]

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
Companies4Player = [
    Company(1, Industry.MANUFACTURING, Country.CN),
    Company(1, Industry.AGRICULTURE, Country.EU),
    Company(1, Industry.HOUSING, Country.US),
    Company(1, Industry.FINANCE, Country.JP),
    Company(2, Industry.HOUSING, Country.EU),
    Company(2, Industry.AGRICULTURE, Country.CN),
    Company(2, Industry.MANUFACTURING, Country.JP),
    Company(2, Industry.FINANCE, Country.US),
    Company(3, Industry.HOUSING, Country.CN),
    Company(3, Industry.FINANCE, Country.EU),
    Company(3, Industry.AGRICULTURE, Country.JP), 
    Company(3, Industry.MANUFACTURING, Country.US),
    Company(4, Industry.FINANCE, Country.CN),
    Company(4, Industry.MANUFACTURING, Country.EU),
    Company(4, Industry.HOUSING, Country.JP),
    Company(4, Industry.AGRICULTURE, Country.US),
]

Companies5Player = [
    Company(2, Industry.HOUSING, Country.EU),
    Company(2, Industry.AGRICULTURE, Country.CN),
    Company(2, Industry.MANUFACTURING, Country.JP),
    Company(2, Industry.FINANCE, Country.US),
    Company(2, Industry.GOVERNMENT, Country.UK),
    Company(3, Industry.HOUSING, Country.CN),
    Company(3, Industry.FINANCE, Country.EU),
    Company(3, Industry.MANUFACTURING, Country.US),
    Company(3, Industry.GOVERNMENT, Country.JP),
    Company(3, Industry.AGRICULTURE, Country.UK),
    Company(4, Industry.MANUFACTURING, Country.EU),
    Company(4, Industry.HOUSING, Country.JP),
    Company(4, Industry.AGRICULTURE, Country.US),
    Company(4, Industry.FINANCE, Country.UK),
    Company(4, Industry.GOVERNMENT, Country.CN),
]

