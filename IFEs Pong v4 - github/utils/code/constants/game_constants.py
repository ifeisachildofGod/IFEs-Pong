
import pygame
from typing import Final
import os

pygame.init()

# RES constants
SCR_WIDTH: Final = pygame.display.get_desktop_sizes()[0][0] - 166
SCR_HEIGHT: Final = pygame.display.get_desktop_sizes()[0][1] - 166
FPS: Final = 70

# Characters contants
CONTROL_OPTIONS: Final = ['MOUSE', 'AI', 'KEYS']
AI_DIFFICULTY_OPTIONS: Final = ['Very Hard', 'Hard', 'Normal', 'Medium', 'Easy']
HIT_OFFSET: Final = 30
EDGE_SPACE: Final = 40
PLAYER_SPEED = BALL_SPEED = .4

PLAYER_SIZE: Final = [20, 70]
P1_START_POS: Final = EDGE_SPACE
P2_START_POS: Final = SCR_WIDTH - EDGE_SPACE - PLAYER_SIZE[0]

BALL_SIZE: Final = 10

# Mid-line constants
LINE_SPACE: Final = 5
LINE_LEN: Final = 20
LINE_WIDTH: Final = 3

# Important directory paths
CWD: Final = os.getcwd()
CONTINUE_VARIABLE_DIR: Final = rf'{CWD}\utils\json\continue.json'
SETTINGS_DIR: Final = rf'{CWD}\utils\json\settings.json'
STATS_DIR: Final = rf'{CWD}\utils\json\stats.json'
BUTTON_CLICKED_SOUND_PATH: Final = rf'{CWD}\utils\sounds\on_widget_clicked.mp3'
BUTTON_HOVERED_SOUND_PATH: Final = rf'{CWD}\utils\sounds\on_widget_focus.wav'
PONG_LOGO_PNG = rf'{CWD}\utils\logos\logo.png'

def all_stats(hpos='p', hpts='p', hpoatsaea='p',
              hpoatsama='p', hpoatsana='p', hpoatsaha='p',
              hpoatsaia='p', heasapoat='p', hmasapoat='p',
              hnasapoat='p', hhasapoat='p', hiasapoat='p',
              dgwpl='p', muao='p', muco='p',
              mup='p', ltsp='p'):
    
    info =  f"""

            1)    Highest Player one score:                                                                  {hpos}
                
            2)    Highest Player two score:                                                                  {hpts}
                
            3)    Highest Player one and two score against Easy AI:                                          {hpoatsaea}
                
            4)    Highest Player one and two score against Medium AI:                                        {hpoatsama}
                
            5)    Highest Player one and two score against Normal AI:                                        {hpoatsana}
                
            6)    Highest Player one and two score against Hard AI:                                          {hpoatsaha}
                
            7)    Highest Player one and two score against Impossible AI:                                    {hpoatsaia}
                
            8)    Highest Easy AI score against Player one and two:                                          {heasapoat}
                
            9)    Highest Medium AI score against Player one and two:                                        {hmasapoat}
                
            10)    Highest Normal AI score against Player one and two:                                       {hnasapoat}
                
            11)    Highest Hard AI score against Player one and two:                                         {hhasapoat}
                
            12)    Highest Impossible AI score against Player one and two:                                   {hiasapoat}
                
            13)    Longest time spent playing:                                               {ltsp}
                
            14)    Most used player:                                                                         {mup}
                
            15)    Most used control option:                                                                 {muco}

            16)    Most used AI option:                                                                      {muao}

            17)    Day game was used longest:                                                                {dgwpl}



            """
    
    return info

# Player constants
AI_RESPONSE_OFFSET: Final = 100
MAX_TIMER: Final = 100

# Anything involving text constants
FN1_SIZE: Final = 20
FN2_SIZE: Final = 9.5
FN3_SIZE: Final = 12
FONT_CELL_SIZE: Final = 15

