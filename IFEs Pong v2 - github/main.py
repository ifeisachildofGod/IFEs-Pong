import pygame
import sys
import json
import threading as thread
from utils.characters import Player, Ball
from utils.constants import (
                            BALL_SPEED, EDGE_SPACE, FN1_SIZE,
                            FN2_SIZE, TXT_PAD, HELP_INFO,
                            PAUSE_TEXT_START_POS, X_PAUSE_TEXT_OFFSET, FONT_CELL_SIZE,
                            PLAYER_SPEED, SCR_WIDTH, SCR_HEIGHT,
                            EXIT_SPACE_OFFSET, FN3_SIZE, PAUSE_TEXT_SPACING,
                            LINE_SPACE, LINE_LEN, LINKS,
                            LINE_WIDTH, X_OPTION_TEXT_OFFSET, OPTION_TEXT_SPACING,
                            OPTION_TEXT_START_POS, FOCUS_RECT_WIDTH, CONTROL_OPTIONS,
                            FONT1, FONT2, FONT3,
                            FONT4, OPTION_SPACE_OFFSET, CURSOR_ADJUST,
                            SPECIAL_KEYS, BLINK_TIMER, EXTRA_HELP_Y_OFFSET,
                            SCROLL_SPEED
                            )
import utils.mods as mods
import time
import pyuac
import pywintypes
import os

