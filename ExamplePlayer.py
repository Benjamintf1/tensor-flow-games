import Cards
import random
class Player:
    def __init__(self, index, countries, industry):
        self.index = index #which order you play in
        self.Countries = countries # which countries all the players are
        self.industry = industry # which industry you have

    def bid(self, card, openBid, gameRound, impulse, playerList):
        # card = card you are bidding on, based on Cards.py
        # openBid = populated with open bid, 0 if you are openBidder
        # gameRound = which round is it
        # impulse = who is auctioneer
        # playerList = true and false list of players in contention
        return random.randint(1,10) # what you bid
    #TODO: detail this
    #def show(self):
        #do this

    def results(self, winner, winningBid, zeroBids):
        # winner = winning player index
        # winningBid = populated with winning bid(or -1 if hidden)
        # zeroBids = true and false list of players with zero bids
        # if a 5 player game, return true if you want to use your 1 bid, result will be called again
        return True
    
