
# Core environment constants

# Sreen constants
SCR_WIDTH = 1200
SCR_HEIGHT = 600
FOREGROUND_COL = (255, 255, 255, 255)
BACKGROUND_COL = (0, 0, 0, 255)
LINK_COL = 'grey'

# Characters contants
EDGE_SPACE = 40
PLAYER_SPEED = .1
BALL_SPEED = .1

# Mid-line constants
LINE_SPACE = 5
LINE_LEN = 20
LINE_WIDTH = 3

# As it clearly says 'help info' I don't need to further specify
LINKS = {
    'IFEs Itch page': 'https://ifeisachildofgod.itch.io/',
    'IFEs Pixel Runner': 'https://ifeisachildofgod.itch.io/ifes-pixel-runner',
    'IFEs YTVDownloader': 'https://ifeisachildofgod.itch.io/ifes-ytvideo-downloader'
}

_LINK_KEY = [k for k, _ in LINKS.items()]

HELP_INFO = f'''
INTRODUCTION
Hello my name is Nwufo Ifechukwu and this my version of pong but better. It was released on 
31st of July 2023 as you know it has taken me sometime to make and believe it or not this
is the most complicated and difficult project I have made so far. At the end of the screen
you will find some links you can go to to support me.

GAME PLAY AND UI
1) If you remember pong you will kow how to play it, click 'a' to toggle the control options of
player one (on the left) and 'i' for player two (on the right)
2) Click the ESCAPE button to go back to any of the previous windows and 'Enter' to activate it

3) The 'Resume', 'Restart' and 'Quit' menu options are very self explanitory and you know what 
they do

Future updates will include                                                                  

1) The options menu                                                                          
-   color scheme change option                                                               
-   character skin change                                                                    
-   font change                                                                              
-   ai difficulty                                                                            
-   default player choice                                                                    
-   others                                                                                   
2) Better sound effects                                                                      
3) Some bug fixes                                                                            
3) Better AI                                                                                 
4) Background music                                                                          
5) Others                                                                                    

Itch.io links `{_LINK_KEY[0]}|`{_LINK_KEY[1]}|`{_LINK_KEY[2]}|
'''

# Users are not to tamper with these values

# Player constants
AI_RESPONSE_OFFSET = 100
MAX_TIMER = 100

# Anything involving text constants
FN1_SIZE = 20
FN2_SIZE = 9.5
FN3_SIZE = 12
FONT_CELL_SIZE = 15

# Scoring text fonts as you can see
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

# Pause UI constants
PAUSE_TEXT_SPACING = 75
PAUSE_TEXT_START_POS = -150
X_PAUSE_TEXT_OFFSET = 150

# Option UI constants
OPTION_TEXT_SPACING = 100
OPTION_TEXT_START_POS = -260
X_OPTION_TEXT_OFFSET = 200

# Misc
EXIT_SPACE_OFFSET = 50
HIT_OFFSET = 10
TXT_PAD = 20
