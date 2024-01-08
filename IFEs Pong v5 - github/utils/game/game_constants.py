
import pygame
from typing import Final

# Res constants and variables
_desktop_scr_width: Final = pygame.display.get_desktop_sizes()[0][0] - (pygame.display.get_desktop_sizes()[0][0] / 8.228915662650602)
_desktop_scr_height: Final = pygame.display.get_desktop_sizes()[0][1] - (pygame.display.get_desktop_sizes()[0][1] / 4.626506024096385)
SCR_SIZE: Final = (_desktop_scr_width, _desktop_scr_height)
FPS: Final = 100

# Player constants
CONTROL_OPTIONS: Final = ['MOUSE', 'AI', 'KEYS']
AI_DIFFICULTY_OPTIONS: Final = ['Very Hard', 'Hard', 'Normal', 'Medium', 'Easy']
HIT_OFFSET: Final = 30
EDGE_SPACE = P1_START_POS = 40
PLAYER_SIZE: Final = (20, 70)
PLAYER_SPEED = BALL_SPEED = .4

# Ball constants
BALL_RADIUS: Final = 5

# Mid-line constants
LINE_SPACE: Final = 5
LINE_LEN: Final = 20
LINE_WIDTH: Final = 3

# Important directory paths
CONTINUE_JSON_PATH: Final = 'utils/json/continue.json'
SETTINGS_JSON_PATH: Final = 'utils/json/settings.json'
ONWIDGETCLICKED_MP3_PATH: Final = 'utils/sounds/on_widget_clicked.mp3'
ONWIDGETFOCUS_WAV_PATH: Final = 'utils/sounds/on_widget_focus.wav'
LOGO_PNG_PATH: Final = 'utils/logos/logo.png'
ONHOVER_PNG_PATH: Final = 'utils/ui/onhover.png'
    
# Player constants
AI_RESPONSE_OFFSET: Final = 100
MAX_TIMER: Final = 100
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

# Help screen constants and variables
LINKS: Final = {
    'IFEs Itch page': 'https://ifeisachildofgod.itch.io/',
    'IFEs Pixel Runner': 'https://ifeisachildofgod.itch.io/ifes-pixel-runner',
    'IFEs YTVDownloader': 'https://ifeisachildofgod.itch.io/ifes-ytvideo-downloader',
    'IFEs Freelance': 'https://www.upwork.com/freelancers/~0113b8c14366fba047?referrer_url_path=%2Fab%2Fprofiles%2Fsearch%2Fdetails%2F~0113b8c14366fba047%2Fprofile',
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
HELP_SCR_START_POS: Final = 70

# Bluetooth constants
MAX_BT_RETRY: Final = 8

