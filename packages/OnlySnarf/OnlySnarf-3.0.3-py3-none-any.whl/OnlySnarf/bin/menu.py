#!/usr/bin/python3
# Snarf.py menu system
import time
import random
import os
import shutil
import datetime
import json
import sys
import pathlib
from PyInquirer import prompt
##
# from OnlySnarf.src.cron import Cron
from OnlySnarf.src.colorize import colorize
from OnlySnarf.src.classes import Discount, Promotion, Message
from OnlySnarf.src.profile import Profile
from OnlySnarf.src.settings import Settings
from OnlySnarf.src import google as Google
from OnlySnarf.src import args

#####################
##### Functions #####
#####################

class Menu:

    def __init__(self):
        pass

    # Action

    def ask_action():
        options = ["back"]
        options.extend(args.ACTIONS)
        menu_prompt = {
            'type': 'list',
            'name': 'action',
            'message': 'Please select an action:',
            'choices': [str(option).title() for option in options],
            'filter': lambda val: str(val).lower()
        }
        menu_prompt["choices"].sort()
        answers = prompt(menu_prompt)
        return answers['action']

    def action_menu():
        action = Menu.ask_action()
        if (action == 'back'): return Menu.main()
        elif (action == 'discount'): Discount.create()
        elif (action == 'message'): Message.Send()
        elif (action == 'post'): Message.Post()
        elif (action == 'promotion'): Promotion.menu()
        else: print("Missing Action: {}".format(colorize(action,"red")))
        Menu.main()
        
    # Main

    def header():
        if not Settings.is_debug(): os.system('clear')
        print(colorize(Settings.ASCII, 'header'))
        print(colorize('version {}\n'.format(Settings.get_version()), 'green'))
        Menu.user_header()
        Menu.settings_header()

    def settings_header():
        Settings.header()

    def user_header():
        print("User:")
        if Settings.get_email() != "":
            print(" - Email = {}".format(Settings.get_email()))
        print(" - Username = {}".format(Settings.get_username()))
        pass_ = ""
        if str(Settings.get_password()) != "":
            pass_ = "******"
        print(" - Password = {}".format(pass_))
        if str(Settings.get_username_twitter()) != "":
            print(" - Twitter = {}".format(Settings.get_username_twitter()))
            pass_ = ""
            if str(Settings.get_password_twitter()) != "":
                pass_ = "******"
            print(" - Password = {}".format(pass_))
        print('\r')

    def menu():
        menu_prompt = {
            'type': 'list',
            'name': 'menu',
            'message': 'Please select an option:',
            'choices': ['Action', 'Profile', 'Settings', 'Exit']
        }
        answers = prompt(menu_prompt)
        return answers['menu']

    def main_menu():
        action = Menu.menu()
        if (action == 'Action'): Menu.action_menu()
        elif (action == 'Profile'): Profile.menu()
        elif (action == 'Settings'): Settings.menu()
        else: exit()
        Menu.main_menu()

    def main():
        time.sleep(1)
        try:
            Menu.header()
            Menu.settings_header()
            Menu.main_menu()
        except Exception as e:
            Settings.dev_print(e)

#################################################################################################

import atexit
def exit_handler():
    print("Shnarrf?")
    exit()
atexit.register(exit_handler)

import signal
def signal_handler(sig, frame):
    print('Shnnnarf?')
    exit()
signal.signal(signal.SIGINT, signal_handler)
  
def exit():
    from OnlySnarf.src.driver import Driver
    Driver.exit_all()
    sys.exit(0)

######################################################

def main():
    Menu.main()

if __name__ == "__main__":
    try:
        menu = Menu()
        menu.main()
    except Exception as e:
        print("Shhhhhnnnnnarf!")
    finally:
        exit()