import Company
from functools import reduce
from collections import Counter
import copy
class Player:
    def __init__(self, bot, industry, country):
        self.bot = bot
        self.industry = industry
        self.country = country
        self.companies = []
        self.currentBids = []
        self.totalBids = 0
        self.peekedBid = None

    def bid(self, gameState):
        openBid = gameState.openBid
        bid = self.bot.bid(gameState)
        if openBid == 0 and bid <= 0:
            bid = 9001
        elif bid == openBid or bid < 0:
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
            self.impulse = -1
            self.gameRound = -1
            self.performBlindAuction()

        #TODO: tiebreakers
        return self.calculateScore()

    def numPlayers(self):
        return len(self.players)

    def getNextCompany(self):
        return self.companies.pop()

    def setupGame(self):
        self.players = []
        self.openBids = []
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
        openBid = auctioneer.bid(state)
        self.openBids.append(openBid)
        (winner, bid) = self.performBidding(self.getBidders(), openBid, company)
        if winner == None:
            winner = auctioneer
            bid = openBid
        winner.awardCompany(company, bid)
        self.winners.append(self.players.index(winner))
        self.bids[(self.gameRound, self.impulse)] = list(map(lambda x: x.currentBids, self.players))
        if self.numPlayers() == 5:
            for player in self.players:
                if player != auctioneer and player != winner and winner != auctioneer and player.peekedBid == None:
                    peek = player.bot.peek(self.getGameStateForPlayer(player, [winner], -1))
                    if peek:
                        player.peekedBid = (self.gameRound, self.impulse, bid)

    def performBlindAuction(self):
        company = self.getNextCompany()
        (winner, bid) = self.performBidding(self.players, 0, company)
        if winner != None:
            winner.awardCompany(company, bid)

    def performBidding(self, players, openBid, company):
        playersToRebid = players
        for x in range(0,3):
            self.Bid(playersToRebid, company, openBid)
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


    def Bid(self, players, company, openBid):
        bids = []
        for player in players:
            state = self.getGameStateForPlayer(player, players, openBid)
            player.bid(state)

    def getGameStateForPlayer(self, player, players, openBid):
        playerIndex = self.players.index(player)
        totalBids = player.totalBids
        countries = self.countries
        industry = player.industry
        auctioneerBids = list(filter(lambda x: x[0][1] == playerIndex, self.bids.items()))
        seenCompanies = self.seenCompanies
        winners = self.winners
        zeroBids = self.getZeroBids()
        zeroBids = []
        peekedBid = player.peekedBid
        currentBidders = list(map(lambda x: self.players.index(x), players))
        return GameState(playerIndex, openBid, totalBids, countries, industry, auctioneerBids, seenCompanies, winners, zeroBids, peekedBid, currentBidders, self.impulse, self.gameRound, self.openBids)

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
                if len(self.players) != 3:
                    zeroBids = self.getZeroBids()
                    zeroBidRounds = []
                    playerIndex = self.players.index(player)
                    for zeroBid in filter(lambda x: x[0][2] == playerIndex, zeroBids.items()):
                        zeroBidRounds.insert(zeroBid[0][0], 2)
                    score = score + sum(zeroBidRounds)
                score = score + Company.calculateCompanyScore(player.companies, player.industry, player.country, len(self.players))
                scores.append(score)
        return scores, totalSpent

class GameState:
    def __init__(self, playerIndex, openBid, totalBids, countries, industry, auctioneerBids, seenCompanies, winners, zeroBids, peekedBid, currentBidders, impulse, gameRound, openBids): 
        self.openBid = copy.deepcopy(openBid)
        self.openBids = copy.deepcopy(openBids)
        self.playerIndex = copy.deepcopy(playerIndex)
        self.country = copy.deepcopy(countries[playerIndex])
        self.industry = copy.deepcopy(industry)
        self.countries = copy.deepcopy(countries)
        self.seenCompanies = copy.deepcopy(seenCompanies)
        self.biddingOn = copy.deepcopy(seenCompanies[-1])
        self.winners = copy.deepcopy(winners)
        self.totalBids = copy.deepcopy(totalBids)
        self.auctioneerBids = copy.deepcopy(auctioneerBids)
        self.numPlayers = copy.deepcopy(len(countries))
        self.zeroBids = copy.deepcopy(zeroBids)
        self.peekedBid = copy.deepcopy(peekedBid)
        self.currentBidders = copy.deepcopy(currentBidders)
        self.gameRound = copy.deepcopy(gameRound)
        self.impulse = copy.deepcopy(impulse)
