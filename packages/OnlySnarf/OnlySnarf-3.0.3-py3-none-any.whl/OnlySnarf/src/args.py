import argparse, os, re
from datetime import datetime
from .validators import valid_action, valid_amount, valid_promo_duration, valid_date, valid_limit, valid_time, valid_price, valid_duration, valid_expiration, valid_schedule, valid_month, valid_path

ACTIONS = ['bot','discount','message','post','profile','promotion', 
'test'
]

CATEGORIES_DEFAULT = [
  "images",
  "galleries",
  "videos"
]
DEFAULT_MESSAGE = ":)"
DEFAULT_GREETING = "hi! thanks for subscribing :3 do you have any preferences?"
DISCOUNT_MAX_AMOUNT = 55
DISCOUNT_MIN_AMOUNT = 10
DISCOUNT_MAX_MONTHS = 7
DISCOUNT_MIN_MONTHS = 1
EXPIRATION_ALLOWED = [1,3,7,30,99]
IMAGE_DOWNLOAD_LIMIT = 6
IMAGE_UPLOAD_LIMIT = 5
MESSAGE_CHOICES = ["all", "recent", "favorite", "renew on"]
PRICE_MINIMUM = 3
UPLOAD_MAX_DURATION = 6*6 # increments of 10 minutes; 6 = 1 hr
DURATION_ALLOWED = [1,3,7,30,99]
LIMIT_ALLOWED = [0,1,2,3,4,5,6,7,8,9,10,20,30,40,50,60,70,80,90,100]
PROMOTION_EXPIRATION_ALLOWED = [int(i) for i in range(30)]
PROMOTION_EXPIRATION_ALLOWED.insert(0,0)
PROMOTION_OFFER_LIMIT = [0,1,2,3,4,5,6,7,8,9,10]
PROMOTION_DURATION_ALLOWED = ["1 day","3 days","7 days","14 days","1 month","3 months","6 months","12 months"]

# Paths
MOUNT_PATH = "/opt/onlysnarf"
DOWNLOAD_PATH = os.path.join(MOUNT_PATH, "downloads")
CONFIG_PATH = os.path.join(MOUNT_PATH, "config.conf")
GOOGLE_PATH = os.path.join(MOUNT_PATH, "google_creds.txt")
SECRET_PATH = os.path.join(MOUNT_PATH, "client_secrets.json")
USERS_PATH = os.path.join(MOUNT_PATH, "users.json")
PROFILE_PATH = os.path.join(MOUNT_PATH, "profile.json")

# from pathlib import Path
# Path(MOUNT_PATH).mkdir(parents=True)

class AttrDict(dict):
  def __init__(self):
    dict.__init__(self)
  # Override getattr and setattr so that they return the values of getitem / setitem
  def __setattr__(self, name, value):
    self[name] = value
  def __getattr__(self, name):
    return self[name]

# overwrites args with config parameters
def read_config(args):
  conf = False 
  if os.path.exists(CONFIG_PATH):
    conf = CONFIG_PATH
  if os.path.exists(args.get("CONFIG_PATH")):
    conf = CONFIG_PATH
  if not conf: return args
  POSTS = AttrDict()
  with open(conf) as f:
    for line in f:
      if str(line[0]) == "#" or len(line) <= 1: continue
      try:
        if "\"" in str(line):
          spl = re.split("\"*\"", line)
          key = spl[0] or None
          val = spl[1] or None
        else:
          (key, val) = line.split()
        key = key.strip()
        if str(val)[0] == "\"": val = str(val[1:])
        if str(val)[len(val)-1] == "\"": val = str(val[:len(val)-1])
        # print("{} : {} ".format(key.upper(),val))
        if "_post" in key: 
          setattr(POSTS, key.upper().replace("_post",""), val)
        else: 
          # setattr(args, key.upper(), val)
          # args.set(key.upper(), val)
          args[key.upper()] = val
      except Exception as e:
        print("Warning: Error Parsing Config")
        print(e)
        # pass
  # args.set("POSTS", POSTS)
  args["POSTS"] = POSTS
  return args

##
# Argument Parser
##

