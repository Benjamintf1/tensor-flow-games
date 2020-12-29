import ExamplePlayer
import Game
import sys

numPlayers = 0
if len(sys.argv) != 2:
    print("Incorrect arguments: run `python main.py <number of players>` to test your bot written in ExamplePlayer")
    sys.exit(1)
try:
    numPlayers = int(sys.argv[1])
except:
    print("argument must be a integer from 3-5")
    sys.exit(1)
if numPlayers <= 2 or numPlayers >= 6:
    print("argument must be a integer from 3-5")
    sys.exit(1)
result = Game.Game([ExamplePlayer.Player]*numPlayers).Play()

print("The points earned by each player")
print(result[0])
print("the ammount spent by each player")
print(result[1])
