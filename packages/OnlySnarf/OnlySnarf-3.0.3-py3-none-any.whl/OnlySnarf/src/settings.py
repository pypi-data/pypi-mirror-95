#!/usr/bin/python3
# App Settings
import pkg_resources
import time
from .colorize import colorize
from .args import CONFIG as config
import PyInquirer
import os, json

DEBUGGING = [
    ""
]
CATEGORIES_DEFAULT = [
  "images",
  "galleries",
  "videos",
  "performers"
]
DEFAULT_MESSAGE = ":)"
DEFAULT_REFRESHER = "hi!"
DEFAULT_GREETING = "hi! thanks for subscribing :3 do you have any preferences?"
DISCOUNT_MAX_AMOUNT = 55
DISCOUNT_MIN_AMOUNT = 5
DISCOUNT_MAX_MONTHS = 12
DISCOUNT_MIN_MONTHS = 1
DURATION_ALLOWED = [1,3,7,30,99]
PROMOTION_DURATION_ALLOWED = ["1 day","3 days","7 days","14 days","1 month","3 months","6 months","12 months"]

EXPIRATION_ALLOWED = [1,3,7,30,99]
IMAGE_DOWNLOAD_LIMIT = 6
IMAGE_UPLOAD_LIMIT = 5
IMAGE_UPLOAD_LIMIT_MESSAGES = 5
MESSAGE_CHOICES = ["all", "recent", "favorite", "renew on", "list"]
PRICE_MINIMUM = 3
UPLOAD_MAX_DURATION = 6*6 # increments of 10 minutes; 6 = 1 hr
# 12 = 2 hrs
# 24 = 4 hrs
# 36 = 6 hrs
class Settings:
    ASCII = "\n     ________         .__          _________                     _____ \n \
    \\_____  \\   ____ |  | ___.__./   _____/ ____ _____ ________/ ____\\\n \
     /   |   \\ /    \\|  |<   |  |\\_____  \\ /    \\\\__  \\\\_   _ \\   __\\ \n \
    /    |    \\   |  \\  |_\\___  |/        \\   |  \\/ __ \\ |  |\\/| |   \n \
    \\_______  /___|  /____/ ____/_______  /___|  (____  \\\\__|  |_|   \n \
            \\/     \\/     \\/            \\/     \\/     \\/              \n"

    LAST_UPDATED_KEY = False
    CATEGORY = None
    CONFIRM = True
    FILES = None
    PERFORMER_CATEGORY = None
    PROMPT = True
    VERSION = pkg_resources.get_distribution("onlysnarf").version

    def __init__():
        pass

    #####################
    ##### Functions #####
    #####################

    def confirm(text):
        try:
            if text == None: return False
            if list(text) == []: return False
            if str(text) == "": return False
            if not Settings.CONFIRM: return True
        except: pass
        questions = [
            {
                'type': 'confirm',
                'message': 'Is this correct? -> {}'.format(text),
                'name': 'confirm',
                'default': True,
            }
        ]
        return PyInquirer.prompt(questions)["confirm"]

    def debug_delay_check():
        if Settings.is_debug() and Settings.is_debug_delay():
            time.sleep(int(10))

    def print(text):
        if int(config["VERBOSE"]) >= 1:
            print(colorize(text, "teal"))

    def maybe_print(text):
        if int(config["VERBOSE"]) >= 2:
            print(colorize(text, "teal"))

    # update for verbosity
    def dev_print(text):
        if int(config["VERBOSE"]) >= 3:
            if "successful" in str(text).lower():
                print(colorize(text, "green"))
            elif "failure" in str(text).lower():
                print(colorize(text, "red")) 
            else:
                print(colorize(text, "blue"))

    def err_print(error):
        print("{}: {}".format(colorize("Error","red"), error))

    def warn_print(error):
        print("{}: {}".format(colorize("Warning","yellow"), error))

    def header():
        if Settings.LAST_UPDATED_KEY:
            print("Updated: {} = {}".format(Settings.LAST_UPDATED_KEY, config[Settings.LAST_UPDATED_KEY.replace(" ","_").upper()]))
            print('\r')
        Settings.LAST_UPDATED_KEY = None

    # Gets

    def get_action():
        return config["ACTION"]

    def get_amount():
        return config["AMOUNT"]

    def get_browser_type():
        return config["BROWSER"]

    def get_months():
        return config["MONTHS"]

    def get_category():
        cat = config["CATEGORY"]
        if str(cat) == "image": cat = "images"
        if str(cat) == "gallery": cat = "galleries"
        if str(cat) == "video": cat = "videos"
        if str(cat) == "performer": cat = "performers"
        return cat or None

    def get_category_performer():
        cat = config["PERFORMER_CATEGORY"]
        if str(cat) == "image": cat = "images"
        if str(cat) == "gallery": cat = "galleries"
        if str(cat) == "video": cat = "videos"
        # if str(cat) == "performer": cat = "performers"
        return cat or None

    def get_categories():
        cats = []
        cats.extend(list(CATEGORIES_DEFAULT))
        cats.extend(list(config["CATEGORIES"]))
        return cats

    def get_cookies_path():
        return os.path.join(Settings.get_mount_path(), Settings.get_username(), "cookies.pkl")

    def get_price():
        return config["PRICE"] or ""

    def get_price_minimum():
        return PRICE_MINIMUM or 0

    def get_date():
        return config["DATE"] or None

    def get_default_greeting():
        return DEFAULT_GREETING or ""

    def get_default_refresher():
        return DEFAULT_REFRESHER or ""
        
    def get_discount_max_amount():
        return DISCOUNT_MAX_AMOUNT or 0
        
    def get_discount_min_amount():
        return DISCOUNT_MIN_AMOUNT or 0
        
    def get_discount_max_months():
        return DISCOUNT_MAX_MONTHS or 0
        
    def get_discount_min_months():
        return DISCOUNT_MIN_MONTHS or 0

    def get_download_max():
        return config["DOWNLOAD_MAX"] or IMAGE_DOWNLOAD_LIMIT
        
    def get_drive_ignore():
        return config["NOTKEYWORD"] or None
        
    def get_drive_keyword():
        return config["BYKEYWORD"] or None
        
    def get_duration():
        return config["DURATION"] or None

    def get_promo_duration():
        return config["DURATION_PROMO"] or None
        
    def get_duration_allowed():
        return DURATION_ALLOWED or []
        
    def get_duration_promo_allowed():
        return PROMOTION_DURATION_ALLOWED or []

    def get_expiration():
        return config["EXPIRATION"] or config["PROMOTION_EXPIRATION"] or None
        
    def get_expiration_allowed():
        return EXPIRATION_ALLOWED or []

    def get_input():
        return config["INPUT"] or []

    def get_input_as_files():
        if Settings.FILES: return Settings.FILES
        from .file import File
        files = []
        for file_path in config["INPUT"]:
            file = File()
            setattr(file, "path", file_path)
            files.append(file)
        Settings.FILES = files
        return files

    def get_keywords():
        keywords = config["KEYWORDS"] or []
        keywords = [n.strip() for n in keywords]
        return keywords

    def get_limit():
        return config["LIMIT"] or None

    def get_message_choices():
        return MESSAGE_CHOICES

    def get_mount_path():
        return config["MOUNT_PATH"] or "/opt/onlysnarf"

    def get_sort_method():
        return config["SORT"] or "random"

    def get_performers():
        performers = config["PERFORMERS"] or []
        performers = [n.strip() for n in performers]
        return performers

    def get_profile_path():
        return config["PROFILE_PATH"] or "/opt/onlysnarf/profile.json"

    def get_recent_user_count():
        return config["RECENT_USERS_COUNT"] or 0

    def get_promotion_method():
        return config["PROMOTION_METHOD"] or None

    def get_password():
        return config["PASSWORD"] or ""

    def get_password_google():
        return config["PASSWORD_GOOGLE"] or ""

    def get_password_twitter():
        return config["PASSWORD_TWITTER"] or ""

    def get_download_path():
        return config["DOWNLOAD_PATH"] or ""

    def get_drive_path():
        return config["DRIVE_PATH"] or "root"

    def get_drive_root():
        return config["DRIVE_ROOT"] or "OnlySnarf"

    def get_users_path():
        return config["USERS_PATH"] or "/opt/onlysnarf/users.json"

    def get_config_path():
        return config["CONFIG_PATH"] or ""    

    def get_local_path():
        localPath = os.path.join(Settings.get_mount_path(), Settings.get_username())
        from pathlib import Path
        Path(localPath).mkdir(parents=True, exist_ok=True)
        for cat in Settings.get_categories():
            Path(os.path.join(localPath, cat)).mkdir(parents=True, exist_ok=True)
        return localPath

    def get_google_path():
        return config["GOOGLE_PATH"] or ""

    def get_destination():
        return config["DESTINATION"] or ""

    def get_source():
        return config["SOURCE"] or ""

    def get_source_options():
        return [
            "local",
            "google",
            "dropbox",
            "remote"
        ]

    def get_reconnect_id():
        return config["SESSION_ID"] or ""

    def get_reconnect_url():
        return config["SESSION_URL"] or ""

    def get_remote_host():
        return config["REMOTE_HOST"] or ""

    def get_remote_port():
        return config["REMOTE_PORT"] or 22

    def get_remote_username():
        return config["REMOTE_USERNAME"] or ""

    def get_remote_password():
        return config["REMOTE_PASSWORD"] or ""

    def get_remote_browser_host():
        return config["REMOTE_HOST"] or ""

    def get_remote_browser_port():
        return config["REMOTE_BROWSER_PORT"] or 4444

    def get_secret_path():
        return config["CLIENT_SECRET"] or ""

    def get_profile_method():
        return config["PROFILE_METHOD"] or None

    def get_schedule():
        if str(config["SCHEDULE"]) != "None": return config["SCHEDULE"]
        if Settings.get_date():
            if Settings.get_time():
                config["SCHEDULE"] = "{} {}".format(Settings.get_date(), Settings.get_time())
            else:
                config["SCHEDULE"] = "{}".format(Settings.get_date())
        return config["SCHEDULE"]

    def get_tags():
        tags = config["TAGS"] or []
        tags = [n.strip() for n in tags]
        return tags

    def get_text():
        return config["TEXT"] or None

    def get_time():
        return config["TIME"] or None

    def get_title():
        return config["TITLE"] or None
        
    def get_skipped_users():
        return config["SKIPPED_USERS"] or []
        
    def get_questions():
        return config["QUESTIONS"] or []
        
    def get_upload_max():
        return config["UPLOAD_MAX"] or IMAGE_UPLOAD_LIMIT
        
    # def get_upload_max_messages():
        # return config["UPLOAD_MAX_MESSAGES"] or UPLOAD_MAX_MESSAGES
    def get_login_method():
        return config["LOGIN"] or ""
        
    def get_upload_max_duration():
        return config["UPLOAD_MAX_DURATION"] or UPLOAD_MAX_DURATION # 6 hours

    # comma separated string of usernames
    def get_users():
        users = config["USERS"] or []
        users = [n.strip() for n in users]
        from .user import User
        users_ = []
        for user in users:
            # user = User({})
            user = User({"username":config["USER"]})
            # setattr(user, "username", config["USER"])
            from .driver import Driver
            setattr(user, "driver", Driver.get_driver())
            users_.append(user)
        return users_

    def get_user():
        if not config["USER"]: return None
        from .user import User
        user = User({"username":config["USER"]})
        # setattr(user, "username", config["USER"])
        return user

    def get_email():
        return config["EMAIL"] or ""

    def get_username():
        return config["USERNAME"] or ""

    def get_username_google():
        return config["USERNAME_GOOGLE"] or ""

    def get_username_twitter():
        return config["USERNAME_TWITTER"] or ""

    # def get_users_favorite():
    #     return config["USERS_FAVORITE"] or []
        
    def get_verbosity():
        return config["VERBOSE"] or 0

    def get_version():
        return Settings.VERSION

    def get_performer_category():
        return Settings.PERFORMER_CATEGORY

    def set_performer_category(category):
        Settings.PERFORMER_CATEGORY = category

    def get_user_num():
        return config["USERS_READ"] or 10

    # Bools

    def is_confirm():
        return Settings.CONFIRM or False

    def is_delete_empty():
        return config["DELETE_EMPTY"] or False

    def is_prompt():
        return Settings.PROMPT or False

    def is_create_missing():
        return config["CREATE_MISSING"] or False

    def is_debug():
        return config["DEBUG"] or False

    def is_debug_delay():
        return config["DEBUG_DELAY"] or False

    def is_delete():
        return config["DELETE_GOOGLE"] or False

    def is_force_backup():
        return config["FORCE_BACKUP"] or False

    def is_force_upload():
        return config["FORCE_UPLOAD"] or False

    def is_keep():
        return config["KEEP"] or False

    def is_prefer_local():
        return config["PREFER_LOCAL"] or False
        
    def is_prefer_local_following():
        return config["PREFER_LOCAL_FOLLOWING"] or False

    def is_save_users():
        return config["SAVE_USERS"] or False
        
    def is_reduce():
        return config["ENABLE_REDUCE"] or False
    
    def is_show_window():
        return config["SHOW"] or False

    def is_split():
        return config["ENABLE_SPLIT"] or False
        
    def is_trim():
        return config["ENABLE_TRIM"] or False
        
    def is_tweeting():
        return config["TWEETING"] or False
        
    def is_backup():
        return config["BACKUP"] or False
        
    def is_skip_download():
        return config["SKIP_DOWNLOAD"] or False
        
    def is_skip_upload():
        return config["SKIP_UPLOAD"] or False

        ### OnlySnarf Settings Menu
    def menu():
        skipList = ["action", "amount", "category", "categories", "cron", "input", "messages", "posts", "date", "duration", "expiration", "keywords", "limit", "months", "bykeyword", "notkeyword", "price", "config_path", "google_path", "client_secret", "questions", "schedule", "skipped_users", "tags", "text", "time", "title", "user", "users", "username", "password", "users_favorite"]
        print('Settings')
        keys = [key.replace("_"," ").title() for key in config.keys() if key.lower() not in skipList and "categories" not in str(key).lower() and "messages" not in str(key).lower()]
        keys.insert(0, "Back")
        question = {
            'type': 'list',
            'name': 'choice',
            'message': 'Set:',
            'choices': keys,
            'filter': lambda val: val.lower()
        }
        answer = PyInquirer.prompt(question)["choice"]
        if str(answer).lower() == "back": return
        answer = answer.replace(" ", "_").upper()
        Settings.set_setting(answer)

    def prompt(text):
        if list(text) == []: return False
        if str(text) == "": return False
        if not Settings.PROMPT: return False
        question = {
            'type': 'confirm',
            'message': '{}?'.format(str(text).capitalize()),
            'name': 'confirm',
            'default': True,
        }
        return PyInquirer.prompt(question)["confirm"]

    def prompt_email():
        question = {
            'type': 'input',
            'message': 'Email:',
            'name': 'email'
        }
        email = PyInquirer.prompt(question)["email"]
        Settings.set_email(email)
        return email

    def prompt_username():
        question = {
            'type': 'input',
            'message': 'Username:',
            'name': 'username'
        }
        username = PyInquirer.prompt(question)["username"]
        Settings.set_username(username)
        return username

    def prompt_password():
        question = {
            'type': 'password',
            'message': 'Password:',
            'name': 'password'
        }
        pw = PyInquirer.prompt(question)["password"]
        Settings.set_password(pw)
        return pw

    def prompt_username_google():
        question = {
            'type': 'input',
            'message': 'Google username:',
            'name': 'username'
        }
        username = PyInquirer.prompt(question)["username"]
        Settings.set_username_google(username)
        return username

    def prompt_password_google():
        question = {
            'type': 'password',
            'message': 'Google password:',
            'name': 'password'
        }
        pw = PyInquirer.prompt(question)["password"]
        Settings.set_password_google(pw)
        return pw

    def prompt_username_twitter():
        question = {
            'type': 'input',
            'message': 'Twitter username:',
            'name': 'username'
        }
        username = PyInquirer.prompt(question)["username"]
        Settings.set_username_twitter(username)
        return username

    def prompt_password_twitter():
        question = {
            'type': 'password',
            'message': 'Twitter password:',
            'name': 'password'
        }
        pw = PyInquirer.prompt(question)["password"]
        Settings.set_password_twitter(pw)
        return pw

    def read_session_data():
        Settings.maybe_print("reading local session")
        path_ = os.path.join(Settings.get_mount_path(), "session.json")
        Settings.dev_print("local session path: "+str(path_))
        id_ = None
        url = None
        try:
            with open(str(path_)) as json_file:  
                data = json.load(json_file)
                id_ = data['id']
                url = data['url']
            Settings.maybe_print("loaded local users")
        except Exception as e:
            Settings.dev_print(e)
        return (id_, url)

    def write_session_data(id_, url):
        Settings.maybe_print("writing local session")
        Settings.dev_print("saving session id: {}".format(id_))        
        Settings.dev_print("saving session url: {}".format(url))
        path_ = os.path.join(Settings.get_mount_path(), "session.json")
        Settings.dev_print("local session path: "+str(path_))
        data = {}
        data['id'] = id_
        data['url'] = url
        try:
            with open(str(path_), 'w') as outfile:  
                json.dump(data, outfile, indent=4, sort_keys=True)
        except FileNotFoundError:
            print("Error: Missing Session File")
        except OSError:
            print("Error: Missing Session Path")

    def select_category(categories=None):
        # if Settings.CATEGORY: return Settings.CATEGORY
        if not categories: categories = Settings.get_categories()
        print("Select a Category")
        categories.insert(0, "Back")
        question = {
            'type': 'list',
            'message': 'Category:',
            'name': 'category',
            'choices': categories,
            'filter': lambda cat: cat.lower()
        }
        cat = PyInquirer.prompt(question)["category"]
        if str(cat) == "back": return None
        if not Settings.confirm(cat): return Settings.select_category()
        # Settings.CATEGORY = cat
        config["CATEGORY"] = cat
        return cat

    def set_bycategory(cat):
        config["BYCATEGORY"] = cat

    def set_category(cat):
        config["CATEGORY"] = cat

    def set_confirm(value):
        Settings.CONFIRM = bool(value)

    def set_email(email):
        config["EMAIL"] = str(email)

    def set_username(username):
        config["USERNAME"] = str(username)

    def set_username_google(username):
        config["USERNAME_GOOGLE"] = str(username)

    def set_username_twitter(username):
        config["USERNAME_TWITTER"] = str(username)

    def set_password(password):
        config["PASSWORD"] = str(password)

    def set_password_google(password):
        config["PASSWORD_GOOGLE"] = str(password)

    def set_password_twitter(password):
        config["PASSWORD_TWITTER"] = str(password)

    def set_prefer_local(buul):
        config["PREFER_LOCAL"] = bool(buul)
    
    def set_prefer_local_following(buul):
        config["PREFER_LOCAL_FOLLOWING"] = bool(buul)

    def set_prompt(value):
        Settings.PROMPT = bool(value)

    def set_setting(key):
        value = config[key]
        key = key.replace("_"," ").title()
        print("Current: {}".format(value))
        if str(value) == "True" or str(value) == "False":
            question = {
                'type': 'confirm',
                'name': 'setting',
                'message': "Toggle value?",
                # 'default': int(value)
            }
            answer = PyInquirer.prompt(question)["setting"]
            if not answer: return Settings.menu()
            if value: config[key.upper()] = False
            else: config[key.upper()] = True
        else:
            question = {
                'type': 'input',
                'name': 'setting',
                'message': "New value:",
                # 'default': int(value)
            }
            answer = PyInquirer.prompt(question)["setting"]
            if not Settings.confirm(answer): return Settings.menu()
            config[key.upper()] = answer
        Settings.LAST_UPDATED_KEY = key
        # return Settings.menu()

    def use_cookies():
        return config["COOKIES"] or False

###########################################################################



#     def update_value(self, variable, newValue):
#         variable = str(variable).upper().replace(" ","_")
#         try:
#             # print("Updating: {} = {}".format(variable, newValue))
#             setattr(self, variable, newValue)
#             # print("Updated: {} = {}".format(variable, getattr(self, variable)))
#         except Exception as e:
#             maybePrint(e)

# # move this behavior to user
#     def update_profile_value(self, variable, newValue):
#         variable = str(variable).upper().replace(" ","_")
#         try:
#             # print("Updating: {} = {}".format(variable, newValue))
#             Settings.PROFILE.setattr(self, variable, newValue)
#             # print("Updated: {} = {}".format(variable, getattr(self, variable)))
#         except Exception as e:
#             maybePrint(e)