parser = argparse.ArgumentParser(prog='OnlySnarf', allow_abbrev=False, epilog="Shnarrf!", 
  description='Post or send messages to OnlyFans.')
# mutually exclusive
# duration & expiration
durationAndExpiration = parser.add_mutually_exclusive_group()
# schedule and date&time
# scheduleAndDate = parser.add_mutually_exclusive_group()
# scheduleAndTime = parser.add_mutually_exclusive_group()
# discount and amount&duration
#
# -action
# the action to be performed
parser.add_argument('-action', type=valid_action, dest='action',
  help='the action to take', choices=ACTIONS, default='post')
##
# -amount
# action: discount
# the amount to discount a user by
parser.add_argument('-amount', type=valid_amount, dest='amount',
  help='the amount (%%) to discount by', default=None)
##
# -backup
# backup uploaded content to "posted" folder
parser.add_argument('-backup', action='store_true', dest='backup',
  help='enables backup processes')
##
# -browser
parser.add_argument('-browser', type=str, default="auto", choices=["auto","google","firefox","auto-remote","remote","remote-chrome","remote-firefox","reconnect"], dest='browser',
  help='the browser to use')
##
# -category
# the category of folder to upload from
parser.add_argument('-category', default=None, dest='category',
  help='the category of content to post or message')
##
# -category-performer
# the category of folder to upload of a performer
parser.add_argument('-category-performer', default=None, dest='performer_category',
  help='the category of content to post or message of a performer')
##
# configurable w/ profile.conf
# OnlySnarf Drive folder list, appends to defaults
parser.add_argument('-categories', dest='categories',
  action='append', help='the categories to list in menu (appends to \'{}\''.format("\'".join(CATEGORIES_DEFAULT)), 
  default=[])
##
# -cookies
# load & save from/to local cookies path
parser.add_argument('-cookies', action='store_true', dest='cookies',
  help='enable loading & saving from/to the local cookies path')
##
# -create-missing 
# creates missing OnlySnarf folders
parser.add_argument('-create-missing', action='store_true', dest='create_missing',
  help='creates missing OnlySnarf folders at target source')
##
# -cron
# determines whether script running is a cronjob
parser.add_argument('-cron', action='store_true', help='toggle cron behavior', dest='cron')
##
# -cron-user
# the user to run OnlySnarf as
parser.add_argument('-cron-user', type=str, dest='cron_user',
  help='the user to run OnlySnarf as', default='root')
##
# -date
# date in MM-DD-YYYY
parser.add_argument('-date', type=valid_date, default=None, dest='date',
  help='schedule date (MM-DD-YYYY)')
##
# -debug
# debugging - skips uploading and deleting unless otherwise forced
parser.add_argument('-debug', action='store_true', dest='debug',
  help='enable debugging')
##
# -debug-force-save
# forces expiration and poll modals to save instead of cancel when debugging
# parser.add_argument('-debug-force-save', action='store_true',
  # help='force expiration and poll to save when debugging')
##
# -debug-delay
# user message delay
parser.add_argument('-debug-delay', action='store_true', dest='debug_delay',
  help='enable a wait between crucial steps for debugging')
##
# -delete-empty
# delete empty content folders
parser.add_argument('-delete-empty', action='store_true', dest='delete_empty',
  help='delete empty content folders')
##
# -delete-google
# delete uploaded content instaed of backing it up
parser.add_argument('-delete-google', action='store_true', dest='delete_google',
  help='delete file instead of backing up')
##
# -destination
# the destination to use when backing up content
parser.add_argument('-destination', dest='destination', default=None, choices=["google",
  # "dropbox",
  "remote","local"],
  help='file backup location. prefers $source if specified')
##
# -discount
# create a format validator for discount where its "[amount]:[duration]"
# parser.add_argument('-discount', metavar='discount', type=valid_discount, default=None,
  # help='discount to apply in format [amount]:[duration]')
##
# download path
parser.add_argument('-download-path', type=str, dest='download_path',
  help='the path to download files to locally', default=DOWNLOAD_PATH)
