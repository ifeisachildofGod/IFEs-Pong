import pygame
import os
from typing import Final, Sequence, Tuple, Union

# Player constants
CONTROL_OPTIONS: Final = ['Mouse', 'AI', 'Keyboard']
AI_DIFFICULTY_OPTIONS: Final = ['Easy', 'Medium', 'Normal', 'Hard', 'Very Hard', "Impossible"]

# Important directory paths
DATA_PATH: Final = os.path.join(os.getcwd(), 'src/json/data.json')
ONWIDGETCLICKED_MP3_PATH: Final = os.path.join(os.getcwd(), 'src/audio/on_widget_clicked.mp3')
ONWIDGETFOCUS_WAV_PATH: Final = os.path.join(os.getcwd(), 'src/audio/on_widget_focus.wav')
LOGO_PNG_PATH: Final = os.path.join(os.getcwd(), 'src/images/logos/logo.png')
ONHOVER_PNG_PATH: Final = os.path.join(os.getcwd(), 'src/images/onhover.png')

# Help screen constants and variables
LINKS: Final = {
    'IFEs Itch page': 'https://ifeisachildofgod.itch.io/',
    'IFEs Github': 'https://github.com/ifeisachildofGod/IFEs-Pong'
}
LINK_KEYS: Final = list(LINKS.keys())
_space = 100 * ' '
_settings = f'Settings:{_space}'
_statistics = f'Statistics:{_space}'
_HelloWorld = 'HELLO WORLD'
_Updates = 'UPDATES'
_GameFeaturesAndMenus = 'GAME FEATURES AND MENUS'
_WhatsNext = 'WHATS NEXT'
_Also = 'ALSO'
_Links = 'Links you should definitly check out'
HELP_SCR_HEADERS = [_settings, _statistics, _HelloWorld, _Updates, _GameFeaturesAndMenus, _WhatsNext, _Also, _Links]
HELP_INFO: Final = f"""
{_HelloWorld}
    Version 5 is here and from making this I've found out that this game is almost done, I've
    looked for what to improve and I couldn't find much, (apart from the features I put coming
    soon on). But a very big update has been added (MORE INFO AT THE UPDATE SECTION), I
    have fixed every single bug not relating to the multiplayer, and have added a permission
    screen as you might have already seen. The permission screen has given me the power to
    make an msi version of this game, bcos during testing, I found out that I get errors
    from my system involving permissions. So now you don't have to install a sketchy zipfile
    on your system.
    
{_Updates}
    1) Permission checking has been added
    
    2) The code has vastly been improved
    
    3) We finally have a github page so that you can check out all of the code, from version one
       to version 5 but you are not allowed to use it to make money, that's my job, link at the
       end of the page
    
    4) Most, if not all bugs in the bluetooth multiplayer have been fixed
    
    5) The ball physics have been improved
    
    6) Tiny optimizations, fixes and adjustments have been made
        
{_GameFeaturesAndMenus}
    I forgot to mention that main menu had been added in the main update but am sure that you
    might have figured it out. I don't plan on adding any more menus, so I may remove this
    section in the next update

{_settings}
    1) Background Color: This is used to change the color of the background of all the menus
    
    2) Foreground Color: This is used to change the color of the foreground of the screen like text,
        buttons and the scroll wheel
    
    3) AI Difficulty: This is to change the difficulty of the opposing AI.
        Their values::[Easy, Medium, Normal, Hard, Very Hard]
    
    4) Player one(two) Binding: This is used to change the keyboard binding that controls each
        player, when focused on the up or down option click enter and then
        press any key you want to you want to bind to up in the mini
        window that appears and the same for down.

    5) Player one(two) Control: This is to change the control method the player selected
        Their values::[KEYS, AI, MOUSE]
    
    Note You have to know this about the options:
        - The color text fields accepts string inputs like "blue", "green" and "black", It also
          accepts RGBA inputs but if you have checked it out you will find out that you can't
          input brackets or braces so if you want to input yellow in RGBA instead of inputing
          "(255, 255, 0, 255)" you instead input "255, 255, 0, 255", Same with hex values instead
          of "#123abc" you replace the '#' for a '.' as in ".123123" and the game will add the
          values that ought to be there it.
        
        - Those things beside the AI DIfficulty and Player Control options are like cursors you
          can click to toggle the options just like you use in your keyboard

{_statistics}
    I got my prioties straight and had a reality check, and I realised that the game does not need
    another menu, so this feature will not be coming out in this update, and probably not in any
    update from now on. This is the last version that will have this section in the info screen.

{_WhatsNext}
   1) I am currently experimenting and working on server multiplayer, but it proves to be quite
      difficult, so I can't make any promises that this will be added in the next update.
    
    2) A better system for adding custom skins may be added, if I can figure it out
    
{_Also}
    If any error was made in this menu or the game in general, I am sorry. I'm currently returning
    back to school, and somewhat had to rush certain fixes and optimizations so as to make it
    release ready, due to our school's resumption I be focusing more on my studies, that's why
    updates might not come out for a while. Bye for now thanks and see you soon :-)

{_Links}
{''.join([f'`{link_name}|' for link_name in LINK_KEYS])}
"""


