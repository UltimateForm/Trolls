import dialog as dlg
import random
import bunch
from bunch.bunch import bunchify
import json
import platform
import os
import glob





TROLL_NPC_DATA = 1
TROLL_BOSS_DATA = 2
TROLL_OTHER_DATA = 0
class game ():
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
                os.mkdir (game.MAIN_DATA + "player/")

    @classmethod
    def troll_info(cls , arg_troll):
        dlg.separate ()
        dlg.dialog (msg=arg_troll.name + " <<<troll name")
        dlg.dialog (msg=arg_troll.troll_class + " <troll class")
        dlg.dialog (msg=str (round (arg_troll.strenght , 1)) + " <troll_str")
        dlg.dialog (msg=str (round (arg_troll.magic , 1)) + " <troll_mag")
        dlg.dialog (msg=str (round (arg_troll.dexterly , 1)) + " <troll_dex")
        dlg.dialog (msg=str (round (arg_troll.intelligence , 1)) + " <troll_int")
        dlg.dialog (msg=str (round (arg_troll.armor , 1)) + " <troll_armor")
        dlg.dialog (msg=str (round (arg_troll.life)) + " <troll_life")
        dlg.dialog (msg=str (round (arg_troll.level , 1)) + " <troll_level")
        dlg.separate ()

    @classmethod
    def serialize(cls , arg_troll, data_type):
        """

        :type arg_troll: Troll
        :type data_type: int
        """
        # trol_dict = {}
        # trol_dict = {"name": arg_troll.name , "class": arg_troll.troll_class , "level": arg_troll.level ,
        #              "strenght": arg_troll.strenght , "dexterly": arg_troll.dexterly , "magic": arg_troll.magic ,
        #              "intelligence": arg_troll.intelligence , "life:": arg_troll.life , "armor": arg_troll.armor}
        string = json.dumps (arg_troll.__dict__)
        folder = game.MAIN_DATA + "bosses/" if data_type == TROLL_BOSS_DATA else game.MAIN_DATA + "npcs/" if data_type == TROLL_NPC_DATA else game.MAIN_DATA + "other/"
        with open (folder+ "{}.json".format(arg_troll.name) , "w+") as my_file:
            my_file.write (string + "\n")

    @classmethod
    def deserialize(cls, json_path):
        # with open(path, encoding="utf-8") as json_file:
        #     print(json_file)
        if os.path.isfile(json_path):
            troll_dict = json.loads (open (json_path).read ())
            mtroll = bunchify (troll_dict)
            # dlg.dialog(msg=troll_dict.get("name") + str(troll_dict.get("life:")))
            # game.troll_info(mtroll)
            return mtroll
        elif json_path.endswith(".json"):
            dlg.dialog(msg= json_path + " : File not found!")
        else:
            json_path+=".json"
            return game.deserialize(json_path)

    @classmethod
    def get_boss(cls, file_name):
        return game.deserialize(game.BOSS_DATA + file_name)

game.start()
game.troll_info(game.get_boss("Bartok"))