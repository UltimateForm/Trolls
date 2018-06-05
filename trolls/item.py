from enum import IntFlag
import game, troll, damage


WEAPON_FLAG = 128
GEAR_FLAG = 65536


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
    WEAPON = 1024
    HELMET = 2048
    BOOTS = 4096
    GLOVES = 8192
    RING = 16384
    AMULET = 32768
    BELT = 65536
    ARMOR = CHEST_ARMOR | SHIELD | HELMET | BOOTS | GLOVES | RING | AMULET | BELT
    EQUIPABLE = WEAPON | ARMOR
    BASIC_ITEM = 131072

    @classmethod
    def is_weapon(cls, weapon: "ItemTypes"):
        return bool(cls.WEAPON & weapon)

    @classmethod
    def is_armor(cls, gear: "ItemTypes"):
        return bool(cls.ARMOR & gear)

    @classmethod
    def is_equipeable(cls, item: "ItemTypes"):
        return bool(cls.EQUIPABLE & item)


class ItemBase:
    def __init__(self, name: str, type: "ItemTypes", level: int, mods: "troll.Mods"):
        self.name = name
        self.type = type
        self.mods = mods


class Weapon(ItemBase):
    def __init__(self, name: str, level: int, mods: "troll.Mods", type: "ItemTypes", damage: int,
                 damage_type: "damage.Damage"):
        super().__init__(name, level, mods)
        self.damage = damage
        self.type = type
        self.damage_type = damage_type


class Gear(ItemBase):
    def __init__(self, name: str, level: int, mods: "troll.Mods", armor: int, fire_resis: float, cold_resis: float,
                 electic_resis):
        super().__init__(name, level, mods)
        self.armor = armor
        self.fire_resistance = fire_resis
        self.cold_resistance = cold_resis
        self.electric_resistance = electic_resis


if __name__ == "__main__":
    print(ItemTypes(64))
    pass
    weap = Weapon("Simple sword", 10, troll.Mods(4, 2, 0, 0, 40, 1.5), ItemTypes.SWORD, 6515, damage.Damage.PHYSICAL)
    game.Game.weapon_info(weap)

    weap2 = Weapon("Fiery Rod", 10, troll.Mods(0, 0, 5, 1, 10, 0.5), ItemTypes.STAFF, 1231231,
                   damage.Damage.MAGIC | damage.Damage.COLD | damage.Damage.PROJECTILE)
    game.Game.weapon_info(weap2)
    game.Game.serialize(weap2, game.TROLL_OTHER_DATA)
