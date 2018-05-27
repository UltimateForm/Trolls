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
import random
import sys
import game

TROLL_ROGUE = "troll:rogue"
TROLL_WARRIOR = "troll:warrior"
TROLL_SORCERER = "troll:sorc"


class Troll:
    """Handles trolls and stuffs"""

    def __init__(self, name: str):
        self.name = str(name)
        self.level = 1
        self.dexterly = 1
        self.strenght = 1
        self.magic = 1
        self.intelligence = 1
        self.armor = 1
        self.life = 100
        self.troll_class = "none"
        self.exp = 0.0

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
                self.dexterly *= 1.6
            elif troll_class == TROLL_SORCERER:
                self.magic *= 1.6
            elif troll_class == TROLL_WARRIOR:
                self.strenght *= 1.6
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

    def level_up(self):
        if self.troll_class == TROLL_WARRIOR:
            Troll.level_to(self, self.level+1, str_mult=1.15, mag_mult=1,dex_mult=1.125, intel_mult=1, life_mult=1.16)
        elif self.troll_class == TROLL_SORCERER:
            Troll.level_to(self, self.level+1, str_mult=1, mag_mult=1.14, dex_mult=1, intel_mult=1.135, life_mult=1.13)
        elif self.troll_class == TROLL_ROGUE:
            Troll.level_to(self, self.level+1, str_mult=1.105, mag_mult=1, dex_mult=1.14, intel_mult=1.1, life_mult=1.14)

    @classmethod
    def level_to(cls, arg_troll, level, life_mult=1.25, mag_mult=1.1, dex_mult=1.1, str_mult=1.1, intel_mult = 1.1):
        for i in range(level - arg_troll.level):
            arg_troll.strenght *= str_mult
            arg_troll.dexterly *= dex_mult
            arg_troll.magic *= mag_mult
            arg_troll.intelligence *= intel_mult
            arg_troll.life *= life_mult
            arg_troll.level += 1

    @classmethod
    def apply_npc_tier(cls, npc_troll):
        pass


if __name__ == "__main__":
    USR_NAME = str(input("Name your troll: "))
    USR_TROLL = Troll(USR_NAME)
    print(
        "Do you wish to init your class right away(y/n)? \n\tInit'ing will raise your class's attribute by 60% and speedup exp gain from your class's actions")
    if sys.stdin.read(1) == 'y':
        Troll.start_classing(USR_TROLL)

    testlevel = int(input("Test level>"))
    for i in range(testlevel):
        USR_TROLL.level_up()
    game.game.troll_info(USR_TROLL)
    game.game.serialize(USR_TROLL, game.TROLL_OTHER_DATA)
    print("test over")

# while(true):

# mytroll = Troll("Don", 22, 55.1, 90, 59, 4000)
# yourtroll = Troll("Bungo", 39, 21.2, 194, 29, 6040)
# Troll.Clash(mytroll, yourtroll)
