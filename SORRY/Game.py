import random
from functools import reduce
from collections import Counter
from operator import add
from tqdm import tqdm

class Game:
    def __init__(self, player1, player2, player3, player4):
        self.players = [player1, player2, player3, player4]


    def Play(self):
        winOrder = []
        for p in self.players:
            p.numGames += 1
        self.pawns = [ Pawn(1), Pawn(1), Pawn(1), Pawn(1), Pawn(2), Pawn(2), Pawn(2), Pawn(2), Pawn(3), Pawn(3), Pawn(3), Pawn(3), Pawn(4), Pawn(4), Pawn(4), Pawn(4) ]
        self.turn = 1

        while not self.IsDone():
            goAgain = False
            # need to implement play again if capture and if 6 move
            self.roll = random.randint(1,6)
            if self.roll == 6:
                goAgain = True

            MovablePawns = self.MovablePawns()
            if len(MovablePawns) > 0:
                index = self.players[self.turn - 1].Choose(self.roll, MovablePawns, self.pawns)
                movedPawn = MovablePawns[index]
                movedPawn.MovePawn(self.roll)
                captured = self.CapturePawns(movedPawn.location)
                if captured:
                    goAgain = True
                if self.PlayerDone():
                    winOrder.append(self.turn)
            if not goAgain or self.PlayerDone():
                self.turn = self.turn % 4 + 1
        self.players[winOrder[0] - 1].wins[winOrder[0] - 1] += 1
        self.players[winOrder[0] - 1].wins[4] += 1


    def MovablePawns(self):
        return [x for x in self.PlayersPawns() if x.CanMove(self.roll)]

    def PlayersPawns(self):
        return [x for x in self.pawns if x.playerNum == self.turn]

    def PlayerDone(self):
        donePawns = [x for x in self.PlayersPawns() if x.IsDone()]
        return len(donePawns) == 4

    def CapturePawns(self, location):
        captured = False
        for pawn in self.OtherPawns():
            if pawn.location == location and location != -1 and location % 13 != 0 and location % 13 != 8:
                self.players[pawn.playerNum -1].spacesCaptured[pawn.playerNum -1] += pawn.distance
                self.players[pawn.playerNum -1].spacesCaptured[4] += pawn.distance
                self.players[pawn.playerNum -1].numCaptured[pawn.playerNum -1] += 1
                self.players[pawn.playerNum -1].numCaptured[4] += 1
                pawn.Captured()
                captured = True
        return captured

    def OtherPawns(self):
        return [x for x in self.pawns if x.playerNum != self.turn]


    def IsDone(self):
        for i in self.pawns:
            if not i.IsDone():
                return False
        return True



class Pawn:
    def __init__(self, playerNum):
        self.location = -1
        self.distance = -1
        self.playerNum = playerNum

    def IsDone(self):
        return self.distance == 56

    def CanMove(self, roll):
        if self.distance == -1 and roll == 6:
            return True
        if self.distance == -1 or self.distance == 56:
            return False
        return self.distance + roll <= 56

    def MovePawn(self, move):
        if self.distance == -1 and move == 6:
            self.distance = 0
            self.location = (self.playerNum - 1) *  13
            return
        self.distance = self.distance + move
        if self.distance > (13 * 3 + 11):
            self.location = -1
        else:
            self.location = (self.location + move) %  (13*4)
         
    
    def Captured(self):
        self.location = -1
        self.distance = -1

class Cheater():
    wins = [0,0,0,0,0]
    numCaptured = [0,0,0,0,0]
    spacesCaptured = [0,0,0,0,0]
    numGames = 0
    def __init__(self):
        pass

    # add distance and later other pieces
    def Choose(self, roll, pieces, otherPawns):
        pieces[0].distance = 56 - roll
        return 0

    def PrintName(self):
        print('Cheater')

