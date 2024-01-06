
import pygame

pygame.init()

# Sreen constants
SCR_WIDTH = 1300
SCR_HEIGHT = 600

# Characters contants
CONTROL_OPTIONS = ['KEYS', 'AI']
HIT_OFFSET = 30
EDGE_SPACE = 40
PLAYER_SPEED = .1
BALL_SPEED = .1
PLAYER_SIZE = [10, 70]

# Mid-line constants
LINE_SPACE = 5
LINE_LEN = 20
LINE_WIDTH = 3

# As it clearly says 'help info' I don't need to further specify
LINKS = {
    'IFEs Itch page': 'https://ifeisachildofgod.itch.io/',
    'IFEs Pixel Runner': 'https://ifeisachildofgod.itch.io/ifes-pixel-runner',
    'IFEs YTVDownloader': 'https://ifeisachildofgod.itch.io/ifes-ytvideo-downloader',
    'IFEs Freelance':'https://www.upwork.com/freelancers/~0113b8c14366fba047?referrer_url_path=%2Fab%2Fprofiles%2Fsearch%2Fdetails%2F~0113b8c14366fba047%2Fprofile'  # 'https://www.upwork.com/ab/profiles/search/details/~0113b8c14366fba047/profile?q=Nwufo%20I&pageTitle=Profile&_navType=slider&_modalInfo=%5B%7B%22navType%22%3A%22slider%22,%22title%22%3A%22Profile%22,%22modalId%22%3A%221691953362387%22%7D%5D'
}

_LINK_KEY = [k for k, _ in LINKS.items()]

HELP_INFO = f'''
INTRODUCTION
Hello my name is Nwufo Ifechukwu and this my version of pong but better. It was released on 
31st of July 2023 and this the update which was released on 14 on August 2023.
As you know it has taken me sometime to make and believe it or not this
is the most complicated and difficult project I have made so far. At the end of the screen
you will find some links you can go to to support me.

UPDATES

1) The biggest update is that the settings menu has been added (In the previous version it      
was referenced as option but I think settings is a better name)                                
    - Under the settings menu there are 7 options: Background color, Foreground color,         
        Link color, player one and player two control, AI Difficulty and Character skin.       
        Their names are self explanitory                                                       

    - AI Difficulty is a selector type input, the control pickers are the inputs where you     
        click the key you want and it is updated (a key is a single character) while the       
        other inputs are text fields                                                           

    - The color text fields accepts string inputs like "blue", "green" and "black", It also    
        accepts RGBA inputs but if you have checked it out you will find out that you can't    
        input brackets or braces so if you want to input yellow in RGBA instead of inputing    
        "(255, 255, 0, 255)" you instead input "255, 255, 0, 255", Same with hex values instead
        of "#123123" you input "123123" ad the game will automatically compute it.             

2) The game mechanics have been better optimized to fit the orignal pong game and bug fixes     
have been made to the player one character especially, (fixes have also been made to other     
aspects of the game) and the size of the characters have been changed also                     

3) A better AI has been added and in a future update I will use machine learning to train       
the AI instead of using the current method I am using                                         

4) Some other miscellaneous updates were made link the blinking of the focus rectangles has     
been increased or the movement of the scores to align with the center properly and some others

GAME PLAY AND UI

1) If you remember pong you will kow how to play it, click 'a' to toggle the control options of
player one (on the left) and 'i' for player two (on the right), the default control for player
one is 'w' for up and 's' for down while for player two it the UP for up and the DOWN button  
for down                                                                                    

2) Click the ESCAPE button to go back to any of the previous windows and ENTER to activate and
deactivate any option that is in focus                                                      

3) For now you will have to manually type in the directory so it is advisable to have it in the
same directory as the main.py file. So if you have a file named "foo.jpg" in the file named 
folder utils, you input "utils/foo.jpg" or if it is in the directory where main.py is in you
input "foo.jpg"                                                                             

4) If you want to add a new key control setting just click the key when the option is in focus
and to toggle between up and down movement just click home to go to the down option and home
for the up option                                                                            

Future updates will include                                                                  

1) Better sound effects                                                                      
2) Text field bug fixes                                                                       
3) An option in the settings menu used for changing the control option, ie "KEYS and AI"      
remotely from the main game                                                                 

Links that I think you should check out
`{_LINK_KEY[0]}|`{_LINK_KEY[1]}|`{_LINK_KEY[2]}|`{_LINK_KEY[3]}|
'''

# Player constants
AI_RESPONSE_OFFSET = 100
MAX_TIMER = 100

# Anything involving text constants
FN1_SIZE = 20
FN2_SIZE = 9.5
FN3_SIZE = 12
FONT_CELL_SIZE = 15

# Fonts used
FONT1 = pygame.font.Font('utils/fonts/font(1).ttf',35)
FONT2 = pygame.font.Font('utils/fonts/font(2).ttf',35//2)
FONT3 = pygame.font.Font('utils/fonts/font(2).ttf',50//2)
FONT4 = pygame.font.Font(size=50)

SCORE_FONTS = [
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
####
   #
   #
   #
   #
   #
######
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

# Constants involving text
FOCUS_RECT_WIDTH = 2
TXT_PAD = 20
MAX_TV_LEN = 20

# Pause UI constants
PAUSE_TEXT_SPACING = 75
PAUSE_TEXT_START_POS = -150
X_PAUSE_TEXT_OFFSET = 150

# Option UI constants
OPTION_TEXT_SPACING = 80
OPTION_TEXT_START_POS = -270
X_OPTION_TEXT_OFFSET = 200

# Misc
EXIT_SPACE_OFFSET = 50
OPTION_SPACE_OFFSET = 40
BLINK_TIMER = 5
EXTRA_HELP_Y_OFFSET = 100
SCROLL_SPEED = 9

SPECIAL_KEYS = {
    'SPACE': pygame.K_SPACE,
    'TAB': pygame.K_TAB,
    'LEFT': pygame.K_LEFT,
    'SHIFT': pygame.K_LSHIFT,
    'SHIFT': pygame.K_RSHIFT,
    'SPACE': pygame.K_SPACE,
    'RIGHT': pygame.K_RIGHT,
    'UP': pygame.K_UP,
    'DOWN': pygame.K_DOWN,
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

CURSOR_ADJUST = {
 'a': 2,
 'b': 3,
 'c': 0,
 'd': 3,
 'e': 1,
 'f': 0,
 'g': 1,
 'h': 3.4,
 'i': -6,
 'j': -5,
 'k': 2,
 'l': -7,
 'm': 10,
 'n': 3.2,
 'o': 4,
 'p': 4,
 'q': 4,
 'r': 0,
 's': 0,
 't': -2,
 'u': 3,
 'v': 3,
 'w': 8,
 'x': 2,
 'y': 1,
 'z': 1,
 '1': 0,
 '2': 2.5,
 '3': 2.3,
 '4': 3.2,
 '5': 2,
 '6': 3,
 '7': 2,
 '8': 2,
 '9': 2.3,
 '0': 2,
 ',': -7,
 '.': -7,
 '`': -4,
 ';': -4,
 '#': 4.9,
 '(': -3,
 ')': -3,
 '\'': -3,
 '\\': -3,
 '/': -3,
 '[': -3,
 ']': -3,
 ' ': 0,
 }



