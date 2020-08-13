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
        self.peaked = False

    def bid(self, company, blindBid):
        bid = self.bot.bid(company, blindBid)
        if bid == blindBid or bid < 0:
            bid = 0
        self.currentBids.append(bid)
        return bid

    def currentBids(self):
        return currentBids

    def latestBid(self):
        return self.currentBids[-1]

    def resetBid(self):
        self.currentBids = []

    def awardCompany(self, company, bid):
        self.companies.append(company)
        self.totalBids = self.totalBids + bid

class Game:
    def __init__(self, bots):
        (companies, industries, countries) = Company.getShuffledDecks(len(bots))
        self.companies = companies
        players = []
        for num, bot in enumerate(bots):
            contructedBot = bot(num, countries[:len(bots)], industries[num])
            players.append(Player(contructedBot, industries[num], countries[num]))
        self.players = players
        self.numRounds = int(len(self.companies)/len(self.players))

    def numPlayers(self):
        return len(self.players)

    def getNextCompany(self):
        return self.companies.pop()


    def Play(self):
        for gameRound in range(self.numRounds):
            self.gameRound = gameRound
            for impulse in range(len(self.players)):
                self.impulse = impulse
                self.performAuction()
                self.resetBids()
                
        if len(self.players) == 3:
            self.performBlindAuction()

        return self.calculateScore()

    def getAuctioneer(self):
        return self.players[self.impulse]

    def getBidders(self):
        return list(filter(lambda x: x != self.getAuctioneer(), self.players))
        
    def resetBids(self):
        for player in self.players:
            player.resetBid()

    def performAuction(self):
        company = self.getNextCompany()
        auctioneer = self.getAuctioneer()
        blindBid = auctioneer.bid(company, -1)
        if blindBid <= 0:
            blindBid = 9001
        (winner, bid) = self.performBidding(self.getBidders(), blindBid, company)
        if winner == None:
            auctioneer.awardCompany(company, blindBid)
        else:
            winner.awardCompany(company, bid)

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
        bids = reduce(lambda x,y: x.append(y), map(lambda x: x.currentBids(),players))
        uniqueBids = list(filter(lambda x: x != 1, Counter(bids)))
        if len(uniqueBids) == 0:
            return (None, None)
        maxBid = max(uniqueBids)
        winningPlayer = list(filter(lambda x: maxBid in x.currentBids(), players))
        if len(winningPlayer) == 0:
            return (None, None)
        return (winningPlayer, maxBid)

    def Bid(self, players, company, blindBid):
        bids = []
        for player in players:
            player.bid(company, blindBid)
    
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