class PrisonCaptureSafeClosest():
    wins = [0,0,0,0,0]
    numCaptured = [0,0,0,0,0]
    spacesCaptured = [0,0,0,0,0]
    numGames = 0
    def __init__(self):
        pass

    def Choose(self, roll, pieces, otherPawns):
        inPrison = [x for x in pieces if x.distance == -1]
        if len(inPrison) > 0:
            return pieces.index(inPrison[0])
        me = pieces[0].playerNum
        locations = [(x.location + roll) % (13*4) for x in pieces]
        canCapture = [any((o.location == x and o.playerNum != me) for o in otherPawns) for x in locations]
        try:
            first = canCapture.index(True)
            return first
        except:
            moveSafe = [x for x in pieces if x.distance != -1 and ((x.distance + roll) > (13 * 3 + 11) or (x.distance + roll) % 13 == 0 or (x.distance + roll) % 13 == 8)]
            if len(moveSafe) > 0:
                piece = max(moveSafe, key=lambda x: x.distance)
                return pieces.index(piece)
            piece = min(pieces, key=lambda x: x.distance)
            return pieces.index(piece)


    def PrintName(self):
        print('Prison, Capture, Safe, Closest')

class PrisonCaptureSafeAlsoSafeFurthest():
    wins = [0,0,0,0,0]
    numCaptured = [0,0,0,0,0]
    spacesCaptured = [0,0,0,0,0]
    numGames = 0
    def __init__(self):
        pass

    def Choose(self, roll, pieces, otherPawns):
        inPrison = [x for x in pieces if x.distance == -1]
        if len(inPrison) > 0:
            return pieces.index(inPrison[0])
        me = pieces[0].playerNum
        locations = [(x.location + roll) % (13*4) for x in pieces]
        canCapture = [any((o.location == x and o.playerNum != me) for o in otherPawns) for x in locations]
        try:
            first = canCapture.index(True)
            return first
        except:
            moveSafe = [x for x in pieces if x.distance != -1 and ((x.distance + roll) > (13 * 3 + 11) or (x.distance + roll) % 13 == 0 or (x.distance + roll) % 13 == 8)]
            if len(moveSafe) > 0:
                piece = max(moveSafe, key=lambda x: x.distance)
                return pieces.index(piece)
            canBeCaptured = [any((o.location < x and o.location + 6 >= x and o.playerNum != me) for o in otherPawns) for x in locations]
            try:
                first = canCapture.index(False)
                return first
            except:
                piece = max(pieces, key=lambda x: x.distance)
                return pieces.index(piece)


    def PrintName(self):
        print('Prison, Capture, SafeSpace, NotCapturable, Furthest')

class PrisonCaptureSafeFurthest():
    wins = [0,0,0,0,0]
    numCaptured = [0,0,0,0,0]
    spacesCaptured = [0,0,0,0,0]
    numGames = 0
    def __init__(self):
        pass

    def Choose(self, roll, pieces, otherPawns):
        inPrison = [x for x in pieces if x.distance == -1]
        if len(inPrison) > 0:
            return pieces.index(inPrison[0])
        me = pieces[0].playerNum
        locations = [(x.location + roll) % (13*4) for x in pieces]
        canCapture = [any((o.location == x and o.playerNum != me) for o in otherPawns) for x in locations]
        try:
            first = canCapture.index(True)
            return first
        except:
            moveSafe = [x for x in pieces if x.distance != -1 and ((x.distance + roll) > (13 * 3 + 11) or (x.distance + roll) % 13 == 0 or (x.distance + roll) % 13 == 8)]
            if len(moveSafe) > 0:
                piece = max(moveSafe, key=lambda x: x.distance)
                return pieces.index(piece)
            piece = max(pieces, key=lambda x: x.distance)
            return pieces.index(piece)


    def PrintName(self):
        print('Prison, Capture, Safe, Furthest')

class BadPlayer():
    wins = [0,0,0,0,0]
    numCaptured = [0,0,0,0,0]
    spacesCaptured = [0,0,0,0,0]
    numGames = 0
    def __init__(self):
        pass

    def Choose(self, roll, pieces, otherPawns):
        inPrison = [x for x in pieces if x.distance == -1]
        if len(inPrison) == len(pieces):
            return pieces.index(inPrison[0])
        moveSafe = [x for x in pieces if x.distance != -1 and ((x.distance + roll) > (13 * 3 + 11) or (x.distance + roll) % 13 == 0 or (x.distance + roll) % 13 == 8)]
        if len(moveSafe) + len(inPrison) == len(pieces):
            piece = min(moveSafe, key=lambda x: x.distance)
            return pieces.index(piece)
        moveUnSafe = [x for x in pieces if x.distance != -1 and (x.distance + roll) <= (13 * 3 + 11) and (x.distance + roll) % 13 != 0 and (x.distance + roll) % 13 != 8]
        piece = min(moveUnSafe, key=lambda x: x.distance)
        return pieces.index(piece)

    def PrintName(self):
        print('Bad Players')

