from data.scritps import troll
import game

TIER_CIVILIAN = 1
TIER_INITIATE = 2
TIER_THUG = 3
TIER_RAIDER = 4
TIER_CHIEF = 5
TIER_WARLORD = 6
TIER_ALPHA = 7
class npc:
    def __init__(self, name, **kwargs):
        troll_class = kwargs.get("troll_class")
        if troll_class is not None:
            self.troll = troll.Troll(name)
            if troll_class != "unclassed":
                self.troll.init_class(troll_class)
                troll_level = kwargs.get("level")
                tier = kwargs.get("tier")
                if troll_level is not None:
                    magic_mult = kwargs.get("magic_mult")
                    dexterly_mult = kwargs.get("dexterly_mult")
                    strenght_mult = kwargs.get("strenght_mult")
                    troll.Troll.level_to(self.troll, troll_level,
                                         str_mult=strenght_mult if strenght_mult is not None else 1,
                                         dex_mult=dexterly_mult if dexterly_mult is not None else 1,
                                         mag_mult=magic_mult if magic_mult is not None else 1)

if __name__ == "__main__":
    my_npc = npc("MY_WARRIOR_TROLL", troll_class=troll.TROLL_WARRIOR, level=10)
    game.game.troll_info(my_npc.troll)
    my_npc = npc ("MY_ROGUE_TROLL", troll_class=troll.TROLL_ROGUE, level=10)
    game.game.troll_info (my_npc.troll)
    my_npc = npc ("MY_SORCERER_TROLL", troll_class=troll.TROLL_SORCERER, level=10)
    game.game.troll_info (my_npc.troll)
    game.game.serialize(my_npc.troll, game.TROLL_OTHER_DATA)



