from enum import IntFlag


class DamageTypes(IntFlag):
    PHYSICAL = 0
    PROJECTILE = 1
    MAGIC = 2
    ELEMENTAL = 4
    FIRE = 8
    COLD = 16
    ELECTRIC = 32
    ARCANE = 64
    AOE = 128