FONT1: Final = pygame.font.Font(rf'{CWD}\utils\fonts\font(1).ttf',35)
FONT2: Final = pygame.font.Font(rf'{CWD}\utils\fonts\font(2).ttf',35//2)
FONT3: Final = pygame.font.Font(rf'{CWD}\utils\fonts\font(2).ttf',50//2)
FONT4: Final = pygame.font.Font(size=50)

# Constants involving text
FOCUS_RECT_WIDTH: Final = 2
TXT_PAD: Final = 20
MAX_TV_LEN: Final = 20

# ETC
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
LINKS: Final = {
    'IFEs Itch page': 'https://ifeisachildofgod.itch.io/',
    'IFEs Pixel Runner': 'https://ifeisachildofgod.itch.io/ifes-pixel-runner',
    'IFEs YTVDownloader': 'https://ifeisachildofgod.itch.io/ifes-ytvideo-downloader',
    'IFEs Freelance':'https://www.upwork.com/freelancers/~0113b8c14366fba047?referrer_url_path=%2Fab%2Fprofiles%2Fsearch%2Fdetails%2F~0113b8c14366fba047%2Fprofile'
}

LINK_KEY: Final = [k for k, _ in LINKS.items()]

_pause = 'Pause:                                                                                       '
_settings = 'Settings:                                                                                   '
_information = 'Information:                                                                                '
_statistics = 'Statistics:                                                                                 '
_HelloWorld = 'HELLO WORLD'
_Updates = 'UPDATES'
_GameFeatursAndMenus = 'GAME FEATURES AND MENUS'
_WhatsNext = 'WHATS NEXT'
_Also = 'ALSO'
_Links = 'Links that I think you should check out'

HEADERS = [_pause, _settings, _information, _statistics, _HelloWorld, _Updates, _GameFeatursAndMenus, _WhatsNext, _Also, _Links]

HELP_INFO: Final = f"""
{_HelloWorld}
    Hi, I didn't think version 4 would be out so soon, in the last update, I insinuated that I might
    not make or release the game so soon, but the fact is that I love to code, and I couldn't stay
    away from my laptop the entire time I was in school. So this is version 4, as with every update
    there are some nice links at the bottom of the screen, that you should check out, soo see ya ;) .
    Oh and this is some sort of a prototype (for testing purposes), and might have some bugs and
    errors, especially in the multiplayer part (Bluetooth).
    
{_Updates}
    Fixed all of the widgets and improved them so very much, you might not really see it, but it is
    much better.
    
    Some certain sound effects have been added, they have not been added everywhere bcos as I
    said this is a prototype and for testing purposes.
    
    Multiplayer has finally been added, but it is only bluetooth for now, and that mainly why I am 
    posting the game, to test some aspects with other computers
    
    Other aspects of the game, apart from some of the visuals have largely remained unchanged, but
    some of the parts of it might be a little buggy, but a new version will come out soon...enough
    
{_GameFeatursAndMenus}
Basically everything is the same from the last update

{_pause}
    Resume: As it says resumes the game, or you can use the button at the top left of the screen 
            to resume                                                                            
    
   Settings: Provides options that change the outlook and performance of the game. Better definition
              below                                                                                 
    
    Restart: Resets the game                                                                     
    
    Exit: Helps you to leave the game, which I don't think you should do                         

{_settings}
    Background Color: This is used to change the color of the background of all the menus        
    
    Foreground Color: This is used to change the color of the foreground of the screen like text,
                    buttons and the scroll wheel                                
    
    AI Difficulty: This is to change the difficulty of the opposing AI. Their values::[Easy,     
                Medium, Normal, Hard, Impossible]                                      
    
    Player one Binding: This is used to change the keyboard binding that controls player one, when
                                    focused on the up or down option click enter and then press any
                                    key you want to you want to bind to up in the mini window that 
                                    appears and vice versa for down.                               
    
    Player two Binding: Same as Player one Binding                                               
    
    Player one Control: This is to change the control method of player one (the bat on the left) 
                                Their values::[KEYS, AI, MOUSE]                            
    
    Player two Control: This is to change the control method of player two (the bat on the right)
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
    I have been putting of this part, but....later                                              

{_WhatsNext}
    Multiplayer is going to be improved in the next update apart from that, multitudes of fixes are
    going to happen, just be patient
    
{_Also}
    If any error was made in this menu or the game in general, I was tired bcos I have spent a lot 
    of time working on this game, so...sorry or whatever. I have finished my first term in school 
    and we are entering christmas holidays, so more things are coming. Thanks and see you soon :-)
    
{_Links}
`{LINK_KEY[0]}|`{LINK_KEY[1]}|`{LINK_KEY[2]}|`{LINK_KEY[3]}|






"""

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


# IF U WAN TO CONTINUE PLAY D GAME PROPER NO TOUCH DEES VALUES
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





