QE is a board game. For a description of the board game, feel free to read the rules/description [here](https://www.ultraboardgames.com/qe/game-rules.php). The goal of this project is to allow people to compete against each other with bots written to try and win the game. 

## How to make a bot

To make a bot you have to implement three functions. 

1) a init function. This can do whatever you want, but recieves no values.
2) a bid function. The details of the data provided is shown in ExamplePlayer.py, and will be printed out once when main is run. Return the value you want to bid for the company.
3) a peek function. This is used in 5 player games to determine if you want to see another players bid. Return true to peek at the winning bid

## How to run game with example bot

Run `python3 main.py <number of players>` to run the bot with the ExamplePlayer.py, or a modified ExamplePlayer.py player to see that it functions correctly.
The example player will show the game state available on standard out, and then the game will show the points earned by each player, and the total amount bid by each player.