class MoveSafe():
    wins = [0,0,0,0,0]
    numCaptured = [0,0,0,0,0]
    spacesCaptured = [0,0,0,0,0]
    numGames = 0
    def __init__(self):
        pass

    def Choose(self, roll, pieces, otherPawns):
        inPrison = [x for x in pieces if x.distance == -1]
        if len(inPrison) > 0:
            return pieces.index(inPrison[0])
        moveSafe = [x for x in pieces if x.distance != -1 and ((x.distance + roll) > (13 * 3 + 11) or (x.distance + roll) % 13 == 0 or (x.distance + roll) % 13 == 8)]
        if len(moveSafe) > 0:
            piece = max(moveSafe, key=lambda x: x.distance)
            return pieces.index(piece)
        piece = max(pieces, key=lambda x: x.distance)
        return pieces.index(piece)

    def PrintName(self):
        print('out of prison first, then move furthest piece that can get to safe square')


class MovePrisonThenFurthest():
    wins = [0,0,0,0,0]
    numCaptured = [0,0,0,0,0]
    spacesCaptured = [0,0,0,0,0]
    numGames = 0
    def __init__(self):
        pass

    def Choose(self, roll, pieces, otherPawns):
        inPrison = [x for x in pieces if x.distance == -1]
        if len(inPrison) > 0:
            return pieces.index(inPrison[0])

        piece = max(pieces, key=lambda x: x.distance)
        return pieces.index(piece)

    def PrintName(self):
        print('Furthest Pawn, move out of prison first')

class MoveFurthestPawn():
    wins = [0,0,0,0,0]
    numCaptured = [0,0,0,0,0]
    spacesCaptured = [0,0,0,0,0]
    numGames = 0
    def __init__(self):
        pass

    def Choose(self, roll, pieces, otherPawns):
        piece = max(pieces, key=lambda x: x.distance)
        return pieces.index(piece)

    def PrintName(self):
        print('Furthest Pawn')
        

class MoveClosestPawn():
    wins = [0,0,0,0,0]
    numCaptured = [0,0,0,0,0]
    spacesCaptured = [0,0,0,0,0]
    numGames = 0
    def __init__(self):
        pass

    def Choose(self, roll, pieces, otherPawns):
        piece = max(pieces, key=lambda x: x.distance)
        return pieces.index(piece)

    def PrintName(self):
        print('Closest Pawn')

class MoveRandomPawn():
    wins = [0,0,0,0,0]
    numCaptured = [0,0,0,0,0]
    spacesCaptured = [0,0,0,0,0]
    numGames = 0
    def __init__(self):
        pass

    def Choose(self, roll, pieces, otherPawns):
        return random.randint(0, len(pieces) - 1)

    def PrintName(self):
        print('Random')

# make all possible playsets?
playerTypes = [MoveRandomPawn(), MoveFurthestPawn(), MovePrisonThenFurthest(), MoveClosestPawn(), MoveSafe(), BadPlayer(), PrisonCaptureSafeFurthest(), PrisonCaptureSafeClosest(), PrisonCaptureSafeAlsoSafeFurthest()]
for i in tqdm(range(100)):
    for i in range(100):
        g = Game(random.choice(playerTypes), random.choice(playerTypes), random.choice(playerTypes), random.choice(playerTypes))
        for i in range(1):
            g.Play()

playerTypes.sort(key=lambda player: player.wins[4])
for player in playerTypes:
    player.PrintName()
    print(f'wins: {player.wins}')
    print(f'num games: {player.numGames}')
    print(f'num captured: {player.numCaptured}')
    print(f'spaces captured: {player.spacesCaptured}')
