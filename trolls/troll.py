import sys
import math
import random
import time
import numpy
import game
import inventory
import item

TROLL_ROGUE = "Rogue"
TROLL_WARRIOR = "Warrior"
TROLL_SORCERER = "Sorcerer"


class ClassFormula:
    def __init__(self, name, weapon_type,
                 str_mult: float, dex_mult: float, magic_mult: float, intel_mult: float, life_mult: float):
        self.name = name
        self.str_mult = str_mult
        self.dex_mult = dex_mult
        self.magic_mult = magic_mult
        self.intel_mult = intel_mult
        self.life_mult = life_mult
        self.weapons = weapon_type


WARRIOR_WEAPON = item.ItemTypes.SWORD | item.ItemTypes.AXE | item.ItemTypes.MAUL
ROGUE_WEAPON = item.ItemTypes.DAGGER | item.ItemTypes.BOW
MAGE_WEAPON = item.ItemTypes.STAFF | item.ItemTypes.MAGIC_ORB | item.ItemTypes.TOME
DEVIANT_FORM = ClassFormula("Deviant", item.ItemTypes.WEAPON,
                            str_mult=1.2, dex_mult=1.2, magic_mult=1.2, intel_mult=1.2, life_mult=1.2)
WARRIOR_FORM = ClassFormula(TROLL_WARRIOR, WARRIOR_WEAPON,
                            str_mult=1.5, dex_mult=1.25, magic_mult=0, intel_mult=0, life_mult=1.25)
SORCERER_FORM = ClassFormula(TROLL_SORCERER, MAGE_WEAPON,
                             str_mult=0, dex_mult=0, magic_mult=1.5, intel_mult=1.4, life_mult=1.1)
ROGUE_FORM = ClassFormula(TROLL_ROGUE, ROGUE_WEAPON,
                          str_mult=1.3, dex_mult=1.4, magic_mult=0, intel_mult=1.1, life_mult=1.2)



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
        return numpy.clip(int(math.sqrt(self.exp)), 1, 100)

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
        return int(math.pow(self.level, self.form.str_mult))

    @property
    def dexterity(self):
        return int(math.pow(self.level, self.form.dex_mult))

    @property
    def magic(self):
        return int(math.pow(self.level, self.form.magic_mult))

    @property
    def intelligence(self):
        return int(math.pow(self.level, self.form.intel_mult))

    def add_exp(self, exp):
        self._exp += exp

    def change_class(self, new_class: "ClassFormula"):
        self._exp *= 0.25
        self._troll_class = new_class


class Mods:
    def __init__(self, str_bonus: int, dex_bonus: int, mag_bonus: int, int_bonus: int, life_bonus: float,
                 crit_bonus: float):
        self.str_bonus = str_bonus
        self.dex_bonus = dex_bonus
        self.mag_bonus = mag_bonus
        self.int_bonus = int_bonus
        self.life_bonus = life_bonus
        self.crit_bonus = crit_bonus

    @classmethod
    def sum(cls, *args: "Mods") -> "Mods":
        str_bonus = 0
        dex_bonus = 0
        mag_bonus = 0
        int_bonus = 0
        life_bonus = 0.0
        crit_bonus = 0.0
        for m in args:
            if m is None:
                continue
            str_bonus += m.str_bonus
            dex_bonus += m.dex_bonus
            mag_bonus += m.mag_bonus
            int_bonus += m.int_bonus
            life_bonus += m.life_bonus
            crit_bonus += m.crit_bonus
        return Mods(str_bonus, dex_bonus, mag_bonus, int_bonus, life_bonus, crit_bonus)

    @classmethod
    def sum_item_mods(cls, *args: "item.Item") -> "Mods":
        modarray = []
        for i in args:
            if i is None:
                continue
            modarray.append(i.mods)
        return cls.sum(*modarray)


