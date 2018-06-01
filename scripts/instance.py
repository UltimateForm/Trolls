from scripts import *
import random

TIER_CITIZENS = 1
TIER_THUGS = 2
TIER_MILITIA = 3
TIER_GUARDS = 4
TIER_ARMY = 5
TIER_ALPHAS = 6
class instance:
    def __init__(self, num_trolls : int, tier : int, troll_boss, **kwargs):
        self.num_trolls = num_trolls
        self.tier = tier
        self.troll_boss = troll_boss
        self.mobs = []
        self.process_dungeon()

    def process_dungeon(self):
        for i in range(self.num_trolls):
            rlevel = random.randint(self.tier*10, self.tier*10 +5)
            mob = npc.npc("station_troll" + str(i), troll_class="random", tier=self.tier, level=rlevel)
            game.game.troll_info(mob.troll)
            self.mobs.append(npc)
        troll.Troll.level_to(self.troll_boss.troll, self.tier * 10 + 8, )
        game.game.troll_info(self.troll_boss.troll)


station_mine = instance(4, 1, npc.npc("BOSS!", level=1, tier=6, troll_class=troll.TROLL_WARRIOR))
# data = {"value1" : "data1", "value2":"data2"}
# jsonstring = json.dumps(data)
# with open("/home/subarashi/file.json", "w") as mfile:
#     mfile.write(jsonstring)