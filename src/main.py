#!/usr/bin/env python3
import random
import time

class Shotgun:
    def __init__(self):
        self.shells, self.rounds, self.blank_shells, self.live_shells = Shotgun.Reload(self)
        self.sawedOff = False

    def Reload(self):
        GameManager.msg("Shotgun is empty!")
        time.sleep(0.5)
        self.rounds = random.randint(2, 6)
        if self.rounds == 2:
            self.live_shells = 1
        elif self.rounds == 3:
            self.live_shells = random.randint(1, 2)
        elif self.rounds == 4:
            self.live_shells = 2
        elif self.rounds == 5:
            self.live_shells = random.randint(2, 3)
        else:
            self.live_shells = random.randint(3, 4)
        self.blank_shells = self.rounds - self.live_shells
        GameManager.msg(f"Rounds: {self.rounds}, shells: {self.live_shells} live, {self.blank_shells} blank")
        time.sleep(2.5)
        self.shells = ['live'] * self.live_shells + ['blank'] * self.blank_shells
        random.shuffle(self.shells)
        GameManager.msg("The shells go in an unknown order...")
        return self.shells, self.rounds, self.live_shells, self.blank_shells
    
    def Shoot(self, target):
        time.sleep(0.2)
        try:
            if self.shells[0] == 'blank':
                GameManager.linebreak("Shotgun clicks...")
                GameManager.linebreak()
                self.blank_shells -= 1
            else:
                GameManager.linebreak("BANG!")
                if self.sawedOff == True:
                    target.lives -= 2
                else:
                    target.lives -= 1
                self.live_shells -= 1
                GameManager.msg(f"{target.name} is on {target.lives} lives!")
                GameManager.linebreak()
                if target.lives < 1:
                    GameManager.EndGame(f"{target.name} has died. GG!")
            del self.shells[0]
            self.rounds -= 1
        except IndexError as e:
            GameManager.debug(e)
            GameManager.msg("Shotgun is out of ammo!")
            raise Exception
        


class GameManager:
    def __init__(self):
        shotgun = Shotgun()
        GameManager.RoundOne(shotgun)

    def linebreak(msg = ""):
        print(f"{str(' '):<12}| {msg}")

    def msg(msg):
        print(f"\033[33;1mGameManager\033[0;0m | {msg}")

    def debug(msg):
        print(f"\033[31;1m{str('Debug'):<12}\033[0;0m| {msg}")

    def EndGame(msg):
        GameManager.msg(f"End of game - {msg}")
        exit(0)

    def RoundOne(shotgun):
        Dealer = Player("Dealer", 4, '\033[32;1m')
        Dealer.say(f"What's your name?")
        while True:
            playername = str(input("> "))
            if len(playername) <= 11:
                break
            else:
                GameManager.msg("Player name too long! Must be below 12 characters.")
        Frisk = Player(playername, 4, '\033[35;1m')

        while True:
            GameManager.debug(f"{shotgun.live_shells} live, {shotgun.blank_shells} blank")
            Dealer.say(f"Your turn, {Frisk.name}.")
            GameManager.linebreak()
            movecount = 2
            while movecount > 0:
                if shotgun.rounds == 0:
                    GameManager.msg("Shotgun is empty!")
                    shotgun.Reload()
                    continue
                GameManager.msg(f"You are on: {Frisk.lives} lives")
                GameManager.msg(f"The Dealer is on: {Dealer.lives} lives")
                GameManager.msg("Valid moves:")
                GameManager.msg(" 1. Shoot Dealer (ends turn)")
                if (movecount == 2):
                    GameManager.msg(" 2. Shoot Self")
                else:
                    GameManager.msg(" 2. Shoot Self (ends turn)")
                while True:
                    move = int(input("> "))
                    if move == 1:
                        shotgun.Shoot(Dealer)
                        movecount -= 2
                        break
                    elif move == 2:
                        shotgun.Shoot(Frisk)
                        movecount -= 1
                        break
                    else:
                        GameManager.msg("Invalid move!")
            if shotgun.rounds == 0:
                shotgun.Reload()
                continue
            Frisk.say(f"Alright, Dealer's turn.")
            GameManager.linebreak()
            movecount = 2
            while movecount > 0:
                time.sleep(0.5)
                if shotgun.rounds == 0:
                    shotgun.Reload()
                    break
                if shotgun.live_shells > shotgun.blank_shells:
                    GameManager.msg("Dealer shot you!")
                    shotgun.Shoot(Frisk)
                    movecount -= 2
                    continue
                if shotgun.live_shells == shotgun.blank_shells:
                    target = random.choice([Frisk, Dealer])
                    if target == Frisk:
                        GameManager.msg("Dealer shot you!")
                        movecount -= 2
                    else:
                        movecount -= 1
                        GameManager.msg("Dealer shot himself!")
                    shotgun.Shoot(target)
                    continue
                if shotgun.blank_shells > shotgun.live_shells:
                    GameManager.msg("Dealer shot himself!")
                    shotgun.Shoot(Dealer)
                    movecount -= 1
                    continue
            if shotgun.rounds == 0:
                shotgun.Reload()

class Player:
    def __init__(self, name, lives, colour):
        self.name = name
        self.lives = lives
        self.colour = colour

    def say(self, msg):
        print(f"{self.colour}{self.name:<12}\033[0;0m| {msg}")


try:
    GM = GameManager()
except KeyboardInterrupt as e:
    print("\n\ncoward")
    
