
import pygame
from typing import Final

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
CONTINUE_VARIABLE_DIR = 'utils/json/continue.json'
SETTINGS_DIR = 'utils/json/settings.json'
STATS_DIR = 'utils/json/stats.json'

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

FONT1: Final = pygame.font.Font('utils/fonts/font(1).ttf',35)
FONT2: Final = pygame.font.Font('utils/fonts/font(2).ttf',35//2)
FONT3: Final = pygame.font.Font('utils/fonts/font(2).ttf',50//2)
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
    'SHIFT': pygame.K_LSHIFT,
    'SHIFT': pygame.K_RSHIFT,
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
    Hello there, this my version of pong but better. This is the 3rd and one of near final update.
    It has taken me a lot to make and this is the most complicated and difficult project I have made
    so far and users might look at it and think it was easy to make but a programmer who looks at
    the code and sees what I did in with python, a Windows 10 HP laptop and pygame will see why this
    was so hard, but that's just me talking. Below you will find some more info about the game and at
    the end of the screen you will find some links that I think you would like to see.

{_Updates}
    The ability to control the player to pause, resume and go back with your mouse has been added. 
    Your mouse can also be used to click on options and use the scroll wheel.
    
    The text fields have been vastly improved making text fields in pygame is not easy and I have  
    done my best to make it feel real.
    
    The Character Skin option has been removed. If you want to add skins and backgrounds, all you 
    have to do is to get an image you would like to use and add it to the folder called SKINS, then
    if the picture is for the background rename it to the background, if it is for the player      
    rename it to player and the same for ui and ball.
    Note: It is advisable to use a complete image not an image that has some transparent parts for 
    better performance.

    The Link Color option has been removed, I realised that you guys don't really need access to the 
    color of those sweet juicy links that you might want to click on and check out and support you know
    
    A major part of the update is the addition of a better UI, basically what you can do with your  
   keyboard you can do with the mouse. Pause, Back and resume buttons have been added to the game     
    (all at the top left of the screen). The pause button is in the main game, resume button is in   
    the pause menu, back button is in the settings and help menu screen (statistics coming later).

{_GameFeatursAndMenus}
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

{_information}
    As you have noticed a scroll wheel has been added to the information (formally known as help
    screen) screen to help you Get to the bottom of the page faster, you can also use home and  
    end to get to see the links that you might want to check out. I've also changed the name from
    Help to Information for certain reasons you may not understand

{_statistics}
    This is a new aspect of the update and it shows multple statistics that you probably don't   
               need but I will still give because I can. like longest play time, best score and others (coming soon)

{_WhatsNext}
    Multiplayer is going to be added in another update apart from that I have no idea, whatever
    bugs I find and things I can optimize I will optimize I will fix and optimize, If you find anything
    wrong comment on my itch page and I will get to it when I can. Links below at the end of the screen.
    And there were some other features I couldn't mention but you'll have to see them for yourself
    
{_Also}
    If any error was made in this menu or the game in general, I was tired and I don't care anymore
    because I am returning to school and missed the error. Thanks and bye for now.

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


