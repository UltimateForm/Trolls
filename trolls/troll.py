import sys
import game
import math
import random
import time
import numpy

TROLL_ROGUE = "Rogue"
TROLL_WARRIOR = "Warrior"
TROLL_SORCERER = "Sorcerer"


class ClassFormula:
    def __init__(self, name, str_mult: float, dex_mult: float, magic_mult: float, intel_mult: float, life_mult: float):
        self.name = name
        self.str_mult = str_mult
        self.dex_mult = dex_mult
        self.magic_mult = magic_mult
        self.intel_mult = intel_mult
        self.life_mult = life_mult


DEVIANT_FORM = ClassFormula("Deviant", str_mult=1.2, dex_mult=1.2, magic_mult=1.2, intel_mult=1.2, life_mult=1.2)
WARRIOR_FORM = ClassFormula(TROLL_WARRIOR, str_mult=1.5, dex_mult=1.25, magic_mult=0, intel_mult=0, life_mult=1.25)
SORCERER_FORM = ClassFormula(TROLL_SORCERER, str_mult=0, dex_mult=0, magic_mult=1.5, intel_mult=1.4, life_mult=1.1)
ROGUE_FORM = ClassFormula(TROLL_ROGUE, str_mult=1.3, dex_mult=1.4, magic_mult=0, intel_mult=1.1, life_mult=1.2)


class Attributes:
    def __init__(self, troll_class: "ClassFormula", exp: int):
        if troll_class is None:
            self._troll_class = DEVIANT_FORM
        else:
            self._troll_class = troll_class
        self._exp = exp

    @property
    def exp(self):
        return self._exp

    @property
    def level(self):
        return int(math.sqrt(self.exp))

    @property
    def form(self):
        return self._troll_class

    @property
    def vitality(self):
        return int(math.pow(self.level, self.form.life_mult) * 10)

    @property
    def physical_critical_hit_chance(self):
        return numpy.clip(1 - (self.strength / self.dexterity), 0, 1)

    @property
    def strength(self):
        return math.pow(self.level, self.form.str_mult)

    @property
    def dexterity(self):
        return math.pow(self.level, self.form.dex_mult)

    @property
    def magic(self):
        return math.pow(self.level, self.form.magic_mult)

    @property
    def intelligence(self):
        return math.pow(self.level, self.form.intel_mult)

    def add_exp(self, exp):
        self._exp += exp

    def change_class(self, new_class: "ClassFormula"):
        self._exp *= 0.25
        self._troll_class = new_class


class Mods:
    def __init__(self, str_bonus: int, dex_bonus: int, mag_bonus: int, int_bonus: int, life_bonus: int,
                 crit_bonus: float):
        self.str_bonus = str_bonus
        self.dex_bonus = dex_bonus
        self.mag_bonus = mag_bonus
        self.int_bonus = int_bonus
        self.life_bonus = life_bonus
        self.crit_bonus = crit_bonus


class Troll:
    """Handles trolls and stuffs"""

    def __init__(self, name: str):
        self.name = str(name)
        self.level = 1
        self.troll_class = DEVIANT_FORM
        self.attributes = Attributes(self.troll_class, 0)
        self.modifiers = Mods(0, 0, 0, 0, 0, 0)
        self.buffs = Mods(0, 0, 0, 0, 0, 0)
        self.armor = 0

    def init_class(self, troll_class: "ClassFormula"):
        """Initiates Troll class, modifying atributes"""
        self.attributes.change_class(troll_class)
        self.troll_class = troll_class

    @property
    def total_strength(self):
        return self.attributes.strength + self.modifiers.str_bonus + self.buffs.str_bonus

    @property
    def total_dexterity(self):
        return self.attributes.dexterity + self.modifiers.dex_bonus + self.buffs.dex_bonus

    @property
    def total_magic(self):
        return self.attributes.magic + self.modifiers.mag_bonus + self.buffs.mag_bonus

    @property
    def total_intelligence(self):
        return self.attributes.intelligence + self.modifiers.int_bonus + self.buffs.int_bonus

    @property
    def total_phys_crit_chance(self):
        return self.attributes.physical_critical_hit_chance + self.modifiers.crit_bonus + self.buffs.crit_bonus

    @property
    def life(self):
        return self.attributes.vitality + self.modifiers.life_bonus + self.buffs.life_bonus

    @classmethod
    def create_classed_troll(cls, troll_class: "ClassFormula", troll_name: str):
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
            troll.init_class(WARRIOR_FORM)
        elif usr_class == 2:
            troll.init_class(ROGUE_FORM)
        elif usr_class == 3:
            troll.init_class(SORCERER_FORM)
        else:
            raise ValueError("Specified class does not exist!")

    def add_exp(self, exp):
        self.attributes.add_exp(exp)

    @classmethod
    def fight(cls, attacker: "Troll", defender: "Troll"):
        while attacker.life >= 0 and defender.life >= 0:
            print("\n->Attacker's turn")
            Troll.clash(attacker, defender)
            print("\n->Defender's turn")
            Troll.clash(defender, attacker)

        print("\n\n")
        print(
            f"Attacker life : {attacker.life}/{attacker.attributes.vitality} "
            f"| Defender life : {defender.life}/{defender.attributes.vitality}")
        if attacker.life <= 0:
            print("Victor is " + defender.name)
        else:
            print("Victor is " + attacker.name)

    @classmethod
    def clash(cls, attacker: "Troll", defender: "Troll"):
        if attacker.troll_class == WARRIOR_FORM or attacker.troll_class == ROGUE_FORM:
            free_weapon_dmg = 500
            free_armor = 1000
            damage = attacker.total_strength * (free_weapon_dmg / free_armor)
            damage *= 1 + random.uniform(-0.25, 0.25)
            damage = int(damage)
            print(attacker.name + "attacks... ", end="", flush=True)
            time.sleep(0.25)

            hit_chance = 0.9 * (attacker.total_dexterity / defender.total_dexterity)
            hit_fail = random.random() > hit_chance
            if hit_fail:
                print("But " + defender.name + " dodged!!")
            else:
                critical_hit = random.random() < attacker.total_phys_crit_chance
                if critical_hit:
                    print("CRITICAL HIT!! ", end="", flush=True)
                    damage *= 2
                print(defender.name + " receives " + str(int(damage)) + " damage!")

                defender.buffs.life_bonus -= damage

    @classmethod
    def apply_npc_tier(cls, npc_troll):
        pass


if __name__ == "__main__":
    c_attacker = Troll("Bully")
    c_defender = Troll("Youngster")
    c_attacker.init_class(WARRIOR_FORM)
    c_defender.init_class(ROGUE_FORM)
    #random_exp = random.randint(1, 10001)
    random_exp = 10000
    print("Will add {0} exp to each troll".format(str(random_exp)))
    c_attacker.add_exp(random_exp)
    c_defender.add_exp(random_exp)
    game.Game.troll_info(c_attacker)
    game.Game.troll_info(c_defender)
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
    game.Game.troll_info(USR_TROLL)
    game.Game.serialize(USR_TROLL, game.TROLL_OTHER_DATA)
    print("test over")

# while(true):

# mytroll = Troll("Don", 22, 55.1, 90, 59, 4000)
# yourtroll = Troll("Bungo", 39, 21.2, 194, 29, 6040)
# Troll.Clash(mytroll, yourtroll)
