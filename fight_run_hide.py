import random

class FightRunHide():
    def __init__(self, health, printing = True):
        self.start_health = health

        self.start_maxhealth = health
        self.printing = printing

        self.reset()

    def reset(self):

        self.health = self.start_health
        self.maxhealth = self.start_maxhealth
        self.last_kills = 0
        self.kills = 0
        self.fight_kills_gain = 1
        self.fight_hp_loss = 50

        self.hide_kills_gain = 1
        self.hide_hp_loss = 50
        self.hide_hp_gain = 15

        self.run_hp_gain = 10
        self.run_hp_loss = 100
        self.run_kills_gain = 2

        self.cry_gain = 15
        self.cry_loss = 10

        return int(self.health / 5), {}
    
    def step(self, action):
        if action == 0:
            self.fight()

        elif action == 1:
            self.run()
            
        elif action == 2:
            self.hide()

        # elif action == 3:
        #     self.cry()

        reward = self.kills - self.last_kills

        self.last_kills = self.kills
        return int(self.health / 5), reward, self.health <= 0, {}

    def fight(self):
        if random.random() > 0.5:
            self.kills += self.fight_kills_gain
            if self.printing:
                print(f'\nYou fought and get {self.fight_kills_gain} kill')
        else:
            self.health -= self.fight_hp_loss
            if self.health < 0 :
                self.health = 0
            if self.printing:
                print(f'\nYou fought but lose {self.fight_hp_loss} hp')

    
    def hide(self):
        x = random.random()
        if x < 0.1:
            self.kills += self.hide_kills_gain
            if self.printing:
                print(f'\nYou hid and get {self.hide_kills_gain} kill')
        elif 0.1 <= x < 0.3:
            self.health -= self.hide_hp_loss
            if self.printing:
                print(f'\nYou hid but lose {self.hide_hp_loss} hp')
        else:
            self.health += self.hide_hp_gain
            self.cap_health()
            if self.printing:
                print(f'\nYou hid and gain {self.hide_hp_gain} hp')

    def run(self):
        y = random.random()
        if y < 0.9:
            self.health += self.run_hp_gain
            self.cap_health()
            if self.printing:
                print(f'\nYou ran and gain {self.run_hp_gain} hp')
        elif 0.9 <= y < 0.95:
            self.health -= self.run_hp_loss
            if self.printing:
                print(f'\nYou ran but lose {self.run_hp_loss} hp')
        else:
            self.kills += self.run_kills_gain
            if self.printing:
                (f'\nYou ran and get {self.run_kills_gain} kills')

    def cry(self):
        y = random.random()
        if y < 0.45:
            self.health += self.cry_gain
            if self.printing:
                print(f"You cried and gained {self.cry_gain} hp")
        else:
            self.health -= self.cry_loss
            if self.printing:
                print(f"You cried and lost {self.cry_loss} hp")
        self.cap_health()

    def cap_health(self):
        if self.health > self.maxhealth :
            self.health = self.maxhealth

if __name__ == "__main__":
    player = FightRunHide(150)

    while player.health > 0:
        action = int(input("What's your operation? \nFight (1), Hide (2), Run (3) or Cry(4)\n"))

        if action == 1:
            player.fight()

        elif action == 2:
            player.run()
            
        elif action == 3:
            player.hide()
        elif action == 4:
            player.cry()
        else:
            print('Please choose 1, 2, 3 or 4')

        #print(action)
        print('Kills = ' + str(player.kills) + '  ' + 'hp = ' + str(player.health) + '\n')

    if player.health <= 0:
        print("You've got " + str(player.kills) + " kills")
        print("Game over! Better luck next time!")