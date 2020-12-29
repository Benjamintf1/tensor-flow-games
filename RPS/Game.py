import tensorflow as tf

ROCK = 1
PAPER = 2
SCISSORS = 3

class Game:
    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.player1moves = [0] * 10
        self.player2moves = [0] * 10

    def doGame(self):
        for i in range(10):
            rps1 = self.player1.Shoot(self.player1moves, self.player2moves)
            rps2 = self.player2.Shoot(self.player2moves, self.player1moves)
            self.player1moves[i] = rps1
            self.player2moves[i] = rps2

        self.player1.Score(self.getScore(self.player1moves, self.player2moves))
        self.player2.Score(self.getScore(self.player2moves, self.player1moves))
        return self.getScore(self.player1moves, self.player2moves)

    def getScore(self, moves1, moves2):
        winner1 = 0
        winner2 = 0
        ties = 0
        for i in range(len(moves1)):
            if moves1[i] == moves2[i]:
                ties = ties + 1
            elif moves1[i] == ROCK and moves2[i] == PAPER:
                winner2 = winner2 + 1
            elif moves1[i] == PAPER and moves2[i] == SCISSORS:
                winner2 = winner2 + 1
            elif moves1[i] == SCISSORS and moves2[i] == ROCK:
                winner2 = winner2 + 1
            elif moves2[i] == ROCK and moves1[i] == PAPER:
                winner1 = winner1 + 1
            elif moves2[i] == PAPER and moves1[i] == SCISSORS:
                winner1 = winner1 + 1
            elif moves2[i] == SCISSORS and moves1[i] == ROCK:
                winner1 = winner1 + 1
            else:
                print("THIS SHOULDN'T HAPPEN I THINK")
        return winner1 - winner2

class AlwaysRock:
    def __init__(self):
        return
    def Shoot(self, thing, thang):
        return ROCK
    def Score(self, score):
        return 
class TensorPlayer:
    def __init__(self):
        return
    def Shoot(self, thing, thang):
        return ROCK
    def Score(self, score):
        return 
        

Player1 = AlwaysRock()
Player2 = TensorPlayer()

game = Game(Player1, Player2)

print(game.doGame())