##
# -duration
# poll duration
parser.add_argument('-duration', type=valid_duration, dest='duration',
  help='the duration in days (99 for \'No Limit\') for a poll', choices=DURATION_ALLOWED, default=None)
##
# -duration-promo
# promotion duration
parser.add_argument('-duration-promo', type=valid_promo_duration, dest='duration_promo',
  help='the duration in days (99 for \'No Limit\') for a promotion', choices=PROMOTION_DURATION_ALLOWED, default=None)
##
# -email
# the OnlyFans email to use for login
parser.add_argument('-email', type=str, default="", dest='email',
  help='the OnlyFans email')
##
# -promotion-expiration
# expiration for a promotion
parser.add_argument('-promotion-expiration', type=int, dest='promotion_expiration',
  help='the promotions expiration in days)', choices=PROMOTION_EXPIRATION_ALLOWED, default=None)
##
# -expiration
# date of post or poll expiration
parser.add_argument('-expiration', type=int, dest='expiration',
  help='the expiration in days (99 for \'No Limit\')', choices=EXPIRATION_ALLOWED, default=None)
##
# -force-backup
# force backup during debugging
parser.add_argument('-force-backup', action='store_true', dest='force_backup',
  help='force backup when debugging')
##
# -force-upload
# ignore upload max wait
parser.add_argument('-force-upload', action='store_true', dest='force_upload',
  help='ignore upload max wait attempts')
##
# -download-max
# maximum number of images to download
parser.add_argument('-download-max', type=int, default=IMAGE_DOWNLOAD_LIMIT, dest="download_limit",
  help='the max number of images to download')
##
# -upload-max
# maximum number of images that can be uploaded
parser.add_argument('-upload-max', type=int, default=IMAGE_UPLOAD_LIMIT, dest='upload_max',
  help='the max number of images to upload')
##
# -keep
# keep the browser window open
parser.add_argument('-keep', action='store_true', dest='keep',
  help='keep the browser window open after script ends')
##
# -keywords
# keywords to # in post
parser.add_argument('-keywords', dest='keywords', action='append', default=[], 
  help="the keywords (#[keyword])")
##
# -limit
# maximum number of subscribers for a promotion
parser.add_argument('-limit', type=valid_limit, default=None, dest='limit', choices=LIMIT_ALLOWED,
  help='the max number of subscribers allowed for a promotion')
##
# -login
# the method to prefer when logging in
parser.add_argument('-login', dest='login', default="auto", choices=["auto","onlyfans","twitter","google"],
  help='the method of login to prefer')
##
# -months
# action: discount
# the number of months to discount for
parser.add_argument('-months', type=valid_month, default=None, dest='months',
  help='the number of months to discount or apply promotion')
##
# -mount-path
# the mounth path for a local directory of OnlyFans config files
parser.add_argument('-mount-path', dest='mount_path',
  help='the local path to OnlySnarf processes')
##
# -bykeyword
# the keyword to search for in folder selection
parser.add_argument('-bykeyword', dest='bykeyword', default=None, 
  help="search for folder by keyword")
##
# -notkeyword
# the keyword to skip in folder selection
parser.add_argument('-notkeyword', dest='notkeyword', default=None,
  help="search for folder not by keyword")
##
# -password
# the password for OnlyFans
parser.add_argument('-password', type=str, dest='password',
  help='the OnlyFans password for login')
##
# -password
# the password for Google
parser.add_argument('-password-google', type=str, dest='password_google',
  help='the Google password for login')
##
# -password
# the password for Twitter
parser.add_argument('-password-twitter', type=str, dest='password_twitter',
  help='the Twitter password for login')
##
# -performers
# list of performers to tag in post
parser.add_argument('-performers', dest='performers', action='append',  default=[],
  help='the performers to list (w/ @[performer]')
# -prefer-local
# prefers local user cache over refreshing first call
parser.add_argument('-prefer-local', action='store_true', dest='prefer_local',
  help='prefer recently cached data')
# -prefer-local-following
# prefers local user cache over refreshing first call for following
parser.add_argument('-prefer-local-following', action='store_true', dest='prefer_local_following',
  help='prefer recently cached data for following')
