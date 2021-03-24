import pickle
import sys
import os
from random import randint


class Character:
    def __init__(self):
        self.name = ""
        self.hp = 50
        self.hp_max = 50
        self.mana = 20
        self.mana_max = 20
        self.Evil = Evil()
        self.activate_skill = False
        self.Skill = Skill()

    def change_health(self):
        if self.Evil.skill:
            self.hp -= min(randint(5, 10), (int(self.Evil.hp / 1.2))) + 5
            self.Evil.mana -= 5
            if self.Evil.mana < 5:
                self.Evil.skill = False
        else:
            self.hp -= min(randint(5, 10), (int(self.Evil.hp / 1.2)))

    def change_mana(self):
        self.mana -= self.Skill.manaOfskill

    def do_damage(self):
        damage = min(max(randint(0, 50) - randint(0, 25), 0), randint(5, 15))
        if self.activate_skill:
            if self.mana >= self.Skill.manaOfskill:
                damage += randint(int(self.Skill.dmg / 2), int(self.Skill.dmg))
                self.change_mana()
            else:
                self.activate_skill = False
                print("Not enough mana, skills deactivated")

        self.Evil.hp -= damage
        if damage == 0:
            print("%s evades %s's  attack." % (self.Evil.name, self.name), "Gor-gin's health [%s/%s], mana [%s/%s]" % (self.Evil.hp, self.Evil.hp_max, self.Evil.mana, self.Evil.mana_max))
        else:
            if self.Evil.hp > 0:
                print("%s hurts %s!" % (self.name, self.Evil.name), "Gor-gin's health [%s/%s], mana [%s/%s]" % (self.Evil.hp, self.Evil.hp_max, self.Evil.mana, self.Evil.mana_max))
            else:
                print("%s hurts %s!" % (self.name, self.Evil.name),
                      "Gor-gin's health [%s/%s], mana [%s/%s]" % (0, self.Evil.hp_max, self.Evil.mana, self.Evil.mana_max))

        return self.Evil.hp <= 0


class Skill:
    def __init__(self):
        self.skills = ["attack with dark magic", "attack with excalibur", "use the help of the gods"]
        self.dark_mana = 8
        self.dark = False
        self.ex_mana = 10
        self.ex = False
        self.helpo_mana = 25
        self.helpo = False
        self.manaOfskill = 0
        self.dmg = 1.5
        self.curv = False
        self.curv_mana = 5


class Evil(Character):
    def __init__(self) -> object:
        self.name = "a gor-gin"
        self.hp_max = randint(5, 20)
        self.mana_max = randint(5, 15)
        self.hp = self.hp_max
        self.mana = self.mana_max
        self.skill_name = "a curved sword[+5 to attack][-5 mana each attack]"
        self.skill = True

