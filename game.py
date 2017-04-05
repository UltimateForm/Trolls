import troll
import dialog

DATA_LOCATION = ""
FIRST_RUN = False
class game():

    @classmethod
    def start(cls):
        print("\tWelcome to TROLL!")


ss = dialog.dialog(msg="Test question? (y/n)", input=True)
print("Answer was: ", ss)
ss = dialog.dialog(msg="Test warning.")
print("Answer was: ", ss)