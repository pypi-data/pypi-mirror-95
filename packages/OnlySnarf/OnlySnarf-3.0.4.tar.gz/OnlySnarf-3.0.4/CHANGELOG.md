# OnlySnarf  

## Changelog  
**0.0.1 : 9/25/2018**
  - code organized
  **0.0.2 : 10/20/2018**
  - python package organized
  **0.0.3 : 1/14/2019**
  - sync with DBot updates; while loop upload
  **0.0.4 : 1/21/2019**
  - upload fix & hashtagging
  **0.0.5 : 1/29/2019**
  - demo
  **0.1.0 : 2/3/2019**
  - menu
  - package & setup.py
  **0.1.1 : 2/4/2019**
  - menu fixes
  **0.1.2 : 2/7/2019**
  - config.py
  - script names updated
  - readme updated
  **2/9/2019**
  - fuck you PyDrive
  **0.1.3 : 2/24/2019**
  - jpeg
  **0.1.4 : 3/4/2019**
  - mount path
  **0.1.5 : 3/7/2019**
  - updated send_post_button refs
  **0.1.6 : 3/19/2019**
  - module separation
  **0.1.7 : 3/28/2019**
  - settings.py
  - user.py
  **0.1.8 : 3/31/2019**
  - debugging
  - Drive API for mp4 downloads
  **0.2.0 : 4/10/2019**
  - User: read_chat
  **0.2.1 : 4/12/2019**
  - upload performer
  - upload scene
  **0.2.2 : 4/15/2019**
  - settings now actually updates
  - settings globals -> class
  **4/16/2019**
  - fucking default variables
**1.0.0 : 4/22/2019**
  - save image_name instead of path
  - uploaded to pip
  **1.0.1**
  - removed video.mp4
  **1.0.2**
  - minor adjustments
  **1.0.3 : 5/3/2019**
  - minor bug fixes
  **1.0.4 : 5/8/2019**
  - more minor bug fixes
  **1.1.0 : 5/12/2019**
  - added: (settings).MOUNT_DRIVE, ROOT_FOLDER, DRIVE_FOLDERS, CREATE_MISSING_FOLDERS
  - create Google folder structure programmatically
  - predefine Google root
  **5/14/2019**
  - replaced: settings.TYPE - settings.ACTION
  - added: settings profile -> skeetzo
  - updated: scenes to include trailer addition
  **1.1.1 : 5/23/2019**
  - fixed tweeting bug
  - todo priority queue
  **1.1.2 : 5/25/2019**
  - added: cron.py
  - |_ needs a menu system to be added
  **1.1.3 : 6/26/2019**
  - fixed file & directory uploads
  - removed config initialization from google.py
  - updated ReadMe
  **1.1.4**
  - fixed MANIFEST and credentials
  **1.1.5**
  - removed credentials
  **1.1.6**
  - relative imports -> absolute
  - fixed messaging: input price
  **1.1.7 : 7/3/2019**
  - collapsed upload_file & upload_directory into upload_to
  **1.1.8 : 7/19/2019**
  - fixed user scrape css
  **1.1.9 : 8/14/2019**
  - fixed user scrape css again
  **1.1.10 : 8/21/2019**
  - really really fixed user scrape css
  - removed apiclient from setup.py
  **1.2.0 : 9/2/2019**
  - fixed user scrape & cache
  - added promotions (unfinished)
  **1.2.1 : 9/4/2019**
  - removed innate debug profiles and added profile.conf
  - added google creds to onlysnarf-config
  - updated readme to reflect creds process
  **1.2.2 : 9/5/2019**
  - fixed user scrape & messaging
  - fixed messaging by username
  **1.3.0 : 9/8/2019**
  - finished testing promotions- unworkable w/o email or clipboard utility
  - finished testing messages & user selection
  - hidden unworking functions in menu w/o debug
  **1.3.1 : 9/9/2019**
  - error messages cleanup in user messaging
  **1.3.2 : 9/10/2019**
  - submit button works again
  - added: way to select google drive file to message
  **1.3.3 : 9/15/2019**
  - package install fix & dynamic version in menu
  **1.3.4 : 9/15/2019**
  - menu cleanup
  **1.4.0 : 9/15/2019**
  - chromedriver binary version set = 77.0.3865.40
  - added catch for image upload error
  **1.4.1 : 9/16/2019**
  - cleaned print & maybePrint outputs
  - cleaned up settings.py
  - cron cleanup
  **1.4.2 : 9/17/2019**
  - text fix
  - fixed verbose output
  **1.4.3 : 9/21/2019**
  - dbot issue
