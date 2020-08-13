import random
class Player:
    def __init__(self):
        print("making player")

    def bid(self, gameState):
        return random.randint(1,3) # what you bid

    
