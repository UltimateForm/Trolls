from enum import IntFlag


class Damage(IntFlag):
    PHYSICAL = 1
    PROJECTILE = 2
    MAGIC = 4
    ELEMENTAL = 8
    FIRE = 16
    COLD = 32
    ELECTRIC = 64
    ARCANE = 128
    AOE = 256

    @classmethod
    def get_name(cls, dmg_type: "Damage"):
        name = ""
        if dmg_type & Damage.AOE:
            name += Damage.AOE.name + " "
        if dmg_type & Damage.MAGIC:
            name += Damage.MAGIC.name + " "
        if dmg_type & Damage.ARCANE:
            name += Damage.ARCANE.name + " "
        if dmg_type & Damage.ELEMENTAL:
            name += Damage.ELEMENTAL.name + " "
        if dmg_type & Damage.ELECTRIC:
            name += Damage.ELECTRIC.name + " "
        if dmg_type & Damage.COLD:
            name += Damage.COLD.name + " "
        if dmg_type & Damage.FIRE:
            name += Damage.FIRE.name + " "
        if dmg_type & Damage.PHYSICAL:
            name += Damage.PHYSICAL.name + " "
        if dmg_type & Damage.PROJECTILE:
            name += Damage.PROJECTILE.name + " "
        return name
