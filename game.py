
import dialog as dlg
import random
import json

DATA_LOCATION = ""
FIRST_RUN = False


class game ():
    bosses = []

    @classmethod
    def start(cls):
        print ("\tWelcome to TROLL!")

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
    def serialize(cls , arg_troll):
        """

        :type arg_troll: Troll
        """
        trol_dict = {}
        trol_dict = {"name": arg_troll.name , "class": arg_troll.troll_class , "level": arg_troll.level ,
                     "strenght": arg_troll.strenght , "dexterly": arg_troll.dexterly , "magic": arg_troll.magic ,
                     "intelligence": arg_troll.intelligence , "life:": arg_troll.life , "armor": arg_troll.armor}
        string = json.dumps (trol_dict)
        with open ("/home/subarashi/my_troll.json" , "w") as my_file:
            my_file.write (string + "\n")

    @classmethod
    def deserialize(cls, path):
        # with open(path, encoding="utf-8") as json_file:
        #     print(json_file)
        troll_dict = json.loads(open("/home/subarashi/my_troll.json").read())
        dlg.dialog(msg=troll_dict.get("name") + str(troll_dict.get("life:")))

game.deserialize("/home/subarashi/my_troll.json")
