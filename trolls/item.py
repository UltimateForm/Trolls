from enum import Enum
import game, troll, damage


class WeaponTypes(Enum):
    FISTS = 0
    SWORD = 1
    MAUL = 2
    AXE = 4
    DAGGER = 8
    BOW = 16
    STAFF = 32
    TOME = 64
    MAGIC_ORB = 128


class ItemTypes(Enum):
    CHEST_ARMOR = 0
    WEAPON = 1
    HELMET = 2
    BOOTS = 4
    GLOVES = 8
    RING = 16
    AMULET = 32
    BELT = 64


class ItemBase:
    def __init__(self, name: str, level: int, mods: "troll.Mods"):
        self.level = level
        self.mods = mods
        self.name = name


class Weapon(ItemBase):
    def __init__(self, name: str, level: int, mods: "troll.Mods", type: "WeaponTypes", damage: int,
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
    weap = Weapon("Simple sword", 10, troll.Mods(4, 2, 0, 0, 40, 1.5), WeaponTypes.SWORD, 65, damage.Damage.PHYSICAL)
    game.Game.weapon_info(weap)

    weap2 = Weapon("Fiery Rod", 10, troll.Mods(0, 0, 5, 1, 10, 0.5), WeaponTypes.STAFF, 120,
                   damage.Damage.MAGIC | damage.Damage.COLD | damage.Damage.PROJECTILE)
    game.Game.weapon_info(weap2)
    game.Game.serialize(weap2, game.TROLL_OTHER_DATA)
