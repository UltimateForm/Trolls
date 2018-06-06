from enum import IntFlag


class Damage(IntFlag):
    PHYSICAL = 1
    PROJECTILE = 2
    MAGIC = 4
    FIRE = 8
    COLD = 16
    ELECTRIC = 32
    ELEMENTAL = FIRE | COLD | ELECTRIC
    MENTAL = 64
    FORCE = 128
    AOE = 256

    @classmethod
    def get_name(cls, dmg_type: "Damage"):
        name = ""
        if dmg_type & Damage.MENTAL:
            name += Damage.MENTAL.name + " "
        if dmg_type & Damage.AOE:
            name += Damage.AOE.name + " "
        if dmg_type & Damage.MAGIC:
            name += Damage.MAGIC.name + " "
        if dmg_type & Damage.FORCE:
            name += Damage.FORCE.name + " "
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
