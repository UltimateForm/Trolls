# collection = ["yo", "collection", "lool", "Ok enough"]
# print(collection)
# print(collection.__len__() , len(collection), "lool" in collection) #this determines if "lool" is in collection position 2
# for i in collection:
#     print(i)

# for h in range(len(collection)): #this is the true C#' for, the one above is more like foreach i believe
#     print(collection[h])

# newCollection = list(range(5)) #so this is the constructor??? (uhm so the range(5) returns a collection)
# newCollection.insert(4,2) #pushes value into the determined index and rearranges order
# for j in newCollection:
#     print(j)


# print(len(newCollection), " over") #dont forget len(collection) to get lenght
import dialog
import sys
import game
import math
import random
import time
import numpy

TROLL_ROGUE = "troll:rogue"
TROLL_WARRIOR = "troll:warrior"
TROLL_SORCERER = "troll:sorc"


class Troll:
    """Handles trolls and stuffs"""

    def __init__(self, name: str):
        self.name = str(name)
        self.level = 1
        self.dexterity = 1
        self.critical_hit_chance = 0.0
        self.strength = 1
        self.magic = 1
        self.intelligence = 1
        self.armor = 1
        self.base_life = 100
        self.life = self.base_life
        self.troll_class = "none"
        self.exp = 0

    def init_class(self, troll_class: str):
        """Initiates Troll class, modifying atributes"""
        if self.troll_class == "none" and troll_class is not None:
            if troll_class == "random":
                r_int = random.randint(1, 3)
                if r_int == 1:
                    troll_class = TROLL_ROGUE
                elif r_int == 2:
                    troll_class = TROLL_SORCERER
                elif r_int == 3:
                    troll_class = TROLL_WARRIOR
            self.troll_class = troll_class
            if troll_class == TROLL_ROGUE:
                self.dexterity *= 1.6
            elif troll_class == TROLL_SORCERER:
                self.magic *= 1.6
            elif troll_class == TROLL_WARRIOR:
                self.strength *= 1.6
            else:
                raise ValueError("Specified class does not exist!")
        else:
            print("troll is already classed or argument is none")

    @classmethod
    def create_classed_troll(cls, troll_class: str, troll_name: str):
        """Creates a new classed troll"""
        new_troll = Troll(troll_name)
        new_troll.init_class(troll_class)
        return new_troll

    @classmethod
    def start_classing(cls, troll):
        """Starts the classing process"""
        print("Troll types: \n1 : Warrior \n2 : Rogue \n3 : Sorcerer")
        usr_class = int(input('Select your class(1-3) and press enter:'))
        if usr_class == 1:
            troll.init_class(TROLL_WARRIOR)
        elif usr_class == 2:
            troll.init_class(TROLL_ROGUE)
        elif usr_class == 3:
            troll.init_class(TROLL_SORCERER)
        else:
            raise ValueError("Specified class does not exist!")

    def add_exp(self, exp):
        self.exp += exp
        self.level = int(math.sqrt(self.exp))
        self.apply_level()

    def apply_level(self):
        if self.troll_class == TROLL_WARRIOR:
            Troll.apply_stats(self, str_mult=1.5, mag_mult=0, dex_mult=1.25, intel_mult=0, life_mult=1.25)
        elif self.troll_class == TROLL_SORCERER:
            Troll.apply_stats(self, str_mult=0, mag_mult=1.5, dex_mult=0, intel_mult=1.4, life_mult=1.1)
        elif self.troll_class == TROLL_ROGUE:
            Troll.apply_stats(self, str_mult=1.3, mag_mult=0, dex_mult=1.4, intel_mult=1.1, life_mult=1.2)
        self.life = self.base_life
        self.critical_hit_chance = numpy.clip(1-(self.strength/self.dexterity), 0, 1)

    @classmethod
    def fight(cls, attacker: "Troll", defender: "Troll"):
        victor = None
        attacker.apply_level()
        defender.apply_level()
        while attacker.life >= 0 and defender.life >= 0:
            print("\n->Attacker's turn")
            Troll.clash(attacker, defender)
            print("\n->Defender's turn")
            Troll.clash(defender, attacker)

        print("\n\n")
        print(
            f"Attacker life : {attacker.life}/{attacker.base_life} "
            f"| Defender life : {defender.life}/{defender.base_life}")
        if attacker.life <= 0:
            print("Victor is " + defender.name)
        else:
            print("Victor is " + attacker.name)

    @classmethod
    def clash(cls, attacker: "Troll", defender: "Troll"):
        if attacker.troll_class == TROLL_WARRIOR or attacker.troll_class == TROLL_ROGUE:
            free_weapon_dmg = 50
            free_armor = 100
            damage = attacker.strength*(free_weapon_dmg/free_armor)
            damage *= 1+random.uniform(-0.25, 0.25)
            damage = int(damage)
            print(attacker.name + "attacks... ", end="", flush=True)
            time.sleep(0.25)

            hit_chance = 0.9*(attacker.dexterity/defender.dexterity)
            hit_fail = random.random() > hit_chance
            if hit_fail:
                print("But " + defender.name + " dodged!!")
            else:
                critical_hit = random.random() < attacker.critical_hit_chance
                if critical_hit:
                    print("CRITICAL HIT!! ", end="", flush=True)
                    damage *= 2
                print(defender.name + " receives " + str(int(damage)) + " damage!")

                defender.life -= damage

    @classmethod
    def apply_stats(cls, arg_troll: "Troll", life_mult=1.25, mag_mult=1.1, dex_mult=1.1, str_mult=1.1, intel_mult=1.1):
        arg_troll.strength = math.pow(arg_troll.level, str_mult)
        arg_troll.dexterity = math.pow(arg_troll.level, dex_mult)
        arg_troll.magic = math.pow(arg_troll.level, mag_mult)
        arg_troll.intelligence = math.pow(arg_troll.level, intel_mult)
        arg_troll.base_life = int(math.pow(arg_troll.level, life_mult) * 10)


    @classmethod
    def apply_npc_tier(cls, npc_troll):
        pass


if __name__ == "__main__":
    c_attacker = Troll("Bully")
    c_defender = Troll("Youngster")
    c_attacker.init_class(TROLL_WARRIOR)
    c_defender.init_class(TROLL_ROGUE)
    random_exp = random.randint(1, 10001)
    c_attacker.add_exp(random_exp)
    c_defender.add_exp(random_exp)
    game.game.troll_info(c_attacker)
    game.game.troll_info(c_defender)
    input("Press enter to continue")
    Troll.fight(c_attacker, c_defender)
    exit()
    USR_NAME = str(input("Name your troll: "))
    USR_TROLL = Troll(USR_NAME)
    print(
        "Do you wish to init your class right away(y/n)? \n\tInit'ing will raise your class's attribute by 60% and speedup exp gain from your class's actions")
    if sys.stdin.read(1) == 'y':
        Troll.start_classing(USR_TROLL)

    testexp = float(input("Insert exp to add"))
    USR_TROLL.add_exp(testexp)
    game.game.troll_info(USR_TROLL)
    game.game.serialize(USR_TROLL, game.TROLL_OTHER_DATA)
    print("test over")

# while(true):

# mytroll = Troll("Don", 22, 55.1, 90, 59, 4000)
# yourtroll = Troll("Bungo", 39, 21.2, 194, 29, 6040)
# Troll.Clash(mytroll, yourtroll)
