import troll
import dialog as dlg


class npc:
    def __init__(self, name, **kwargs):
        troll_class = kwargs.get("troll_class")
        if troll_class is not None:
            self.troll = troll.Troll(name)
            if troll_class != "unclassed":
                self.troll.init_class(troll_class)
                troll_level = kwargs.get("level")
                if troll_level is not None:
                    troll.Troll.level_to(self.troll, troll_level, str_mult=1.19, dex_mult=1.19, mag_mult=1.19)

if __name__ == "__main__":
    my_npc = npc("MYNPC", troll_class=troll.Troll.TROLL_SORCERER, level=10)
    dlg.dialog(msg=my_npc.troll.name + " <troll name")
    dlg.dialog(msg=my_npc.troll.troll_class + " <troll class")
    dlg.dialog(msg=str(my_npc.troll.strenght) + " <troll_str")
    dlg.dialog(msg=str(my_npc.troll.magic) + " <troll_mag")
    dlg.dialog(msg=str(my_npc.troll.dexterly) + " <troll_dex")
    dlg.dialog(msg=str(my_npc.troll.level) + " <troll_level")


