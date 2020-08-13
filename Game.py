import Company
from functools import reduce
from collections import Counter
class Player:
    def __init__(self, bot, industry, country):
        self.bot = bot
        self.industry = industry
        self.country = country
        self.zeroBids = []
        self.companies = []
        self.currentBids = []
        self.totalBids = 0
        self.peakedBid = None

    def bid(self, gameState):
        blindBid = gameState.blindBid
        bid = self.bot.bid(None)
        if blindBid == 0 and bid <= 0:
            bid = 9001
        elif bid == blindBid or bid < 0:
            bid = 0
        self.currentBids.append(bid)
        return bid

    def latestBid(self):
        return self.currentBids[-1]

    def resetBid(self):
        self.currentBids = []

    def awardCompany(self, company, bid):
        self.companies.append(company)
        self.totalBids = self.totalBids + bid

class Game:
    def __init__(self, bots):
        self.bots = bots
        if len(bots) == 3:
            self.numRounds = 5
        elif len(bots) == 4:
            self.numRounds = 4
        elif len(bots) == 5:
            self.numRounds = 3

    def Play(self):
        self.setupGame()
        for gameRound in range(self.numRounds):
            self.gameRound = gameRound
            for impulse in range(len(self.players)):
                self.impulse = impulse
                self.performAuction()
                self.resetBids()
                
        if len(self.players) == 3:
            self.performBlindAuction()

        #TODO: tiebreakers
        return self.calculateScore()

    def numPlayers(self):
        return len(self.players)

    def getNextCompany(self):
        return self.companies.pop()

    def setupGame(self):
        self.players = []
        self.bids = {}
        self.seenCompanies = []
        self.winners = []
        (self.companies, self.industries, self.countries) = Company.getShuffledDecks(len(self.bots))
        self.countries = self.countries[:len(self.bots)]
        for num, bot in enumerate(self.bots):
            contructedBot = bot()
            self.players.append(Player(contructedBot, self.industries[num], self.countries[num]))

    def getAuctioneer(self):
        return self.players[self.impulse]

    def getBidders(self):
        return list(filter(lambda x: x != self.getAuctioneer(), self.players))
        
    def resetBids(self):
        for player in self.players:
            player.resetBid()

    def performAuction(self):
        company = self.getNextCompany()
        self.seenCompanies.append(company)
        auctioneer = self.getAuctioneer()
        state = self.getGameStateForPlayer(auctioneer, self.players, 0)
        blindBid = auctioneer.bid(state)
        (winner, bid) = self.performBidding(self.getBidders(), blindBid, company)
        if winner == None:
            winner = auctioneer
            bid = blindBid
        winner.awardCompany(company, bid)
        self.winners.append(self.players.index(winner))
        self.bids[(self.gameRound, self.impulse)] = list(map(lambda x: x.currentBids, self.players))

    def performBlindAuction(self):
        company = self.getNextCompany()
        (winner, bid) = self.performBidding(self.players, 0, company)
        if winner != None:
            winner.awardCompany(company, bid)

    def performBidding(self, players, blindBid, company):
        playersToRebid = players
        for x in range(0,3):
            self.Bid(playersToRebid, company, blindBid)
            maxBid = max(map(lambda x: x.latestBid(), players))
            playersToRebid = list(filter(lambda x: x.latestBid() == maxBid, players))
            if len(playersToRebid) == 1:
                return (playersToRebid[0], maxBid)
        allBids = list(map(lambda x: x.currentBids,players))
        bids = reduce(lambda x,y: x + y, allBids)
        uniqueBids = list(filter(lambda x: x != 1, Counter(bids)))
        if len(uniqueBids) == 0:
            return (None, None)
        maxBid = max(uniqueBids)
        winningPlayer = list(filter(lambda x: maxBid in x.currentBids, players))
        if len(winningPlayer) == 0:
            return (None, None)
        return (winningPlayer[0], maxBid)


    def Bid(self, players, company, blindBid):
        bids = []
        for player in players:
            state = self.getGameStateForPlayer(player, players, blindBid)
            player.bid(state)

    def getGameStateForPlayer(self, player, players, blindBid):
        playerIndex = self.players.index(player)
        totalBids = player.totalBids
        countries = self.countries
        industry = player.industry
        auctioneerBids = list(filter(lambda x: x[0][1] == playerIndex, self.bids.items()))
        seenCompanies = self.seenCompanies
        winners = self.winners
        zeroBids = self.getZeroBids()
        zeroBids = []
        peakedBid = player.peakedBid
        currentBidders = list(map(lambda x: self.players.index(x), players))
        return GameState(playerIndex, blindBid, totalBids, countries, industry, auctioneerBids, seenCompanies, winners, zeroBids, peakedBid, currentBidders)
    def getZeroBids(self):
        zeroBids = {}
        for auction in self.bids.items():
            gameRound = auction[0][0]
            impulse = auction[0][1]
            for index, bids in enumerate(auction[1]):
                if bids[-1] == 0:
                    zeroBids[(gameRound, impulse, index)] = True
        return zeroBids

    def calculateScore(self):
        scores = []
        totalSpent = list(map(lambda x: x.totalBids, self.players))
        minBids = min(totalSpent)
        maxBids = max(totalSpent)
        for player in self.players:
            if player.totalBids == maxBids:
                scores.append(-5)
            else:
                score = 0
                if player.totalBids == minBids:
                    if len(self.players) == 5:
                        score = score + 7
                    else:
                        score = score + 6
                score = score + sum(player.zeroBids)
                cardScore = Company.calculateCompanyScore(player.companies, player.industry, player.country, len(self.players))
                scores.append(score)
        return scores, totalSpent

class GameState:
    def __init__(self, playerIndex, blindBid, totalBids, countries, industry, auctioneerBids, seenCompanies, winners, zeroBids, peakedBid, currentBidders): 
        #TODO: ensure not mutatable by bots
        self.blindBid = blindBid
        self.playerIndex = playerIndex
        self.country = countries[playerIndex]
        self.industry = industry
        self.countries = countries
        self.seenCompanies = seenCompanies
        self.biddingOn = seenCompanies[-1]
        self.winners = winners
        self.totalBids = totalBids
        self.auctioneerBids = auctioneerBids
        self.numPlayers = len(countries)
        self.zeroBids = zeroBids
        self.peakedBid = peakedBid
        self.currentBidders = currentBidders