P1_Y_POS_SAVE_KEY: Final = 'P1_Y_POS_SAVE_KEY'
P2_Y_POS_SAVE_KEY: Final = 'P2_Y_POS_SAVE_KEY'
BALL_DIR_SAVE_KEY: Final = 'BALL_DIR_SAVE_KEY'
BALL_POS_SAVE_KEY: Final = 'BALL_POS_SAVE_KEY'
SCORE_SAVE_KEY: Final = 'SCORE_SAVE_KEY'

MPO_BG_COLOR_KEY: Final = "MPO_BG_COLOR_KEY"
MPO_FG_COLOR_KEY: Final = "MPO_FG_COLOR_KEY"
MPO_DATA_KEY: Final = "MPO_DATA_KEY"
MPO_PC_KEY: Final = "MPO_PC_KEY"
MPO_PB_KEY: Final = "MPO_PB_KEY"

MPO_CONTROL_OPTIONS = ["Mouse", "Keyboard"]
MPO_OPTIONS = ["Bluetooth", "Multiplayer"]

# Settings UI constants
SETTINGS_DICT_BG_KEY: Final = 'Background Color'
SETTINGS_DICT_FG_KEY: Final = 'Foreground Color'
SETTINGS_DICT_AI_KEY: Final = 'AI Difficulty'
SETTINGS_DICT_P1C_KEY: Final = 'Player one Control'
SETTINGS_DICT_P2C_KEY: Final = 'Player two Control'
SETTINGS_DICT_POB_KEY: Final = 'Player one Binding'
SETTINGS_DICT_PTB_KEY: Final = 'Player two Binding'

# Constants
SPECIAL_KEYS: Final = {
    'SPACE': pygame.K_SPACE,
    'TAB': pygame.K_TAB,
    'LEFT': pygame.K_LEFT,
    'SHIFTL': pygame.K_LSHIFT,
    'SHIFTR': pygame.K_RSHIFT,
    'SPACE': pygame.K_SPACE,
    'RIGHT': pygame.K_RIGHT,
    'UP': pygame.K_UP,
    'DOWN': pygame.K_DOWN,
    'PAGEDOWN': pygame.K_PAGEDOWN,
    'PAGEUP': pygame.K_PAGEUP,
    'HOME': pygame.K_HOME,
    'END': pygame.K_END,
    'F1': pygame.K_F1,
    'F2': pygame.K_F2,
    'F3': pygame.K_F3,
    'F4': pygame.K_F4,
    'F5': pygame.K_F5,
    'F6': pygame.K_F6,
    'F7': pygame.K_F7,
    'F8': pygame.K_F8,
    'F9': pygame.K_F9,
    'F10': pygame.K_F10,
    'F11': pygame.K_F11,
    'F12': pygame.K_F12,
}

SCORE_FONTS: Final = [
'''
######
#    #
#    #
#    #
#    #
#    #
######
''',
'''
   #
   #
   #
   #
   #
   #
   #
''',
'''
#####
    #
    #
#####
#
#
#####
''',
'''
#####
    #
    #
#####
    #
    #
#####
''',
'''
#
#  #
#  #
#####
   #
   #
   #
''',
'''
#####
#
#
#####
    #
    #
#####
''',
'''
#####
#
#
#####
#   #
#   #
#####
''',
'''
#####
    #
    #
    #
    #
    #
    #
''',
'''
#####
#   #
#   #
#####
#   #
#   #
#####
''',
'''
#####
#   #
#   #
#####
    #
    #
    #
'''
]

CURSOR_ADJUST: dict[str, float] = {
    "a": 1.999,
    "b": 2.999,
    "c": 0,
    "d": 3,
    "e": 2,
    "f": -3.3,
    "g": 2,
    "h": 3,
    "i": -6,
    "j": -6,
    "k": 1.1,
    "l": -6,
    "m": 11,
    "n": 3,
    "o": 3,
    "p": 3.11,
    "q": 3.11,
    "r": -2,
    "s": 0,
    "t": -3,
    "u": 3,
    "v": 1,
    "w": 7,
    "x": 1,
    "y": 1,
    "z": 0,
    "A": 3.999,
    "B": 3.999,
    "C": 4,
    "D": 6,
    "E": 2,
    "F": 1,
    "G": 6,
    "H": 5.98,
    "I": -4.95,
    "J": -5,
    "K": 3,
    "L": 1,
    "M": 11,
    "N": 7.1,
    "O": 7,
    "P": 3,
    "Q": 7,
    "R": 3,
    "S": 2,
    "T": 2,
    "U": 6,
    "V": 3,
    "W": 11,
    "X": 2,
    "Y": 2,
    "Z": 2,
    
    "1": 2,
    "2": 2,
    "3": 2,
    "4": 2,
    "5": 2,
    "6": 2,
    "7": 2,
    "8": 2,
    "9": 2,
    "0": 2,
    ",": -6,
    ".": -6,
    "`": 1.9,
    ";": -5,
    "#": 4,
    ")": -5,
    "(": -5,
    "'": -6,
    "\\": -3,
    "/": -3,
    "]": -4,
    "[": -4,
    " ": -5,
    "-": -4,
 }

ColorType = Union[int, str, Tuple[int, int, int], Tuple[int, int, int, int], Sequence[int], str, pygame.color.Color]
