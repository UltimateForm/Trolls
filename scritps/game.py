import dialog as dlg
import bunch
import json
import os

TROLL_NPC_DATA = 1
TROLL_BOSS_DATA = 2
TROLL_OTHER_DATA = 0


class game():
    bosses = []
    DATA_LOCATION = ""
    MAIN_DATA = ""
    PLAYER_DATA = ""
    BOSS_DATA = ""
    FIRST_RUN = False

    @classmethod
    def start(cls):
        game.DATA_LOCATION = os.path.abspath(__file__)[:-7] + "config.cfg"
        game.MAIN_DATA = os.path.abspath(__file__)[:-7] + "data/"
        game.PLAYER_DATA = game.MAIN_DATA + "player/"
        game.BOSS_DATA = game.MAIN_DATA + "bosses/"
        game.FIRST_RUN = not os.path.isfile(game.DATA_LOCATION)
        game.config()
        print("\tWelcome to TROLL!")

    @classmethod
    def config(cls):
        if game.FIRST_RUN:
            dlg.dialog(msg="FIRST RUN")
            with open(game.DATA_LOCATION, "w+") as datafile:
                datafile.write("init=true")
            if not os.path.exists(game.MAIN_DATA):
                os.mkdir(game.MAIN_DATA)
                os.mkdir(game.MAIN_DATA + "bosses/")
                os.mkdir(game.MAIN_DATA + "npcs/")
                os.mkdir(game.MAIN_DATA + "other/")
                os.mkdir(game.MAIN_DATA + "instance/")
                os.mkdir(game.MAIN_DATA + "player/")

    @classmethod
    def troll_info(cls, arg_troll: "troll.Troll"):
        dlg.separate()
        dlg.dialog(msg="Name: " + arg_troll.name)
        dlg.dialog(msg="Level: " + str(arg_troll.attributes.level))
        dlg.dialog(msg="Class: " + arg_troll.attributes.form.name)
        dlg.dialog(msg="Strength: {0}".format(str(round(arg_troll.total_strength, 1))))
        dlg.dialog(msg="Dexterity: {0}".format(str(round(arg_troll.total_dexterity, 1))))
        dlg.dialog(msg="Critical hit chance (phys): {0}%".format(str(round(arg_troll.total_phys_crit_chance*100, 1))))
        dlg.dialog(msg="Magic: {0}".format(str(round(arg_troll.total_magic, 1))))
        dlg.dialog(msg="Intelligence: {0}".format(str(round(arg_troll.total_intelligence, 1))))
        dlg.dialog(msg="Vitality: {0}".format(str(int(arg_troll.attributes.vitality))))
        dlg.separate()

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
        string = json.dumps(arg_troll.__dict__)
        folder = game.MAIN_DATA + "bosses/" if data_type == TROLL_BOSS_DATA else game.MAIN_DATA + "npcs/" if data_type == TROLL_NPC_DATA else game.MAIN_DATA + "other/"
        with open(folder + "{}.json".format(arg_troll.name), "w+") as my_file:
            my_file.write(string + "\n")

    @classmethod
    def deserialize(cls, json_path):
        # with open(path, encoding="utf-8") as json_file:
        #     print(json_file)
        if os.path.isfile(json_path):
            troll_dict = json.loads(open(json_path).read())
            mtroll = bunch.bunchify(troll_dict)
            # dlg.dialog(msg=troll_dict.get("name") + str(troll_dict.get("life:")))
            # game.troll_info(mtroll)
            return mtroll
        elif json_path.endswith(".json"):
            dlg.dialog(msg=json_path + " : File not found!")
        else:
            json_path += ".json"
            return game.deserialize(json_path)

    @classmethod
    def get_boss(cls, file_name):
        return game.deserialize(game.BOSS_DATA + file_name)


game.start()
if __name__ == "__main__":
    game.troll_info(game.get_boss("Bartok"))