**2.0.0 : 9/25/2019**
  - added functionality to choose instead of random
  **2.0.1**
  - oops
  **2.1.0 9/29/2019**
  - discount: all or select users x% for n months
  - fixed local user load
  - updated User(mess=mess) -> User(data)
  **2.1.1**
  - shameless 2.1.0 fix
  **2.2.0**
  - cleaned up & mostly fixed release via selection
  - cleaned up release via random
  - nonrandom uploads now confirm entered information
  - cleaned out user methods from driver -> static
  - updated download_performers and seperated randomizing selection
  **2.2.1**
  - release: keywords and performers can be deleted
  **2.2.2**
  - standalone script bug
  **2.2.3**
  - removed pointless User cache -> fixed User count bug
  - removed overwrite-local
  - added BROWSER.url checks
  **2.2.4**
  - user selections -> debug
  **2.3.0**
  - added: post
  **2.4.0**
  - settings cleanup
  - release -> upload
  - onlyfans var cleanup
  - added local input
  - added posts beginning -> needs configparser
  **2.5.0 : 10/5/2019**
  - configparser -> profile.conf updated
  - posts & text prompt
  - functionality to create a post w/ text
  |_ create multiple basic posts such as "greetings" or "going on holiday" or a trip, or question of what to post more of?
  |_ a menu of standardized posts like above
  |_ a menu of questions|greetings to message to users
  - added: easier way to select local file to upload
  **2.5.1**
  - more verbose cleanup
  **2.6.0**
  - config cleanup
  |_ profile.conf & posts.conf & config.json -> config.conf
  - added: cron feature for adding, deleting, listing crons
  - added: Twitter login prompt
  - added: `local` setting
  - added check for failed login
  - added post: "OnlySnarf Bot commands: !pic | !pic dick | !pic ass"
  **2.6.1**
  - creds cleanup
  **2.7.0**
  - menu sort
  - onlysnarfpy
  **2.7.1**
  - driver auth fix
  - cron fix
  **2.8.0 : 10/8/2019**
  - added Expiration
  - added Schedule
  - added: Poll
  - upload a gallery to a message
  **2.9.0**
  - a post that advertises custom requests
  - a post that advertises tipping price for messaging
  - a post that advertises prices for paid messages for individual photo requests
  - a post for requesting people to comment or dm me individuals they'd like to see me with
  - a post thanking followers for being followers
  **2.9.1**
  - args fix: keywords, performers, input
  **2.9.2**
  - text fix
  **2.9.3**
  - add video reduce to somewhere it can impact INPUT files
  **2.9.4**
  - input bug?
  **2.10.0**
  - discount css update
  - message image upload fix
  - added gifs
  **2.11.0**
  - OFKEYWORD - specifies random folder
  **2.11.1**
  - oops
  **2.11.2**
  - oops
  **2.11.3**
  - oopsies
  **2.11.4**
  - more oopsies
  **2.12.0**
  - added setting: skip-backup
  **2.12.1**
  - fixed BYKEYWORD bug preventing random upload
  - fixed messaging folder of images
  **2.13.0**
  - fixed: skip-backup
  - added: skip-delete-google
  **2.13.1**
  - fixed fixed: skip-backup
  - fixed: enter upload
  **2.13.2**
  - updated: google mimetypes
  **2.14.0**
  - added: NOTKEYWORD for excluding folders by keyword
  **2.14.1**
  - updated: upload_to_OnlyFans w/ more error checks in attempt to fix below bug
  - BUG: does not find "send_post_button" from chromebook ubuntu laptop using ChromeDriver 74.0.3729.6 | Google Chrome 74.0.3729.131
  - cleaned up settings.py comments
  - added: remember me upon login is checked, does nothing
  **2.14.2**
  - added: error_checker for not found elements
  **2.14.3**
  - fixed: user scrapes
  - updated: config.py, unable to test
  **2.14.4**
  - class reorg
  - added 'dynamic' element searching
  - fixed css elements for major functions
  - added element.py
  **2.15.0**
  - major functionality restored
  **2.15.1**
  - fixed menu
  - added -version flag
  **2.15.2**
  - settings options debugging
  - added: tabbing to inputs
  - undid tabbing to inputs -> unpredictable odd behavior
  - minor random debugging (??wtf?)
  - xmas scripts
  **2.15.3**
  - better sorted test scripts
  - changed error_window:filename fix to just closing window
  - fixed mimetype upload (sorta)
  **2.15.4**
  - updated test scripts output
  - added setting: verbosest
  - cleaned up driver&profile elements
  **2.15.5**
  - more settings prep
  - minor fixes to login
  **2.16.0**
  - fixed: post
  - updated menu.md
  **2.16.1**
  - fixed: browser closes now
  **2.16.2**
  - more Settings integration
  - updated method of messaging all, recent, favorite
  **2.16.3**
  - OnlySnarf classname -> Snarf
  - updated profile init
  **2.16.4**
  - minor bugs
  **2.16.5**
  - updated BYKEYWORD and NOTKEYWORD -> str != str
  **2.16.6**
  - fixed: message all price submit
  - fixed: random files now properly downloaded, again
  **2.16.7**
  - fixed: messageAll
  - fixed: go_to_page
  **2.16.8**
  - update: go_to_* auths first
  - added: following_get
  **2.16.9**
  - update: users_get, following_get -> speed +, reliability +
  - mostly functional
  **2.16.10** debugging pre 2.17.0
  - upload -> post
  - Message, File, Google_File, Google_Folder, Video, Image classes
  - ffmpeg.py
  - login function cleaned up / spawn_browser
  - settings -> argsparse
  - menu cleaned up
  - file system selection cleaned up
  - category
  **2.17.0**
  - massive spaghetti -> api overhaul
  - new menu
  **2.17.1**
  - fixed packaging
  **2.17.2**
  - fixed post/message w/o prompt
  **2.17.3**
  - fucking a
  **2.17.4**
  - fixed google uploads w/o prompt
  **2.17.5**
  - fixed video extensions
  **2.17.6**
  - increased UPLOAD_MAX_DURATION to 6 hrs
  - minor fixes to menu input
  **2.17.7**
  - fixed backup pathing
  - fixed file upload max
  **2.17.8**
  - added remote webdriver operations
  - added firefox
  - add performers; debugging
  **2.17.9**
  - debugged 2.17.8
  **2.17.10**
  - removed moviepy
  - exit(1) when missing driver
  **2.17.11**
  - fixed messaging a user
  - fixed performer operations
  **2.17.12**
  - minor fixes to launching firefox
  **2.17.13**
  - fixed post uploads with random content
  - updated onlysnarf-config
  **2.17.14**
  - herpderp
  **2.17.15**
  - herpaderpaderp
  - fixedfixed uploading
  **2.17.16**
  - herpaderpaderpa
  - fixed more uploading prompts
  **2.17.17**
  - debugged firefox
  - debugged Profile (a bit)
  - debugged backup content
  - args: added username_account to differentiate from twitter username for login
  - args: added source & destination
  - added remote ssh dir
  - added: login source [onlyfans|twitter]
  **2.17.18**
  - oops; fixed firefox "binary"
  **2.17.19**
  - User: following_get, following_write (still needs debugging)
  - remote: updated connection priorities; auto -> form -> twitter -> google
  - login: google; needs debugging
  **2.17.20**
  - oops, disabled auto_reconnect until debugging
  **2.17.21**
  - minor fixes to menu
  **2.18.0**
  - menu updates
  - profile / settings updates
  - cleaned up menu.md
  - updated profile: sync from, sync to, backup
  - updated login methods
  - added: delete-empty folders; properly remove empty folders that all images have been removed from when backing up / moving files
  - debugged: google login
  - debugged: following_write
  -> remote webserver behavior
  - added: session_id, session_url
  - added: remote-chrome, remote-firefox, auto-remote
  - added: reconnect
  - added: session_id & session_url -> session.json for reconnecting to existing browser sessions
  **2.18.1**
  - debugged: redundant category asking
  - debugging: local
  - updated: tests
  **2.18.2**
  - debugged: local
  - create-drive -> create-missing
  - debugging: remote
  **2.18.3**
  - failed expires/poll/schedule ends post
  - fixed date validator
  - debugged: schedule, date, time
  - debugged: post schedule
  - debugging promotion: updated promotion args
  - debugged: discount
  - debugging: promotion (mostly)
  **2.18.4**
  - debugged: promotion- free trial (ish)
  - debugging: promotion- campaign
  **2.18.5**
  - debugged: promotion- campaign
  - debugging: settings
  **2.19.0**
  - added: tabs behavior
  - added: cookies - wow i'm a fucking idiot for not adding this sooner
  - debugging: bot
  - properly tested: settings get
  - properly testedish: settings set
  **2.20.0**
  - added: bot functionality - menu prompt, tip parsing
  **2.20.1**
  - updated: saving session_id and session_url
  - more bot debugging
  - fixed bin/install-firefox.sh: update for processor
  **2.20.2**
  - more debugging
  - fixed: file input
  - debugging: grandfathered