@pyuac.main_requires_admin
def main():
    pygame.init()

    screen = pygame.display.set_mode((SCR_WIDTH,SCR_HEIGHT))

    pygame.display.set_caption('IFEs Pong')
    logo = pygame.image.load('utils\\logos\\pong_logo.png')
    pygame.display.set_icon(logo)
    clock = pygame.time.Clock()

    with open('utils/settings.json') as file:
        saved_data = json.loads(file.read())
        
        bg_txt_view_input = bg_color = saved_data['bg_color']
        fg_txt_view_input = fg_color = saved_data['fg_color']
        link_txt_view_input = link_color = saved_data['link_color']
        skin_txt_view_input = skin = mods.check_valid_file_name(saved_data['skin'])

        ad_index = saved_data['ad_index']

        player1_up_txt_view_input = key1_up = saved_data['key1_up']
        player1_down_txt_view_input = key1_down = saved_data['key1_down']
        player2_up_txt_view_input = key2_up = saved_data['key2_up']
        player2_down_txt_view_input = key2_down = saved_data['key2_down']

    col = fg_color
    col2 = fg_color

    ai_difficulty_settings = ['Easy', 'Medium', 'Normal', 'Hard', 'Impossible']
    ai_difficulty = ai_difficulty_settings[ad_index]

    player1_up, key1_up = mods.get_correct_control_key(key1_up, '1u')
    player1_down, key1_down = mods.get_correct_control_key(key1_down, '1d')
    player2_up, key2_up = mods.get_correct_control_key(key2_up, '2u')
    player2_down, key2_down = mods.get_correct_control_key(key2_down, '2d')

    player1 = Player(screen, SCR_WIDTH//2, EDGE_SPACE)
    player2 = Player(screen, SCR_WIDTH//2, SCR_WIDTH-EDGE_SPACE)

    ball = Ball(screen)

    pause_focus = 0
    setting_focus = 0

    start_opt_foc = setting_focus

    scr_focus = 0
    mouse_pressed = False
    paused_scr = False
    settings = False
    help_scr = False
    setting_name_focused = True
    thread1_started = True
    thread2_started = True
    typing = False

    control_index1 = 1
    control_index2 = 0
    start_timer = time.time()
    words = []
    cursor = len(bg_txt_view_input)
    just_started = True

    while True:
        cur_time = time.time()
        delay_time = 4
        fps  = clock.get_fps()

        if cur_time >= start_timer+delay_time:
            mouse = pygame.mouse.get_pos()
            mouse_rect = pygame.Rect(mouse[0],mouse[1],2,3)

            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

                if pygame.mouse.get_pressed()[0]:mouse_pressed = True

                keys = pygame.key.get_pressed()

                if keys[pygame.K_ESCAPE] and not help_scr and not settings:
                    paused_scr = not paused_scr
                
                if not paused_scr and not help_scr and not settings:
                    if event.type == pygame.KEYDOWN:
                        if keys[pygame.K_a]:
                            control_index1 += 1
                            control_index1 = mods.repeat(control_index1, len(CONTROL_OPTIONS)-1, 0)
                        if keys[pygame.K_i]:
                            control_index2 += 1
                            control_index2 = mods.repeat(control_index2, len(CONTROL_OPTIONS)-1, 0)
                else:
                    paused_rects = [k for k, _ in pause_text_rects.items()]
                    setting_rects = [k for k, _ in setting_text_rects.items()]
                    
                    shift_pressed = keys[pygame.K_RSHIFT] or keys[pygame.K_LSHIFT] 
                    
                    if event.type == pygame.KEYDOWN:
                        
                        if not help_scr and not settings:
                            if keys[pygame.K_UP]:
                                pause_focus-=1
                                pause_focus = mods.clamp(pause_focus, len(paused_rects)-1, 0)
                            elif keys[pygame.K_DOWN]:
                                pause_focus+=1
                                pause_focus = mods.clamp(pause_focus, len(paused_rects)-1, 0)
                            if keys[pygame.K_RETURN]:
                                time_it = time.time()
                                if paused_rects[pause_focus] == 'Exit':
                                    pygame.quit()
                                    sys.exit()
                                elif paused_rects[pause_focus] == 'Help':
                                    help_scr = not help_scr
                                elif paused_rects[pause_focus] == 'Resume':
                                    paused_scr = False
                                elif paused_rects[pause_focus] == 'Restart':
                                    player1 = Player(screen, SCR_WIDTH//2, EDGE_SPACE)
                                    player2 = Player(screen, SCR_WIDTH//2, SCR_WIDTH-EDGE_SPACE)
                                    ball = Ball(screen)
                                    player1_score = 0
                                    player2_score = 0
                                    paused_scr = False
                                    pause_focus = 0
                                elif paused_rects[pause_focus] == 'Settings':
                                    settings = not settings
                        else:
                            if keys[pygame.K_ESCAPE]:
                                if help_scr:
                                    paused_scr = True
                                    help_scr = False
                                elif settings:
                                    if setting_name_focused:
                                        paused_scr = True
                                        settings = False
                                    else:
                                        setting_name_focused = False
                            if settings:
                                if setting_rects[setting_focus] == 'AI Difficulty opt':
                                    if keys[pygame.K_RIGHT]:
                                        ad_index += 1
                                    elif keys[pygame.K_LEFT]:
                                        ad_index -= 1
                                    ad_index = mods.clamp(ad_index, len(ai_difficulty_settings) - 1, 0)
                                    ai_difficulty = ai_difficulty_settings[ad_index]
                                
                                if setting_rects[setting_focus] in ('Background Color opt', 'Foreground Color opt', 'Link Color opt', 'Character Skin opt'):
                                    if keys[pygame.K_LEFT]:
                                        cursor -= 1
                                        cursor = mods.clamp(cursor, len(words), 0)
                                    elif keys[pygame.K_RIGHT]:
                                        cursor += 1
                                        cursor = mods.clamp(cursor, len(words), 0)
                                    try:
                                        if keys[pygame.K_BACKSPACE]:
                                            if setting_rects[setting_focus] in ('Background Color opt', 'Foreground Color opt', 'Link Color opt', 'Character Skin opt'):
                                                cursor -= 1
                                                words[cursor] = '@'
                                                words.remove('@')
                                                cursor = mods.clamp(cursor, len(words), 0)
                                                if setting_rects[setting_focus] == 'Background Color opt':
                                                    bg_txt_view_input = ''.join(words)
                                                elif setting_rects[setting_focus] == 'Foreground Color opt':
                                                    fg_txt_view_input = ''.join(words)
                                                elif setting_rects[setting_focus] == 'Link Color opt':
                                                    link_txt_view_input = ''.join(words)
                                                elif setting_rects[setting_focus] == 'Character Skin opt':
                                                    skin_txt_view_input = ''.join(words).lower()
                                    except IndexError:
                                        pass
                                    
                                    if setting_rects[setting_focus] == 'Background Color opt':
                                        if just_started:
                                            words.clear()
                                            for i in str(bg_txt_view_input):
                                                words.append(i)
                                                cursor = len(words)
                                            just_started = False
                                        for i in range(len(keys)):
                                            if keys[i] not in (keys[pygame.K_ESCAPE], keys[pygame.K_RETURN], keys[pygame.K_BACKSPACE]):
                                                cursor += 1
                                                words.insert(cursor, chr(i))
                                                cursor = mods.clamp(cursor, len(words), 0)
                                                bg_txt_view_input = ''.join(words)
                                    elif setting_rects[setting_focus] == 'Foreground Color opt':
                                        if just_started:
                                            words.clear()
                                            for i in fg_txt_view_input:
                                                words.append(i)
                                            cursor = len(words)
                                            just_started = False
                                        for i in range(len(keys)):
                                            if keys[i] and not keys[pygame.K_ESCAPE] and not keys[pygame.K_RETURN] and not keys[pygame.K_BACKSPACE]:
                                                cursor = mods.clamp(cursor, len(words), 0)
                                                words.insert(cursor, chr(i))
                                                cursor += 1
                                                fg_txt_view_input = ''.join(words)
                                    elif setting_rects[setting_focus] == 'Link Color opt':
                                        if just_started:
                                            words.clear()
                                            for i in link_txt_view_input:
                                                words.append(i)
                                            cursor = len(words)
                                            just_started = True
                                        for i in range(len(keys)):
                                            if keys[i] and not keys[pygame.K_ESCAPE] and not keys[pygame.K_RETURN] and not keys[pygame.K_BACKSPACE]:
                                                cursor = mods.clamp(cursor, len(words), 0)
                                                words.insert(cursor, chr(i))
                                                cursor += 1
                                                link_txt_view_input = ''.join(words)
                                    elif setting_rects[setting_focus] == 'Character Skin opt':
                                        if just_started:
                                            words.clear()
                                            skin_txt_view_input = str(skin_txt_view_input).lower()
                                            for i in skin_txt_view_input:
                                                words.append(i)
                                            cursor = len(words)
                                            just_started = False
                                        for i in range(len(keys)):
                                            if keys[i] and not keys[pygame.K_ESCAPE] and not keys[pygame.K_RETURN] and not keys[pygame.K_BACKSPACE]:
                                                cursor = mods.clamp(cursor, len(words), 0)
                                                words.insert(cursor, chr(i))
                                                cursor += 1
                                                skin_txt_view_input = ''.join(words).lower()
                                else:
                                    just_started = True
                                    words.clear()

                                if setting_rects[setting_focus] in ('control1up opt', 'control1down opt', 'control2up opt', 'control2down opt'):
                                    if setting_rects[setting_focus] == 'control1up opt':
                                        for i in range(len(keys)):
                                            if keys[i] and not keys[pygame.K_ESCAPE] and not keys[pygame.K_RETURN] and not keys[pygame.K_BACKSPACE]:
                                                player1_up_txt_view_input = chr(i)
                                            for k, v in list(zip([k for k, _ in SPECIAL_KEYS.items()], [v for _, v in SPECIAL_KEYS.items()])):
                                                if keys[v]:
                                                    player1_up_txt_view_input = k
                                    elif setting_rects[setting_focus] == 'control1down opt':
                                        for i in range(len(keys)):
                                            if keys[i] and not keys[pygame.K_ESCAPE] and not keys[pygame.K_RETURN] and not keys[pygame.K_BACKSPACE]:
                                                player1_down_txt_view_input = chr(i)
                                            for k, v in list(zip([k for k, _ in SPECIAL_KEYS.items()], [v for _, v in SPECIAL_KEYS.items()])):
                                                if keys[v]:
                                                    player1_down_txt_view_input = k
                                    elif setting_rects[setting_focus] == 'control2up opt':
                                        for i in range(len(keys)):
                                            if keys[i] and not keys[pygame.K_ESCAPE] and not keys[pygame.K_RETURN] and not keys[pygame.K_BACKSPACE]:
                                                player2_up_txt_view_input = chr(i)
                                            for k, v in list(zip([k for k, _ in SPECIAL_KEYS.items()], [v for _, v in SPECIAL_KEYS.items()])):
                                                if keys[v]:
                                                    player2_up_txt_view_input = k
                                    elif setting_rects[setting_focus] == 'control2down opt':
                                        for i in range(len(keys)):
                                            if keys[i] and not keys[pygame.K_ESCAPE] and not keys[pygame.K_RETURN] and not keys[pygame.K_BACKSPACE]:
                                                player2_down_txt_view_input = chr(i)
                                            for k, v in list(zip([k for k, _ in SPECIAL_KEYS.items()], [v for _, v in SPECIAL_KEYS.items()])):
                                                if keys[v]:
                                                    player2_down_txt_view_input = k
                                
                                
                                if setting_name_focused:
                                    if keys[pygame.K_UP]:
                                        setting_focus-=1
                                        setting_focus = mods.clamp(setting_focus, (len(setting_rects)-3)//2, 0)
                                        start_opt_foc = setting_focus
                                    elif keys[pygame.K_DOWN]:
                                        setting_focus+=1
                                        setting_focus = mods.clamp(setting_focus, (len(setting_rects)-3)//2, 0)
                                        start_opt_foc = setting_focus
                                else:
                                    if setting_rects[setting_focus] == 'control1up opt':
                                        if keys[pygame.K_END]:
                                            setting_focus = setting_rects.index('control1down opt')
                                    elif setting_rects[setting_focus] == 'control1down opt':
                                        if keys[pygame.K_HOME]:
                                            setting_focus = setting_rects.index('control1up opt')
                                    elif setting_rects[setting_focus] == 'control2up opt':
                                        if keys[pygame.K_END]:
                                            setting_focus = setting_rects.index('control2down opt')
                                    elif setting_rects[setting_focus] == 'control2down opt':
                                        if keys[pygame.K_HOME]:
                                            setting_focus = setting_rects.index('control2up opt')

                                if keys[pygame.K_RETURN]:
                                    setting_name = [k for k, _ in setting_texts.items()]
                                    setting_name_focused = not setting_name_focused
                                    column_len = (len(setting_rects)-2) // 2
                                    if setting_rects[setting_focus] in setting_name:
                                        setting_focus += column_len
                                    setting_focus = mods.clamp(setting_focus, len(setting_rects)-1, 0)
                                    
                                    if setting_name_focused:
                                        setting_focus = start_opt_foc

            pause_texts = {
                'Exit': mods.font_renderer('Exit', FONT3, fg_color),
                'Settings': mods.font_renderer('Settings', FONT3, fg_color),
                'Resume': mods.font_renderer('Resume', FONT3, fg_color),
                'Help': mods.font_renderer('Help', FONT3, fg_color),
                'Restart': mods.font_renderer('Restart', FONT3, fg_color)
            }
            pause_text_rects = {
                'Resume': mods.font_rect_renderer('Resume', FN3_SIZE,y_offset=PAUSE_TEXT_START_POS, x_offset= X_PAUSE_TEXT_OFFSET),
                'Settings': mods.font_rect_renderer('Settings', FN3_SIZE,y_offset=PAUSE_TEXT_START_POS + PAUSE_TEXT_SPACING, x_offset= -X_PAUSE_TEXT_OFFSET),
                'Help': mods.font_rect_renderer('Help', FN3_SIZE, y_offset=PAUSE_TEXT_START_POS + PAUSE_TEXT_SPACING*2, x_offset= X_PAUSE_TEXT_OFFSET),
                'Restart': mods.font_rect_renderer('Restart', FN3_SIZE, y_offset=PAUSE_TEXT_START_POS + (PAUSE_TEXT_SPACING*3), x_offset= -X_PAUSE_TEXT_OFFSET),
                'Exit': mods.font_rect_renderer(' Exit', FN3_SIZE, y_offset=PAUSE_TEXT_START_POS + (PAUSE_TEXT_SPACING*4))
            }

            setting_texts = {
                'Background Color': mods.font_renderer('Background Color', FONT3, fg_color),
                'Foreground Color': mods.font_renderer('Foreground Color', FONT3, fg_color),
                'Link Color': mods.font_renderer('Link Color', FONT3, fg_color),
                'Player one Control': mods.font_renderer('Player one Control', FONT3, fg_color),
                'Player two Control': mods.font_renderer('Player two Control', FONT3, fg_color),
                'AI Difficulty': mods.font_renderer('AI Difficulty', FONT3, fg_color),
                'Character Skin': mods.font_renderer('Character Skin', FONT3, fg_color),

                'Background Color opt': mods.font_renderer(bg_txt_view_input, FONT3, fg_color),
                'Foreground Color opt': mods.font_renderer(fg_txt_view_input, FONT3, fg_color),
                'Link Color opt': mods.font_renderer(link_txt_view_input, FONT3, fg_color),
                'control1up opt': mods.font_renderer(f'Up: {player1_up_txt_view_input}', FONT3, fg_color),
                'control2up opt': mods.font_renderer(f'Up: {player2_up_txt_view_input}', FONT3, fg_color),
                'AI Difficulty opt': mods.font_renderer(ai_difficulty, FONT3, fg_color),
                'Character Skin opt': mods.font_renderer(skin_txt_view_input, FONT3, fg_color),
                
                'control1down opt': mods.font_renderer(f'Down: {player1_down_txt_view_input}', FONT3, fg_color),
                'control2down opt': mods.font_renderer(f'Down: {player2_down_txt_view_input}', FONT3, fg_color),
            }
            setting_text_rects = {
                'Background Color': mods.font_rect_renderer('Background Color', FN3_SIZE,y_offset=OPTION_TEXT_START_POS, x_offset= -X_OPTION_TEXT_OFFSET),
                'Foreground Color': mods.font_rect_renderer('Foreground Color', FN3_SIZE,y_offset=OPTION_TEXT_START_POS + OPTION_TEXT_SPACING, x_offset= -X_OPTION_TEXT_OFFSET),
                'Link Color': mods.font_rect_renderer('Link Color', FN3_SIZE,y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*2), x_offset= -X_OPTION_TEXT_OFFSET),
                'Player one Control': mods.font_rect_renderer('Player one Control', FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*3), x_offset= -X_OPTION_TEXT_OFFSET),
                'Player two Control': mods.font_rect_renderer('Player two Control', FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*4), x_offset= -X_OPTION_TEXT_OFFSET),
                'AI Difficulty': mods.font_rect_renderer('AI Difficulty', FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*5), x_offset= -X_OPTION_TEXT_OFFSET),
                'Character Skin': mods.font_rect_renderer('Character Skin', FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*6), x_offset= -X_OPTION_TEXT_OFFSET),

                'Background Color opt': mods.font_rect_renderer(bg_txt_view_input, FN3_SIZE,y_offset=OPTION_TEXT_START_POS, x_offset= X_OPTION_TEXT_OFFSET),
                'Foreground Color opt': mods.font_rect_renderer(fg_txt_view_input, FN3_SIZE,y_offset=OPTION_TEXT_START_POS + OPTION_TEXT_SPACING, x_offset= X_OPTION_TEXT_OFFSET),
                'Link Color opt': mods.font_rect_renderer(link_txt_view_input, FN3_SIZE,y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*2), x_offset= X_OPTION_TEXT_OFFSET),
                'control1up opt': mods.font_rect_renderer(f'Up: {player1_up_txt_view_input}', FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*3), x_offset= X_OPTION_TEXT_OFFSET - FN3_SIZE*6),#*len('UP: ')),
                'control2up opt': mods.font_rect_renderer(f'Up: {player2_up_txt_view_input}', FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*4), x_offset= X_OPTION_TEXT_OFFSET - FN3_SIZE*6),#*len(f'UP: ')),
                'AI Difficulty opt': mods.font_rect_renderer(ai_difficulty, FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*5), x_offset= X_OPTION_TEXT_OFFSET),
                'Character Skin opt': mods.font_rect_renderer(skin_txt_view_input, FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*6), x_offset= X_OPTION_TEXT_OFFSET),
            
                'control1down opt': mods.font_rect_renderer(f'Down: {player1_down_txt_view_input}', FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*3), x_offset= X_OPTION_TEXT_OFFSET + FN3_SIZE*8.5),
                'control2down opt': mods.font_rect_renderer(f'Down: {player2_down_txt_view_input}', FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*4), x_offset= X_OPTION_TEXT_OFFSET + FN3_SIZE*8.5)
            }

            if not paused_scr and not help_scr and not settings:
                screen.fill(bg_color)
                ball_rect = ball.get_rect()
                player1_rect = player1.get_rect_vals()
                player2_rect = player2.get_rect_vals()
                player2_score, player1_score = ball.get_score()
                
                mods.draw_nums(player1_score, (SCR_WIDTH//2) - (8*FONT_CELL_SIZE)-9, 0, FONT_CELL_SIZE, screen, col=fg_color)
                mods.draw_nums(player2_score, (SCR_WIDTH//2) + (FONT_CELL_SIZE//2), 0, FONT_CELL_SIZE, screen, col=fg_color)
                
                player1.update(CONTROL_OPTIONS[control_index1], [ball_rect, ball.ball_x_pos], True, speed=(PLAYER_SPEED*fps), col=fg_color, ai_difficulty=ai_difficulty, skin=skin, up=player1_up, down=player1_down)
                player2.update(CONTROL_OPTIONS[control_index2], [ball_rect, ball.ball_x_pos], False, speed=(PLAYER_SPEED*fps), col=fg_color, ai_difficulty=ai_difficulty, skin=skin, up=player2_up, down=player2_down)
                ball.update(BALL_SPEED*fps, *(player1_rect, player2_rect), col=fg_color)
                
                spacing = LINE_SPACE

                for i in range(SCR_HEIGHT//LINE_LEN):
                    l_x_pos = SCR_WIDTH//2 - (LINE_WIDTH//2)
                    pygame.draw.line(screen, fg_color, (l_x_pos, spacing), (l_x_pos, spacing + LINE_LEN), LINE_WIDTH)
                    spacing += LINE_LEN + LINE_SPACE
                
                screen.blit(FONT2.render('Click ESC to pause', False, fg_color), (1, 1))
                screen.blit(FONT2.render(CONTROL_OPTIONS[control_index1], False, fg_color), (len(CONTROL_OPTIONS[control_index1]), SCR_HEIGHT-FN2_SIZE*2))
                screen.blit(FONT2.render(CONTROL_OPTIONS[control_index2], False, fg_color), (SCR_WIDTH-(FN2_SIZE*len(CONTROL_OPTIONS[control_index2])+FN2_SIZE+3), SCR_HEIGHT-FN2_SIZE*2))

            else:
                timer = str(round(time.time(), 1))[-1]
                screen.fill(bg_color)
                pause_outline = pygame.Rect(pause_text_rects[paused_rects[pause_focus]].x - EXIT_SPACE_OFFSET//2, pause_text_rects[paused_rects[pause_focus]].y,
                                    pause_texts[paused_rects[pause_focus]].get_width() + EXIT_SPACE_OFFSET, pause_texts[paused_rects[pause_focus]].get_height())
                if int(timer)%BLINK_TIMER in (0,1):col = fg_color
                elif int(timer)%BLINK_TIMER in (2,3):col = bg_color

                pygame.draw.rect(screen, col, pause_outline, 2)
                screen.blit(FONT1.render('Game Paused', False, fg_color), (mods.position(SCR_WIDTH, 'center', 'Game Paused', 57//2.2), 40))
                screen.blit(FONT3.render('Click Enter to pick a menu', False, fg_color), (0, 0))
                screen.blit(pause_texts['Settings'], pause_text_rects['Settings'])
                screen.blit(pause_texts['Help'], pause_text_rects['Help'])
                screen.blit(pause_texts['Restart'], pause_text_rects['Restart'])
                screen.blit(pause_texts['Resume'], pause_text_rects['Resume'])
                screen.blit(pause_texts['Exit'], pause_text_rects['Exit'])
                if help_scr:
                    if keys[pygame.K_UP]:
                        scr_focus -= SCROLL_SPEED
                    if keys[pygame.K_DOWN]:
                        scr_focus += SCROLL_SPEED
                    
                    screen.fill(bg_color)
                    y_val = 70
                    vals, surf, one_line = mods.multiline_write(HELP_INFO, 85, FONT3, fore_col = fg_color, link_col=link_color)
                    
                    screen.blit(FONT1.render('IFEs Pong', False, fg_color), pygame.Rect(mods.position(SCR_WIDTH, 'center', 'IFEs Pong', FN1_SIZE), -50+mods.clamp(y_val-scr_focus, y_val, -(FN3_SIZE+TXT_PAD)), 0, 0))
                    scr_focus = mods.clamp(scr_focus, (((len(HELP_INFO.split('\n')) * FN3_SIZE)+y_val)*2) + EXTRA_HELP_Y_OFFSET , 0)
                    if not one_line:
                        for k, v in enumerate(surf):
                            x = mods.position(SCR_WIDTH, 'center', vals[k], FN3_SIZE)
                            y = mods.clamp(y_val-scr_focus, y_val, -(FN3_SIZE+TXT_PAD))
                            screen.blit(v, pygame.Rect(x, y, 0, 0))
                            if v.get_colorkey() == mods.font_renderer('This is Ife\'s test', FONT3, link_color).get_colorkey():
                                txt_size = v.get_rect().size
                                link_rect = pygame.Rect(x, y, txt_size[0], txt_size[1])
                                if mouse_rect.colliderect(link_rect):
                                    pygame.draw.line(screen, link_color, (x, y + FN3_SIZE*2.5), (x + txt_size[0], y + FN3_SIZE*2.5), 2)
                                    if mouse_pressed:
                                        link = vals[k].replace('!', '')
                                        link_starter = thread.Thread(target=mods.link_opener, args=(LINKS.get(link),))
                                        link_starter.start()
                                        mouse_pressed = False

                            y_val += FN3_SIZE+TXT_PAD
                    else:
                        screen.blit(surf, pygame.Rect(mods.position(SCR_WIDTH, 'center', vals, FN3_SIZE), y_val, 0, 0))
                    
                    screen.blit(pygame.transform.rotate(FONT4.render('<' if scr_focus >= 3 else '', False, fg_color), -90), (SCR_WIDTH-50, 12))
                    screen.blit(pygame.transform.rotate(FONT4.render('<' if scr_focus <= ((len(HELP_INFO.split('\n')) * FN3_SIZE)+y_val//2.6) + EXTRA_HELP_Y_OFFSET else '', False, fg_color), 90), (SCR_WIDTH-50, SCR_HEIGHT-30))

                elif settings:
                    screen.fill(bg_color)

                    timer2 = str(round(time.time(), 1))[-1]
                    
                    screen.fill(bg_color)

                    setting_outline = pygame.Rect(setting_text_rects[setting_rects[setting_focus]].x - OPTION_SPACE_OFFSET//2,
                                                setting_text_rects[setting_rects[setting_focus]].y,
                                                setting_texts[setting_rects[setting_focus]].get_width() + OPTION_SPACE_OFFSET,
                                                setting_texts[setting_rects[setting_focus]].get_height()
                                                )

                    pygame.draw.rect(screen, fg_color, setting_outline, FOCUS_RECT_WIDTH)

                    if int(timer2)%BLINK_TIMER in (0,1):col2 = fg_color
                    elif int(timer2)%BLINK_TIMER in (2,3):col2 = bg_color
                    
                    if not setting_name_focused:
                        if setting_rects[setting_focus] in ('Background Color opt', 'Foreground Color opt', 'Link Color opt',
                                                        'Character Skin opt', 'control1up opt', 'control1down opt',
                                                        'control2up opt', 'control2down opt'):
                            if setting_rects[setting_focus] in ('Background Color opt', 'Foreground Color opt', 'Link Color opt', 'Character Skin opt'):
                                if setting_rects[setting_focus] == 'Background Color opt':
                                    bg_cursor_x = setting_text_rects[setting_rects[setting_focus]].left + (FN3_SIZE) * len(str(bg_txt_view_input)[:cursor])
                                    for i in bg_txt_view_input:
                                        bg_cursor_x += CURSOR_ADJUST.get(i)
                                    pygame.draw.line(
                                                    screen,
                                                    col2,
                                                    (bg_cursor_x, setting_outline.bottom - FOCUS_RECT_WIDTH),
                                                    (bg_cursor_x, setting_outline.top + FOCUS_RECT_WIDTH)
                                                    )
                                elif setting_rects[setting_focus] == 'Foreground Color opt':
                                    fg_cursor_x = setting_text_rects[setting_rects[setting_focus]].left + (FN3_SIZE) * len(str(fg_txt_view_input)[:cursor])
                                    for i in fg_txt_view_input:
                                        fg_cursor_x += CURSOR_ADJUST.get(i)
                                    pygame.draw.line(
                                                    screen,
                                                    col2,
                                                    (fg_cursor_x, setting_outline.bottom - FOCUS_RECT_WIDTH),
                                                    (fg_cursor_x, setting_outline.top + FOCUS_RECT_WIDTH)
                                                    )
                                elif setting_rects[setting_focus] == 'Link Color opt':
                                    l_cursor_x = setting_text_rects[setting_rects[setting_focus]].left + (FN3_SIZE) * len(str(link_txt_view_input)[:cursor])
                                    for i in link_txt_view_input:
                                        l_cursor_x += CURSOR_ADJUST.get(i)
                                    pygame.draw.line(
                                                    screen,
                                                    col2,
                                                    (l_cursor_x, setting_outline.bottom - FOCUS_RECT_WIDTH),
                                                    (l_cursor_x, setting_outline.top + FOCUS_RECT_WIDTH)
                                                    )
                                elif setting_rects[setting_focus] == 'Character Skin opt':
                                    skin_cursor_x = setting_text_rects[setting_rects[setting_focus]].left + (FN3_SIZE) * len(str(skin_txt_view_input)[:cursor])
                                    for i in str(skin_txt_view_input).lower():
                                        skin_cursor_x += CURSOR_ADJUST.get(i)
                                    pygame.draw.line(
                                                    screen,
                                                    col2,
                                                    (skin_cursor_x, setting_outline.bottom - FOCUS_RECT_WIDTH),
                                                    (skin_cursor_x, setting_outline.top + FOCUS_RECT_WIDTH)
                                                    )
                            elif setting_rects[setting_focus] in ('control1up opt', 'control1down opt', 'control2up opt', 'control2down opt'):
                                if setting_rects[setting_focus] == 'control1up opt':
                                    player1_up_cursor_x = (FN3_SIZE * len('Up: ')) + setting_text_rects[setting_rects[setting_focus]].left + FN3_SIZE * len(player1_up_txt_view_input[:cursor])
                                elif setting_rects[setting_focus] == 'control1down opt':
                                    player1_down_cursor_x = (FN3_SIZE * len('Down: ')) + setting_text_rects[setting_rects[setting_focus]].left + (FN3_SIZE) * len(player1_down_txt_view_input[:cursor])
                                elif setting_rects[setting_focus] == 'control2up opt':
                                    player2_up_cursor_x = (FN3_SIZE * len('Up: ')) + setting_text_rects[setting_rects[setting_focus]].left + (FN3_SIZE) * len(player2_up_txt_view_input[:cursor])
                                elif setting_rects[setting_focus] == 'control2down opt':
                                    player2_down_cursor_x = (FN3_SIZE * len('Down: ')) + setting_text_rects[setting_rects[setting_focus]].left + (FN3_SIZE) * len(player2_down_txt_view_input[:cursor])
                    else:
                        if len(str(bg_txt_view_input).split(',')) == 4:
                            bg_txt_view_input = tuple(int(i) for i in str(bg_txt_view_input).removeprefix('(').removesuffix(')').removeprefix('[').removesuffix(']').split(','))
                        if len(str(fg_txt_view_input).split(',')) == 4:
                            fg_txt_view_input = tuple(int(i) for i in str(fg_txt_view_input).removeprefix('(').removesuffix(')').removeprefix('[').removesuffix(']').split(','))
                        if len(str(link_txt_view_input).split(',')) == 4:
                            link_txt_view_input = tuple(int(i) for i in str(link_txt_view_input).removeprefix('(').removesuffix(')').removeprefix('[').removesuffix(']').split(','))
                        
                        bg_color = mods.check_valid_color(bg_txt_view_input, bg_color)
                        bg_txt_view_input = mods.check_valid_color(bg_txt_view_input, bg_color)
                        
                        fg_color = mods.check_valid_color(fg_txt_view_input, fg_color)
                        fg_txt_view_input = mods.check_valid_color(fg_txt_view_input, fg_color)
                        
                        link_color = mods.check_valid_color(link_txt_view_input, link_color)
                        link_txt_view_input = mods.check_valid_color(link_txt_view_input, link_color)
                        
                        skin = mods.check_valid_file_name(skin_txt_view_input, skin)
                        skin_txt_view_input = mods.check_valid_file_name(skin_txt_view_input, skin)
                        
                        _, player1_up_txt_view_input = mods.get_correct_control_key(player1_up_txt_view_input, '1u')
                        player1_up, key1_up = mods.get_correct_control_key(player1_up_txt_view_input, '1u')
                        _, player1_down_txt_view_input = mods.get_correct_control_key(player1_down_txt_view_input, '1d')
                        player1_down, key1_down = mods.get_correct_control_key(player1_down_txt_view_input, '1d')
                        _, player2_up_txt_view_input = mods.get_correct_control_key(player2_up_txt_view_input, '2u')
                        player2_up, key2_up = mods.get_correct_control_key(player2_up_txt_view_input, '2u')
                        _, player2_down_txt_view_input = mods.get_correct_control_key(player2_down_txt_view_input, '2d')
                        player2_down, key2_down = mods.get_correct_control_key(player2_down_txt_view_input, '2d')
                        
                        with open('utils/settings.json', "w") as settings:
                            saved_data['bg_color'] = bg_color
                            saved_data['fg_color'] = fg_color
                            saved_data['link_color'] = link_color
                            saved_data['skin'] = skin
                            saved_data['ad_index'] = ad_index
                            saved_data['key1_up'] = key1_up
                            saved_data['key1_down'] = key1_down
                            saved_data['key2_up'] = key2_up
                            saved_data['key2_down'] = key2_down
                            
                            new_info = json.dumps(saved_data, indent=2)
                            settings.write(new_info)

                    screen.blit(setting_texts['Background Color'], setting_text_rects['Background Color'])
                    screen.blit(setting_texts['Foreground Color'], setting_text_rects['Foreground Color'])
                    screen.blit(setting_texts['Link Color'], setting_text_rects['Link Color'])
                    screen.blit(setting_texts['Player one Control'], setting_text_rects['Player one Control'])
                    screen.blit(setting_texts['Player two Control'], setting_text_rects['Player two Control'])
                    screen.blit(setting_texts['AI Difficulty'], setting_text_rects['AI Difficulty'])
                    screen.blit(setting_texts['Character Skin'], setting_text_rects['Character Skin'])
                    
                    screen.blit(setting_texts['Background Color opt'], setting_text_rects['Background Color opt'])
                    screen.blit(setting_texts['Foreground Color opt'], setting_text_rects['Foreground Color opt'])
                    screen.blit(setting_texts['Link Color opt'], setting_text_rects['Link Color opt'])
                    screen.blit(setting_texts['control1up opt'], setting_text_rects['control1up opt'])
                    screen.blit(setting_texts['control2up opt'], setting_text_rects['control2up opt'])
                    screen.blit(setting_texts['AI Difficulty opt'], setting_text_rects['AI Difficulty opt'])
                    screen.blit(setting_texts['Character Skin opt'], setting_text_rects['Character Skin opt'])

                    screen.blit(setting_texts['control1down opt'], setting_text_rects['control1down opt'])
                    screen.blit(setting_texts['control2down opt'], setting_text_rects['control2down opt'])

                    screen.blit(FONT4.render('>' if setting_rects[setting_focus] == 'AI Difficulty opt' and ad_index != len(ai_difficulty_settings) - 1 else '', False, col2), (setting_outline.right + 10, setting_outline.top))
                    screen.blit(FONT4.render('<' if setting_rects[setting_focus] == 'AI Difficulty opt' and ad_index != 0 else '', False, col2), (setting_outline.left - 30, setting_outline.top))

        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(bg_color)
            temp1_size = -10
            temp2_size = -50
            font4 = pygame.font.Font('utils/fonts/font(1).ttf',100)
            screen.blit(font4.render('IFES PONG', False, fg_color), (mods.position(SCR_WIDTH//2, 'center', 'IFES PONG',temp1_size), mods.position(SCR_HEIGHT//2, 'center', ' ',temp1_size)))
            screen.blit(FONT3.render(f'Starting in {round((start_timer+delay_time) - cur_time)+1}', False, fg_color), (mods.position(SCR_WIDTH//2, 'center', 'IFES PONG',temp2_size)+20, mods.position(SCR_HEIGHT//2, 'center', ' ',temp2_size)+mods.position(SCR_HEIGHT//2, 'center', ' ',temp1_size)))

        pygame.display.update()
        clock.tick(60)

if __name__ == '__main__':
    try:
        main()
    except (pywintypes.error, PermissionError):
        sys.exit()
    except AttributeError:
        stdout_temp_fn = 'pyuac.stdout.tmp.txt'
        stderr_temp_fn = 'pyuac.stderr.tmp.txt'
        if os.path.exists(stdout_temp_fn):
            os.remove(stdout_temp_fn)
        if os.path.exists(stderr_temp_fn):
            os.remove(stderr_temp_fn)

