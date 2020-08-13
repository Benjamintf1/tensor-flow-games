import random
class Player:
    def __init__(self, index, countries, industry):
        self.index = index #which order you play in
        self.Countries = countries # which countries all the players are
        self.industry = industry # which industry you have

    def bid(self, card, openBid):
        # card = card you are bidding on, based on Cards.py
        # openBid = populated with open bid, 0 if you are openBidder
        # gameRound = which round is it
        # impulse = who is auctioneer
        # playerList = true and false list of players in contention
        return random.randint(1,10) # what you bid

    
