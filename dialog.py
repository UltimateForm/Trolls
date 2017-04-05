import sys


def dialog(**kwargs):
    main_message = kwargs.get("msg")
    print(main_message)
    if kwargs.get("input"):
        usr_input = str(input())
        return usr_input