**3.0.0 : 9/21/2020**
  - major updates to browsers debugged
  - added: grandfather promotion
  - added: user lists (finally) - favorites, bookmarks, friends, etc
  - fixed: performer uploads
  - added: specify inner category for performers via 'category-performer'
  - added: fetch file by 'sort' - random|ordered
  -> Bot
  - bot functionality to check posts for tips
  - automatically heart / send dick pics to tips in messages
  **3.0.1**
  - added argument error catch
  **3.0.2**
  - documentation started
  **3.0.3**
  - selenium version 3.141.1 -> 3.141.59
  - bin/install-firefox version 26 -> 29
  **3.0.4**
  - jk no selenium bump...

----------------------------------------  

  - empty messages bug: Type a message below to start a conversation with 

  **x.x.x**
  - test Profile: check
  - test Profile: posts
  |- advertise - tweet to advertise new account, tweet to ask about what you should post
  - test Profile: setup
  
  - finish debugging `onlysnarf-config`
  - updated: images & demo gifs

  **x.x.x**
  - Profile options completely "functional" / debugged

----------------------------------------

## ToDo
  - add to upload: greatest & least (folder sizes)

### Low Priority
  - add: read messages html for emojis
  - update: backup function to include original folder name -> posted/galleries/$file
  - [MESSAGES] layout in config for preset message formats

  -> Cron
  - completely remove cron features

  -> Promotion
  - add email|Twitter functionality for sending trial link; add clipboard function to copy link
  - functionality to scan profiles to estimate their posts-to-fan income ratios

  -> Profile
  - new - setup - Twitter -> profile, banner; Price and Settings
  - new - advertise
  - new - posts - tweet to advertise new account, tweet to ask about what you should post, etc; recommend what to post
  - need to add 'create' to Profile for asking for profile settings when syncing to

  -> Twitter
  - tweet reminders
  - can enter text that is tweeted
  - include media attachments
  -- check for previously existing tweet

  -> Remote
  -- need to reproduce --
  - debug / add error catch for uploads: ('Connection aborted.', BrokenPipeError(32, 'Broken pipe'))

### Medium Priority

### High Priority


Referral Code
https://onlyfans.com/?ref=409408