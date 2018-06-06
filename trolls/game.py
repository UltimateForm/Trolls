import troll, dialog, item, damage
import jsonpickle
import os

TROLL_NPC_DATA = 1
TROLL_BOSS_DATA = 2
TROLL_OTHER_DATA = 0
TROLL_ITEMS_DATA = 3


class Game:
    bosses = []
    DATA_LOCATION = ""
    MAIN_DATA = ""
    PLAYER_DATA = ""
    BOSS_DATA = ""
    FIRST_RUN = False

    @classmethod
    def start(cls):
        Game.DATA_LOCATION = os.path.abspath(__file__)[:-8] + "config.cfg"
        Game.MAIN_DATA = os.path.abspath(__file__)[:-8] + "data/"
        Game.PLAYER_DATA = Game.MAIN_DATA + "player/"
        Game.BOSS_DATA = Game.MAIN_DATA + "bosses/"
        Game.ITEMS_DATA = Game.MAIN_DATA + "item/"
        Game.FIRST_RUN = not os.path.isfile(Game.DATA_LOCATION)
        Game.config()
        print("\tWelcome to TROLL!")

    @classmethod
    def config(cls):
        if Game.FIRST_RUN:
            dialog.dialog(msg="FIRST RUN")
            with open(Game.DATA_LOCATION, "w+") as datafile:
                datafile.write("init=true")
            if not os.path.exists(Game.MAIN_DATA):
                os.mkdir(Game.MAIN_DATA)
                os.mkdir(Game.MAIN_DATA + "bosses/")
                os.mkdir(Game.MAIN_DATA + "npcs/")
                os.mkdir(Game.MAIN_DATA + "other/")
                os.mkdir(Game.MAIN_DATA + "instance/")
                os.mkdir(Game.MAIN_DATA + "player/")

    @classmethod
    def troll_info(cls, arg_troll: "troll.Troll"):
        dialog.separate()
        dialog.dialog(msg="Name: " + arg_troll.name)
        dialog.dialog(msg="Level: " + str(arg_troll.attributes.level))
        dialog.dialog(msg="Class: " + arg_troll.attributes.form.name)
        dialog.dialog(msg="Strength: {0}".format(str(round(arg_troll.total_strength, 1))))
        dialog.dialog(msg="Dexterity: {0}".format(str(round(arg_troll.total_dexterity, 1))))
        dialog.dialog(
            msg="Critical hit chance (phys): {0}%".format(str(round(arg_troll.total_phys_crit_chance * 100, 1))))
        dialog.dialog(msg="Magic: {0}".format(str(round(arg_troll.total_magic, 1))))
        dialog.dialog(msg="Intelligence: {0}".format(str(round(arg_troll.total_intelligence, 1))))
        dialog.dialog(msg="Vitality: {0}".format(str(int(arg_troll.attributes.vitality))))
        dialog.separate()

    @classmethod
    def weapon_info(cls, arg_item: "item.Weapon"):
        dialog.separate()
        dialog.dialog(msg=f"Type: {arg_item.item_type.name}\n"
                          f"Name: {arg_item.name}\n"
                          f"Damage: {arg_item.damage} {damage.Damage.get_name(arg_item.damage_type)}\n"
                          f"\tMods:\n"
                          f"\t\tStrength: {str(arg_item.mods.str_bonus)}\n"
                          f"\t\tDexterity: {str(arg_item.mods.dex_bonus)}\n"
                          f"\t\tMagic: {str(arg_item.mods.mag_bonus)}\n"
                          f"\t\tIntelligence: {str(arg_item.mods.int_bonus)}\n"
                          f"\t\tCrit. Chance: {str(arg_item.mods.crit_bonus)}\n"
                          f"\t\tLife: {str(arg_item.mods.life_bonus)}\n"
                          f"Level: {arg_item.level}")

    @classmethod
    def gear_info(cls, arg_item : "item.Gear"):
        pass

    @classmethod
    def serialize(cls, arg_troll, data_type):
        """

        :type arg_troll: Troll
        :type data_type: int
        """
        # trol_dict = {}
        # trol_dict = {"name": arg_troll.name , "class": arg_troll.troll_class , "level": arg_troll.level ,
        #              "strength": arg_troll.strength , "dexterity": arg_troll.dexterity , "magic": arg_troll.magic ,
        #              "intelligence": arg_troll.intelligence , "life:": arg_troll.life , "armor": arg_troll.armor}
        string = jsonpickle.encode(arg_troll)
        folder = Game.MAIN_DATA + "bosses/" if data_type == TROLL_BOSS_DATA else Game.MAIN_DATA + "npcs/" if data_type == TROLL_NPC_DATA else Game.MAIN_DATA + "other/"
        with open(folder + "{}.json".format(arg_troll.name), "w+") as my_file:
            my_file.write(string + "\n")

    @classmethod
    def deserialize(cls, json_path):
        # with open(path, encoding="utf-8") as json_file:
        #     print(json_file)
        if os.path.isfile(json_path):
            mtroll = jsonpickle.decode(open(json_path).read())
            # dlg.dialog(msg=troll_dict.get("name") + str(troll_dict.get("life:")))
            # Game.troll_info(mtroll)
            return mtroll
        elif json_path.endswith(".json"):
            dialog.dialog(msg=json_path + " : File not found!")
        else:
            json_path += ".json"
            return Game.deserialize(json_path)

    @classmethod
    def get_boss(cls, file_name):
        return Game.deserialize(Game.BOSS_DATA + file_name)


Game.start()