class Hero(Character):
    def __init__(self):
        Character.__init__(self)
        Evil.__init__(self.Evil)
        self.Skill = Skill()
        self.state = 'normal'
        self.myskills = []
        self.add_menu = False
        self.remove_menu = False


    def help(self):
        print("[quit] - quit the game")
        print("[rest] - take rest, replenish hp and mana")
        print("[help] - print the commands")
        print("[status] - characteristics of %s" % self.name)
        print("[explore] - explore the cave")
        print("[attack] - attack the enemy")
        print("[activate] - activate/deactivate your skill")
        print("[skills] - open your skills menu")

    def skills_menu(self):
        self.state = 'InSkills'
        print("My skills:")
        for c in range(len(self.myskills)):
            print("%s. %s" % ((c + 1), self.myskills[c]), end='\n')
        print()
        print("> 1. Add new skill")
        print("> 2. Remove skill")
        print("> 3. Leave from menu")

    def add_skill(self):
        if self.state == 'InSkills' and self.add_menu==False:
            if len(self.Skill.skills) > 0:
                if len(self.myskills) < 1:
                    self.add_menu = True
                    print("Available skills: ")
                    for c in range(len(self.Skill.skills)):
                        print("%s." % (c + 1), self.Skill.skills[c], end='\n')
                    n = input()
                    if n.isdigit() and 0 < int(n) <= len(self.Skill.skills):
                        self.myskills.append(self.Skill.skills[int(n) - 1])
                        self.Skill.skills.pop(int(n) - 1)
                        self.add_menu = False
                        print("%s successfully added a new skill" % self.name)
                        self.skills_menu()
                    else:
                        print("%s doesn't understand the suggestion." % self.name)
                        self.add_menu = False
                        self.skills_menu()
                else:
                    print("You can only have one skill")
                    self.skills_menu()
            else:
                print("No available skills")
                self.skills_menu()

    def activate(self):
        if len(self.myskills) < 1:
            print("%s doesn't have any skills" % self.name)
        else:
            if not self.activate_skill:
                if self.mana >= self.Skill.manaOfskill:
                    print("My skills:")
                    for c in range(len(self.myskills)):
                        print("%s. %s" % ((c + 1), self.myskills[c]))
                    n = input()
                    if n.isdigit() and 0 < int(n) <= len(self.myskills):
                        self.activate_skill = True
                        if self.myskills[0] == "attack with dark magic":
                            self.Skill.dark = True
                            self.Skill.dmg = int(self.Skill.dmg * self.Skill.dark_mana)
                            self.Skill.manaOfskill += self.Skill.dark_mana
                            self.activate_skill = True
                            print("Attack with dark magic activated!")
                        if self.myskills[0] == "attack with excalibur":
                            self.Skill.ex = True
                            self.Skill.manaOfskill += self.Skill.ex_mana
                            self.Skill.dmg = int(self.Skill.dmg * self.Skill.ex_mana)
                            self.activate_skill = True
                            print("Attack with excalibur activated!")
                        if self.myskills[0] == "use the help of the gods":
                            self.Skill.helpo = True
                            self.Skill.manaOfskill += self.Skill.helpo_mana
                            self.Skill.dmg = int(self.Skill.dmg * self.Skill.helpo_mana)
                            self.activate_skill = True
                            print("Use the help of the gods activated!")
                        if self.myskills[0] == "a curved sword[+5 to attack][-5 mana each attack]":
                            self.Skill.curv = True
                            self.Skill.manaOfskill += self.Skill.curv_mana
                            self.Skill.dmg = int(self.Skill.dmg * self.Skill.curv_mana)
                            self.activate_skill = True
                            print("Gor-gin's curved sword activated!")
                    else:
                        print("%s doesn't understand the suggestion." % self.name)
                        self.skills_menu()
                else:
                    print("Not enough mana!")
                    self.skills_menu()
            else:
                self.activate_skill = False
                print("Skills deactivated!")

    def remove_skill(self):
        if self.state == 'InSkills' and self.remove_menu==False:
            if len(self.myskills) > 0:
                self.remove_menu = True
                print("My skills:")
                for c in range(len(self.myskills)):
                    print("%s. %s" % ((c + 1), self.myskills[c]), end='\n')
                n = input()
                if n.isdigit() and int(n) <= len(self.myskills):
                    self.myskills.pop(int(n) - 1)
                    print("%s successfully deleted skill" % self.name)
                    self.remove_menu = False
                    self.skills_menu()
                else:
                    print("%s doesn't understand the suggestion." % self.name)
                    self.remove_menu = False
                    self.skills_menu()
            else:
                print("%s hasn't got any skills" % self.name)
                self.skills_menu()
        else:
            print("%s doesn't understand the suggestion." % self.name)

    def leave_menu(self):
        if self.state == 'InSkills':
            self.state = 'normal'
            print("%s continues journey" % self.name)
        else:
            print("%s doesn't understand the suggestion." % self.name)

    def quit(self):
        sys.exit()

    def status_menu(self):
        if self.state != 'InSkills':
            print("%s's health: %d/%d" % (self.name, self.hp, self.hp_max))
            print("%s's mana: %d/%d" % (self.name, self.mana, self.mana_max))
        else:
            print("First of all, leave the menu")

    def tired(self):
        print("%s feels tired" % self.name)
        self.hp = max(1, self.hp - 5)

    def rest(self):
        if self.state == 'InSkills':
            print("First of all, leave the menu")
        elif self.state != 'normal':
            print("%s can't rest now!" % self.name)
            self.evil_attacks()
        else:
            print("%s rests" % self.name)
            if randint(0, 1):
                self.Evil = Evil()
                print("%s is rudely awakened by %s with %s!" % (self.name, self.Evil.name, self.Evil.skill_name))
                self.state = 'fight'
                self.evil_attacks()
            else:
                if (self.hp_max - self.hp) >= 5:
                    self.hp += int((self.hp_max - self.hp) / 2)
                else:
                    print("%s slept too much!" % self.name)

    def explore(self):
        if self.state == 'InSkills':
            print("First of all, leave the menu")
        elif self.state != 'normal':
            print("%s is too busy right now!" % self.name)
            self.evil_attacks()
        else:
            print("%s explores a mysterious cave" % self.name)
            if randint(0, 1):
                self.Evil = Evil()
                print("%s encounters %s with %s" % (self.name, self.Evil.name, self.Evil.skill_name))
                self.state = 'fight'
            else:
                if randint(0, 1):
                    self.tired()

    def attack(self):
        if self.state != 'fight':
            print("You're not in fight")
        else:
            if self.do_damage():
                print("%s executes %s!" % (self.name, self.Evil.name))
                if not self.activate_skill and len(self.myskills) < 1:
                    self.myskills.append(self.Evil.skill_name)
                    print("A gor-gin's skill became yours!")
                self.state = 'normal'
                self.hp_max += self.Evil.hp_max
                self.mana_max += self.Evil.mana_max
                self.Evil = None
                print("%s feels stronger!" % self.name)
            else:
                self.evil_attacks()

    def evil_attacks(self):
        print("A gor-gin attacks!")
        Character.change_health(self)
        self.Evil.hp -= min(randint(0, 10), int(self.Evil.hp / 1.7))
        if self.hp <= 0:
            print('%s was slaughtered by %s!!!\nR.I.P.' % (self.name, self.Evil.name))
            sys.exit()


Commands = {
    'quit': Hero.quit,
    'q': Hero.quit,
    'Q': Hero.quit,
    'rest': Hero.rest,
    'help': Hero.help,
    'status': Hero.status_menu,
    'explore': Hero.explore,
    'attack': Hero.attack,
    'skills': Hero.skills_menu,
    '1': Hero.add_skill,
    '2': Hero.remove_skill,
    '3': Hero.leave_menu,
    'activate': Hero.activate,
}

h = Hero()
print("Hello, player!")
print("What is your character's name?")
h.name = input()
print("(type help to get a list of actions)")
print("%s enters a dark cave, searching for adventure." % h.name)

while h.hp > 0:
    line = input("> ")
    args = line.lower().strip().split()
    if len(args) > 0:
        commandFound = False
        for i in Commands.keys():
            if args[0] == i[:len(args[0])]:
                Commands[i](h)
                commandFound = True
                break
        if not commandFound:
            print("%s doesn't understand the suggestion." % h.name)