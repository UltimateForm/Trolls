from enum import IntFlag
import game, troll, damage


class ItemTypes(IntFlag):
    SWORD = 1
    MAUL = 2
    AXE = 4
    DAGGER = 8
    BOW = 16
    STAFF = 32
    TOME = 64
    MAGIC_ORB = 128
    WEAPON = SWORD | MAUL | AXE | DAGGER | BOW | STAFF | TOME | MAGIC_ORB
    CHEST_ARMOR = 256
    SHIELD = 512
    HELMET = 1024
    BOOTS = 2048
    GLOVES = 4096
    RING = 8192
    AMULET = 16384
    BELT = 32768
    ARMOR = CHEST_ARMOR | SHIELD | HELMET | BOOTS | GLOVES | RING | AMULET | BELT
    EQUIPABLE = WEAPON | ARMOR
    WORLD_ITEM = 65536

    @classmethod
    def is_weapon(cls, weapon: "ItemTypes"):
        return bool(cls.WEAPON & weapon)

    @classmethod
    def is_armor(cls, gear: "ItemTypes"):
        return bool(cls.ARMOR & gear)

    @classmethod
    def is_equipeable(cls, item: "ItemTypes"):
        return bool(cls.EQUIPABLE & item)


class Item:
    def __init__(self, name: str, i_type: "ItemTypes", level: int, mods: "troll.Mods", **kwargs):
        self.name = name
        self.item_type = i_type
        self.level = level
        self.mods = mods
        self.armor = kwargs.get("armor")
        self.block_chance = kwargs.get("block_chance")
        self.damage = kwargs.get("damage")

        self.primary_damage_type = kwargs.get("primary_damage_type")
        self.secondary_damage_type = kwargs.get("secondary_damage_type")
        self.tertiary_damage_type = kwargs.get("tertiary_damage_type")

        self.fire_resistance = kwargs.get("fire_resistance")
        self.cold_resistance = kwargs.get("cold_resistance")
        self.electric_resistance = kwargs.get("electric_resistance")
        self.weight = kwargs.get("weight")


class Weapon(Item):
    def __init__(self, name: str, level: int, mods: "troll.Mods", w_type: "ItemTypes", damage: float,
                 primary_damage_type: "damage.Damage", secondary_damage_type=None, tertiary_damage_type=None,
                 block_chance=0, weight=1):
        if not ItemTypes.is_weapon(w_type):
            print(f"{name} provided weapon type is not valid, received {w_type}, expected {ItemTypes.WEAPON} or less.")
            return
        super().__init__(name, w_type, level, mods, block_chance=block_chance, damage=damage,
                         primary_damage_type=primary_damage_type, secondary_damage_type=secondary_damage_type,
                         tertiary_damage_type=tertiary_damage_type, weight=weight)


class Armor(Item):
    def __init__(self, name: str, level: int, mods: "troll.Mods", a_type: "ItemTypes", armor: int, fire_resis: float,
                 cold_resis: float, electic_resis: float, block_chance=0, weight=1):
        if not ItemTypes.is_armor(a_type):
            print(f"{name} provided armor type is not valid, received {a_type}, expected {ItemTypes.ARMOR} or less.")
            return
        super().__init__(name, a_type, level, mods, block_chance=block_chance, armor=armor, fire_resistance=fire_resis,
                         cold_resistance=cold_resis, electric_resistance=electic_resis,weight=weight)


if __name__ == "__main__":
    print(ItemTypes.WEAPON.value)
    exit()
    weap = Weapon("Simple sword", 10, troll.Mods(4, 2, 0, 0, 40, 1.5), ItemTypes.AXE, 6515, damage.Damage.PHYSICAL)
    game.Game.weapon_info(weap)

    weap2 = Weapon("Fiery Rod", 10, troll.Mods(0, 0, 5, 1, 10, 0.5), ItemTypes.STAFF, 1231231,
                   damage.Damage.MAGIC | damage.Damage.COLD | damage.Damage.PROJECTILE)
    game.Game.weapon_info(weap2)
    game.Game.serialize(weap2, game.TROLL_ITEMS_DATA)