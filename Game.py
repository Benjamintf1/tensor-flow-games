import Cards

class Player:
    def __init__(self, bot, industry, country):
        self.bot = bot
        self.industry = industry
        self.country = country
        self.zeroBids = []
        self.cards = []
        self.totalBids = 0
        self.peaked = False
def PlayGame(bots):
    (deck, industries, countries) = Cards.getShuffledDecks(len(bots))
    
    players = []
    for num, bot in enumerate(bots):
        contructedBot = bot(num, countries[:len(bots)], industries[num])
        players.append(Player(contructedBot, industries[num], countries[num]))
    for gameRound in range(int(len(deck)/len(players))):
        for impulse in range(len(players)):
            card = deck.pop()
            blindBid = players[impulse].bot.bid(card, 0, gameRound, impulse, [True]*len(players))
            if blindBid <= 0:
                blindBid = 9001
            (winner, bid, zeroes) = doImpulse(players, blindBid, card, gameRound, impulse, [], 3)
            recordBids(players, card, winner, bid, zeroes, gameRound, impulse)
            
    if len(players) == 3:
        card = deck.pop()
        (winner, bid, zeroes) = doImpulse(players, 0, card, 0, 4, [], 3)
        recordBids(players, card, winner, bid, [False]*3, gameRound, impulse)
    return getScore(players)

def getScore(players):
    scores = []
    totalSpent = list(map(lambda x: x.totalBids, players))
    minBids = min(totalSpent)
    maxBids = max(totalSpent)
    for num, player in enumerate(players):
        if player.totalBids == maxBids:
            scores.append(-5 + num)
        else:
            score = 0
            if player.totalBids == minBids:
                if len(players) == 5:
                    score = score + 7
                else:
                    score = score + 6
            score = score + sum(player.zeroBids)
            cardScore = Cards.calculateCardScore(player.cards, player.industry, player.country, len(players))
            scores.append(score)
    return scores, totalSpent

def recordBids(players, card, winner, bid, zeroes, gameRound, impulse):
    for num, player in enumerate(players):
        if num == winner:
            player.bot.results(winner, bid, zeroes)
            player.cards.append(card)
            player.totalBids = player.totalBids + bid
        elif num == impulse:
            player.bot.results(winner, bid, zeroes)
        else:
            peak = player.bot.results(winner, -1, zeroes)
            if peak == True and player.peaked != True and len(players) == 5:
                player.bot.results(winner, bid, zeroes)
                player.peaked = True
        if zeroes[num] and len(players) != 3:
            player.zeroBids.insert(2, gameRound)

# show auctioneer all bids...woops           
def doImpulse(players, blindBid, card, gameRound, impulse, previousBids, count):
    bids = Bid(players, card, blindBid, gameRound, impulse,[True]*len(players), [False]*len(players))
    maxBid = max(bids)
    maxBids = list(map(lambda x: x == maxBid, bids))
    zeroBids = list(map(lambda x: x == 0, bids))
    if maxBids.count(True) > 1:
        if count == 1:
            allBids = bids + previousBids
            maxBid = max(allBids)
            maxBids = list(map(lambda x: x == maxBid, allBids))
            while maxBids.count(True) > 1:
                allBids = list(filter(lambda x: x != maxBid, allBids))
                maxBid = max(allBids)
                maxBids = list(map(lambda x: x == maxBid, allBids))
            return (bids + previousBids).index(maxBid) % len(players)    
        else:
            return doImpulse(players, blindBid, card, gameRound, impulse, bids+previousBids, count-1)
    else:
        return bids.index(maxBid), maxBid, zeroBids

def Bid(players, card, blindBid, gameRound, impulse, remaining, zeroes):
    bids = []

    for num, player in enumerate(players):
        
        if remaining[num]:
            if num == impulse:
                bids.append(blindBid)
            else:
                bid = players[num].bot.bid(card, blindBid, gameRound, impulse, remaining)
                if bid == blindBid:
                    bid = 0
                bids.append(bid)
        else:
            if zeroes[num]:
                bids.append(0)
            else:
                bids.append(-1)
    return bids