class Troll:
    """Handles trolls and stuffs"""

    def __init__(self, name: str):
        self.name = str(name)
        self.troll_class = DEVIANT_FORM
        self.attributes = Attributes(self.troll_class, 0)
        self.modifiers = Mods(0, 0, 0, 0, 0, 0)
        self.buffs = Mods(0, 0, 0, 0, 0, 0)
        self.bag = inventory.Inventory(self)

    def init_class(self, troll_class: "ClassFormula"):
        """Initiates Troll class, modifying atributes"""
        self.attributes.change_class(troll_class)
        self.troll_class = troll_class

    @property
    def level(self):
        return self.attributes.level

    @property
    def total_strength(self):
        return self.attributes.strength + self.total_mods.str_bonus + self.buffs.str_bonus

    @property
    def total_dexterity(self):
        return self.attributes.dexterity + self.total_mods.dex_bonus + self.buffs.dex_bonus

    @property
    def total_magic(self):
        return self.attributes.magic + self.total_mods.mag_bonus + self.buffs.mag_bonus

    @property
    def total_intelligence(self):
        return self.attributes.intelligence + self.total_mods.int_bonus + self.buffs.int_bonus

    @property
    def total_phys_crit_chance(self):
        return self.attributes.physical_critical_hit_chance + self.total_mods.crit_bonus + self.buffs.crit_bonus

    @property
    def life(self):
        return self.attributes.vitality + self.total_mods.life_bonus + self.buffs.life_bonus

    @property
    def total_vitality(self):
        return self.attributes.vitality + self.total_mods.life_bonus

    @property
    def weapon(self):
        return self.bag.equipped_weapon

    @property
    def armor(self):
        return self.bag.equipped_armor

    @property
    def wear_weight(self):
        weight = 0.0
        if self.weapon is not None:
            weight += self.weapon.weight
        if self.armor is not None:
            weight += self.armor.weight
        return weight

    @property
    def total_mods(self):
        item_mods = Mods.sum_item_mods(self.weapon, self.armor)
        total_mods = Mods.sum(self.modifiers, item_mods)
        return total_mods

    def equip(self, it: "item.Item"):
        if not bool(item.ItemTypes.EQUIPABLE & it.item_type):
            print(f"{it.name} is not equipable")
            return
        if isinstance(it, item.Weapon):
            if not bool(self.attributes.form.weapons & it.item_type):
                print(f"{self.attributes.form.name} can't equip weapons of type {it.item_type.name}")
                return
            self.bag.equip_weapon(it)
        elif isinstance(it, item.Armor):
            self.bag.equip_armor(it)
        else:
            print("Could not equip " + str(it.__class__))

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
            damage = attacker.total_strength * (attacker.weapon.damage / defender.armor.armor)
            damage *= 1 + random.uniform(-0.25, 0.25)
            damage = int(damage)
            o_weight_ratio = numpy.clip(1 - (attacker.wear_weight / defender.wear_weight), 0.0, 0.5)
            d_weight_ratio = numpy.clip(1 - (defender.wear_weight / attacker.wear_weight), 0.0, 0.25)
            print(attacker.name + " attacks... ", end="", flush=True)
            time.sleep(0.25)

            hit_chance = attacker.weapon.hit_chance * (attacker.total_dexterity / defender.total_dexterity)
            hit_chance *= 1-d_weight_ratio
            hit_fail = random.random() > hit_chance
            if hit_fail:
                print("But " + defender.name + " dodged!!")
            else:
                block_chance = defender.weapon.block_chance
                blocked = random.random() <= block_chance
                if blocked:
                    print("But " + defender.name + " blocked the attack!!")
                    return
                battle_crit_hit = attacker.total_phys_crit_chance * (1+o_weight_ratio)
                critical_hit = random.random() < battle_crit_hit
                if critical_hit:
                    print("CRITICAL HIT!! ", end="", flush=True)
                    damage *= 2
                print(defender.name + " receives " + str(int(damage)) + " damage!")
                defender.buffs.life_bonus -= damage

    @classmethod
    def apply_npc_tier(cls, npc_troll):
        pass


if __name__ == "__main__":
    inventory.Inventory.populate_world()
    thug = Troll("Jaffa")
    thug.init_class(WARRIOR_FORM)
    thug.add_exp(10 * 10)
    exit()
    thug.equip(inventory.Inventory.WORLDBAG.get_item_by_id(9))
    thug.equip(inventory.Inventory.WORLDBAG.get_item_by_id(16))
    game.Game.troll_info(thug)

    thief = Troll("Yuri")
    thief.init_class(ROGUE_FORM)
    thief.add_exp(10 * 10)
    thief.equip(inventory.Inventory.WORLDBAG.get_item_by_id(18))
    thief.equip(inventory.Inventory.WORLDBAG.get_item_by_id(17))
    game.Game.troll_info(thief)

    input("Press enter to continue")

    Troll.fight(thug, thief)
    exit()
    c_attacker = Troll("Bully")
    c_defender = Troll("Youngster")
    c_attacker.init_class(WARRIOR_FORM)
    c_defender.init_class(ROGUE_FORM)
    # random_exp = random.randint(1, 10001)
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