# -prefer-local-following
# prefers local user cache over refreshing first call for following
# parser.add_argument('-prefer-local-following', action='store_true', dest='prefer_local_following',
#   help='prefer recently cached data for following')
##
# -price
# the price to be set in a message
parser.add_argument('-price', type=valid_price, help='the price', default=0, dest='price')
## 
# -profile-method
parser.add_argument('-profile-method', dest="profile_method", default="syncfrom", choices=["syncto","syncfrom"],
  help='the profile method to use')
##
# -promotion
# the promotion method to use
parser.add_argument('-promotion-method', dest='promotion_method', default="campaign", choices=["campaign","trial","grandfather","user"],
  help='the method of promotion to use')
###
### PATHS ###
# -drive-path
# the folder path within Google Drive for OnlySnarf's root folder
parser.add_argument('-drive-path', dest="drive_path", type=str, 
  help='the folder path within Drive to root OnlySnarf (/OnlySnarf)')
# -config-path
# the path to the config.conf file
parser.add_argument('-config-path', dest="config_path", type=str, 
  help='the path to the config.conf', default=CONFIG_PATH)
# -google-path
# the path to the google_creds.txt
parser.add_argument('-google-creds', dest="google_path", type=str, 
  help='the path to Google credentials', default=GOOGLE_PATH)
# the path to the client_secret.json
parser.add_argument('-client-secret', dest="client_secret", type=str, 
  help='the path to Google secret credentials', default=SECRET_PATH)
# -user-path
# the path to the users.json file
parser.add_argument('-users-path', type=str, dest='users_path',
  help='the path to cache users locally', default=USERS_PATH)
# -profile-path
# the path to the profile.json file
parser.add_argument('-profile-path', type=str, dest='profile_path',
  help='the path to cache profile locally', default=PROFILE_PATH)
##
# -remote-host
# the remote host to connect to
parser.add_argument('-remote-host', type=str, dest='remote_host',
  help='the remote host to connect to', default="127.0.0.1")
##
# -remote-browser-port
# the remote port to connect to
parser.add_argument('-remote-browser-port', type=int, dest='remote_browser_port',
  help='the remote port to connect to for remote browser', default=4444)
##
# -remote-port
# the remote port to connect to
parser.add_argument('-remote-port', type=int, dest='remote_port',
  help='the remote port to connect to', default=22)
##
# -remote-username
# the remote username to use
parser.add_argument('-remote-username', type=str, dest='remote_username',
  help='the remote username to use', default=None)
##
# -remote-password
# the remote password to use
parser.add_argument('-remote-password', type=int, dest='remote_password',
  help='the remote password to use', default=None)
###
##
# -question
# poll questions
parser.add_argument('-question', dest='questions', action='append', default=[],
  help='the questions to ask')
###
# the maximum number of recent users
parser.add_argument('-recent-users-count', default=3, dest='recent_users_count',
  type=int, help='the number of users to consider recent')
##
# enables file reduction
parser.add_argument('-reduce', action='store_true', dest='reduce',
  help='enable reducing files under 50 MB')
##
# enables file repair (buggy)
parser.add_argument('-repair', action='store_true', dest='repair',
  help='enable repairing videos as appropriate')
##
# can be set in profile.conf
# root Google drive folder
parser.add_argument('-drive-root', type=str, default='OnlySnarf', dest='drive_root',
  help='the Google Drive root folder name')
##
# -save-users
# saves OnlyFans users upon exit
parser.add_argument('-save-users', action='store_true', dest='save_users',
  help='enable saving users locally on exit')
##
# -schedule
# 
parser.add_argument('-schedule', type=valid_schedule, default=None, dest='schedule',
  help='the schedule (MM-DD-YYYY:HH:MM)')
##
# -session-id
parser.add_argument('-session-id', default=None, dest='session_id',
  help='the session id to use')
# -session-url
parser.add_argument('-session-url', default=None, dest='session_url',
  help='the session url to use')
##
# -skip-download
parser.add_argument('-skip-download', action='store_true', dest='skip_download',
  help='skip file downloads')
##
# -skip-upload
# skips file upload
parser.add_argument('-skip-upload', action='store_true', dest='skip_upload',
  help='skip file uploads')
