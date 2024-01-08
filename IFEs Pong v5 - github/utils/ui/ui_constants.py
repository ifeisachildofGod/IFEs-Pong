
from typing import Final
import pygame

pygame.init()

# Common UI constants
BORDER_RAD: Final = 7
BG_OFFSET: Final = 2
SCROLL_SPEED: Final = .15
PTR_Y_POS: Final = 5
ICON_POS: Final = 10
ICON_SIZE: Final = 2

# New UI constants
TV_INPUT_DELAY_TIMER: Final = 3
TV_INPUT_MAX_WAIT_DELAY_TIMER: Final = 50
BORDER_RAD_BUTTON: Final = 4

# Text view constants
MAX_TV_LEN: Final = 20
BLINK_TIMER: Final = 1
ON_HOVER_OPAC: Final = 200
ON_CLICK_OPAC: Final = 100

# Pause UI constants
PAUSE_TEXT_START_POS: Final = 120
PAUSE_TEXT_SPACING: Final = 70
X_PAUSE_WIDG_POS_OFFSET: Final = 200
X_WIDG_SPACE_OFFSET: Final = 50
EXTRA_HELP_Y_OFFSET: Final = 100
PAUSE_DICT_RESUME: Final = 'Resume'
PAUSE_DICT_SETTINGS: Final = 'Settings'
PAUSE_DICT_INFORMATION: Final = 'Information'
PAUSE_DICT_MAIN_MENU: Final = 'Main menu'
PAUSE_DICT_RESTART: Final = 'Restart'
PAUSE_DICT_EXIT: Final = 'Exit'

# Main menu UI constants
MAIN_MENU_TEXT_START_POS: Final = 250
MAIN_MENU_TEXT_SPACING: Final = 80
MAIN_MENU_TEXT_Y_SPACE_OFFSET: Final = 50
MAIN_MENU_X_SPACING_OFFSET: Final = 50
MAIN_MENU_DICT_CONTINUE: Final = 'Continue'
MAIN_MENU_DICT_NEW_GAME: Final = 'New Game'
MAIN_MENU_DICT_MULTIPLAYER: Final = 'Multiplayer'
MAIN_MENU_DICT_EXIT: Final = 'Exit'

# Settings UI constants
SETTINGS_TEXT_START_POS: Final = 70
SETTINGS_TEXT_SPACING: Final = 70
X_SETTINGS_TEXT_OFFSET: Final = 200
X_SETTINGS_SPACE_OFFSET: Final = 100
Y_SETTINGS_SPACE_OFFSET: Final = 20
SETTINGS_DICT_BG_KEY: Final = 'Background Color'
SETTINGS_DICT_BG_OPT_KEY: Final = f'{SETTINGS_DICT_BG_KEY} opt'
SETTINGS_DICT_FG_KEY: Final = 'Foreground Color'
SETTINGS_DICT_FG_OPT_KEY: Final = f'{SETTINGS_DICT_FG_KEY} opt'
SETTINGS_DICT_AI_KEY: Final = 'AI Difficulty'
SETTINGS_DICT_AI_OPT_KEY: Final = f'{SETTINGS_DICT_AI_KEY} opt'
SETTINGS_DICT_P1C_KEY: Final = 'Player one Control'
SETTINGS_DICT_P1C_OPT_KEY: Final = f'{SETTINGS_DICT_P1C_KEY} opt'
SETTINGS_DICT_P2C_KEY: Final = 'Player two Control'
SETTINGS_DICT_P2C_OPT_KEY: Final = f'{SETTINGS_DICT_P2C_KEY} opt'
SETTINGS_DICT_MPO_KEY: Final = 'Multiplayer type'
SETTINGS_DICT_MPO_OPT_KEY: Final = f'{SETTINGS_DICT_MPO_KEY} opt'
SETTINGS_DICT_POB_KEY: Final = 'Player one Binding'
SETTINGS_DICT_POB_UP_OPT_KEY: Final = f'{SETTINGS_DICT_POB_KEY} opt up'
SETTINGS_DICT_POB_DOWN_OPT_KEY: Final = f'{SETTINGS_DICT_POB_KEY} opt down'
SETTINGS_DICT_PTB_KEY: Final = 'Player two Binding'
SETTINGS_DICT_PTB_UP_OPT_KEY: Final = f'{SETTINGS_DICT_PTB_KEY} opt up'
SETTINGS_DICT_PTB_DOWN_OPT_KEY: Final = f'{SETTINGS_DICT_PTB_KEY} opt down'

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

CURSOR_ADJUST: Final = {
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

# Font Constants
FONT1: Final = pygame.font.Font('utils/fonts/font(1).ttf', 35)
FONT2: Final = pygame.font.Font('utils/fonts/font(2).ttf', 17)
FONT3: Final = pygame.font.Font('utils/fonts/font(2).ttf', 25)
FONT4: Final = pygame.font.Font(None, 50)
FN1_SIZE: Final = 20
FN2_SIZE: Final = 9.5
FN3_SIZE: Final = 12
FONT_CELL_SIZE: Final = 15
FOCUS_RECT_WIDTH: Final = 2
TXT_PAD: Final = 20






















# NOT THE USER OR THE DEV IS TO CHANGE THiS VARIABLE
SCROLL_WEIGHT: Final = 2.320800000000473

