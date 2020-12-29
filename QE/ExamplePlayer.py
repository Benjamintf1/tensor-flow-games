import random
class Player:
    def __init__(self):
        self.printedOnce = False

    def bid(self, gameState):
        if not self.printedOnce and gameState.playerIndex == 0 and gameState.gameRound == 2: 
            #these are all the pieces of data in use
            print("the impulse, or whos turn it is to be the auctioneer. -1 if in bonus round(only 3 players)")
            print(gameState.impulse)
            print("the round. -1 if in bonus round(only 3 players)")
            print(gameState.gameRound)
            print("this is the bid placed by the auctioner. If the bid is either you are the auctioneer, or there isn't any")
            print(gameState.openBid)

            print("this is the previous and current bids placed by the auctioner.")
            print(gameState.openBids)


            print("the number of players in the current game")
            print(gameState.numPlayers)

            print("this is which player you are. 0=first")
            print(gameState.playerIndex)

            print("# this is the country you are, This is a enum defined in Company.py")
            print(gameState.country)

            print("your hidden industry, enum in Company.py")
            print(gameState.industry)

            print("a list of countries which palyers are, listed in turn order")
            print(gameState.countries)

            print("a list of all companies already bid on, and the current company bid on")
            print(gameState.seenCompanies)

            print("the current company up for auction")
            print(gameState.biddingOn)

            print("a list of which player, by index, has won each previous card")
            print(gameState.winners)

            print("the amount that has been spent by you on companies so far")
            print(gameState.totalBids)

            print("a map of all the bids you have seen as auctioneer. Format is key=(gameRound, impulse), value=([ [player 1 bets], [player 2 bets], ...] multiple entries means there was ties")
            print(gameState.auctioneerBids)
        
            print("a map of (round, impulse, player). The presence of a true value means the player bet 0 in that round and impulse")
            print(gameState.zeroBids)
            
            print("The (round, impulse, value) of the winning bid which you peeked at. None if not present") 
            print(gameState.peekedBid)
            
            print("the indexes of the players you are competing againsts")
            print(gameState.currentBidders)

            print("all your bot really needs to do is return a number of what to bid")
            print("\n\n\n")
            self.printedOnce = True
        return random.randint(1,3) # what you bid
    
    def peek(self, gameState):
        if gameState.playerIndex == 0:
            print("this function is only called in 5 player games. return true if you wish to peek at the winning bid. Will be placed in peeked bid.")
        return True