##
# list of users to skip
parser.add_argument('-skip-users', dest='skipped_users', 
  action='append', help='the users to skip or ignore ')
##
# -show
# shows window
parser.add_argument('-show','-show-window', dest='show', action='store_true', 
  help='enable displaying the browser window')
##
# -sort
# the sort method to use when selecting content unprompted
parser.add_argument('-sort', dest='sort', default="random", choices=["ordered","random"],
  help='the sort method to use when selecting content unprompted')
##
# -source
# the source to use when searching for content
parser.add_argument('-source', dest='source', default=None, choices=["google",
  # "dropbox",
  "remote","local"],
  help='file host location')
##
# -tags
# @[tag]
parser.add_argument('-tags', dest='tags', action='append', default=[],
  help='the tags (@[tag])')
##
# -text
# text for message or upload
parser.add_argument('-text', default=None, dest='text',
  help='the text to type')
##
# -time
# time in HH:MM
parser.add_argument('-time', type=valid_time, default=None, dest='time',
  help='the time (HH:MM)')
##
# -title
# the title of a file to search for
parser.add_argument('-title', default=None, dest='title',
  help='the title of the file to search for')
##
# -thumbnail
parser.add_argument('-thumbnail', action='store_true', dest='thumbnail',
  help='fix thumbnails when necessary')
##
# -tweet
# enabled tweeting
parser.add_argument('-tweeting', action='store_true', dest='tweeting',
  help='enable tweeting when posting')
##
# -upload-max
# the max number of 10 minute intervals to upload for
parser.add_argument('-upload-max-duration', dest='upload_max_duration', default=UPLOAD_MAX_DURATION,
  type=int, help='the number of 10 minute intervals to wait while uploading a file')
##
# -user
# the user to target
parser.add_argument('-user', type=str,  default=None, dest='user',
  help='the user to message')
##
# -users
# the users to target
parser.add_argument('-users', dest='users', action='append', default=[],
  help='the users to message')
##
# -users-favorite
# list of favorited users
parser.add_argument('-users-favorite', default=[],
  dest='users_favorite', action='append', help='supplied list of favorite users')
##
# -username
# the OnlyFans username to use
parser.add_argument('-username', type=str, default="", dest='username',
  help='the OnlyFans username')
##
# -username-google
# the Google username to use
parser.add_argument('-username-google', type=str, default="", dest='username_google',
  help='the Google username for login')
##
# -username-twitter
# the Twitter username to use
parser.add_argument('-username-twitter', type=str, default="", dest='username_twitter',
  help='the Twitter username for login')
##
# -users-read
# the number of users read when checking messages
parser.add_argument('-users-read', type=int, dest='users_read',
  help='the number of users to read when checking messages', default=10)
##
# -verbose
# v, vv, vvv
parser.add_argument('-v', '-verbose', dest="verbose", action='count', default=0, 
  help="verbosity level (max 3)")

## Promotion Methods
# -promotion-user
parser.add_argument('-promotion-user', dest="promotion_user", action='store_true', 
  help="uses user method when combined with action=promotion")



##
# Positional
##

##
# input
parser.add_argument('input', default=[], nargs=argparse.REMAINDER, 
  type=valid_path, help='file input to post or message')

##
import pkg_resources
parser.version = str(pkg_resources.get_distribution("onlysnarf").version)
parser.add_argument('-version', action='version')

############################################################################################

try:
  args = vars(parser.parse_args())
except Exception as e:
  print("Error: Incorrect arg format")
  import sys
  sys.exit(1)

if args["source"] and not args["destination"]:
  args["destination"] = args["source"]
if not args["source"]: args["source"] = "local"
if not args["destination"]: args["destination"] = "local"
# if args["debug"]: ACTIONS.append("promotion")
# if args["debug"]: ACTIONS.append("test")
if not args["category"]: args["source"] = None

############################################################################################

# print(args)
CONFIG = {}
for key in args:
  CONFIG[key.upper()] = args.get(key)
CONFIG = read_config(CONFIG)

#############
# Debugging #
# import sys
# print(CONFIG)
# sys.exit(0)