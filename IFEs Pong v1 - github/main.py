import pygame
import sys
import threading as thread
from assets.settings import (
                            AI_RESPONSE_OFFSET,BALL_SPEED, EDGE_SPACE,
                            FN1_SIZE, FN2_SIZE, TXT_PAD,
                            HELP_INFO,PAUSE_TEXT_START_POS,
                            X_PAUSE_TEXT_OFFSET,FONT_CELL_SIZE, MAX_TIMER,
                            PLAYER_SPEED,SCR_WIDTH, SCR_HEIGHT,
                            EXIT_SPACE_OFFSET,FN3_SIZE, PAUSE_TEXT_SPACING,
                            LINE_SPACE,LINE_LEN,BACKGROUND_COL,
                            FOREGROUND_COL,HIT_OFFSET,LINK_COL,
                            LINKS,LINE_WIDTH)
import assets.mods as mods
import random
import time
import pyuac
import pywintypes
import os

@pyuac.main_requires_admin
def main():
    class Player:
        def __init__(self, mid_point, pos_x, pos_y = SCR_HEIGHT // 2, up = pygame.K_UP, down = pygame.K_DOWN, col = FOREGROUND_COL) -> None:
            self.player_rect = pygame.Rect(pos_x, pos_y,5,70)
            self.player_pos = 0
            self.speed = PLAYER_SPEED
            self.up = up
            self.down = down
            self.scr_height = SCR_HEIGHT
            self.player_ai = False
            self.offset = AI_RESPONSE_OFFSET
            self.mid_point = mid_point
            self.col = col
            
        def player_input(self, control: str, ball: pygame.Rect, left: bool):
            keys = pygame.key.get_pressed()
            if control == 'KEYS':
                    if keys[self.up]:self.player_pos = -1
                    elif keys[self.down]:self.player_pos = 1
                    else:self.player_pos = 0
            elif control == 'AI':
                active = ball.x > self.mid_point+self.offset if not left else ball.x < self.mid_point-self.offset
                if active:
                    if ball.y > self.player_rect.y:self.player_pos = 1
                    elif ball.y < self.player_rect.y:self.player_pos = -1
                    elif ball.y == self.player_rect.y:self.player_pos = 0
                else:
                    self.player_pos = 0

        def movement(self, speed):
            self.player_rect.y += (self.player_pos*speed)
            self.player_rect.y = mods.clamp(self.player_rect.y, self.scr_height-self.player_rect.height, 0)
        
        def get_rect_vals(self):
            return self.player_rect, self.player_pos
        
        def update(self, control: str, ball: pygame.Rect, left: bool, speed):
            self.player_input(control, ball, left)
            self.movement(speed)
            pygame.draw.rect(screen, self.col, self.player_rect)

    class Ball:
        def __init__(self, col = FOREGROUND_COL) -> None:
            self.scr_height = SCR_HEIGHT
            self.scr_width = SCR_WIDTH
            self.ball_rect = pygame.Rect(self.scr_width//2, self.scr_height//2, 10, 10)
            self.speed = BALL_SPEED
            self.score1 = 0
            self.score2 = 0
            self.scored = False 
            self.timer = 0
            self.ball_x_pos = random.choice([-1, 1])
            self.ball_y_pos = random.choice([-1, 1])
            self.col = col
            
        def collision(self, collide_rects):
            wall_hit = pygame.mixer.Sound(r'assets\sounds\wall_bounce.mp3')
            hit_bounce = pygame.mixer.Sound(r'assets\sounds\\hit_bounce.mp3')
            wall_hit.set_volume(.5)
            if (self.ball_rect.y >= self.scr_height-self.ball_rect.height) or (self.ball_rect.y <= 0):
                self.ball_y_pos *= -1
                wall_hit.play()

            if self.ball_rect.x >= self.scr_width-self.ball_rect.width:score2 = True
            else:score2 = False
            
            if self.ball_rect.x <= 0:score1 = True
            else:score1 = False
            
            if not self.scored and (score1 or score2):
                if not self.scored and score1:
                    self.score1 += 1
                    self.scored = True
                elif not self.scored and score2:
                    self.score2 += 1
                    self.scored = True

            if (self.ball_rect.x >= self.scr_width+self.ball_rect.width) or (self.ball_rect.x <= -(self.ball_rect.width*2)):
                self.timer += 1
                if self.timer >= MAX_TIMER:
                    self.speed = BALL_SPEED
                    self.ball_x_pos = 1 if self.ball_rect.x <= 0 else -1
                    self.ball_y_pos = random.choice([-1, 1])
                    self.ball_rect.x = self.scr_width//2
                    self.ball_rect.y = self.scr_height//2
                    self.timer = 0
                    self.scored = False
                else:
                    self.ball_rect.y = self.scr_height//2
                    self.ball_x_pos = 0
                    self.ball_y_pos = 0

            if collide_rects is not None:
                for collide_rect in collide_rects:
                    if (self.ball_rect.left <= collide_rect[0].right+HIT_OFFSET or self.ball_rect.right >= collide_rect[0].left-HIT_OFFSET) and self.ball_rect.colliderect(collide_rect[0]):
                        if collide_rect[1] + self.ball_y_pos == 0:
                            self.ball_y_pos = collide_rect[1]
                            if self.ball_y_pos != 0:
                                pass
                            else:
                                if (self.ball_rect.top - collide_rect[1].top) > (collide_rect[1].length // 2):self.ball_y_pos = 1
                                else:self.ball_y_pos = -1
                        else:pass
                        if self.ball_rect.left <= collide_rect[0].right+HIT_OFFSET:self.ball_rect.x += 5
                        if self.ball_rect.right >= collide_rect[0].left-HIT_OFFSET:self.ball_rect.x -= 5
                        self.ball_x_pos *= -1
                            
                        hit_bounce.play()
                    if (self.ball_rect.bottom == collide_rect[0].top or self.ball_rect.top == collide_rect[0].bottom) and self.ball_rect.colliderect(collide_rect[0]):
                        self.ball_y_pos *= -1

        def get_rect(self):
            return self.ball_rect

        def get_score(self):
            return self.score1, self.score2
        
        def movement(self, speed):
            self.ball_rect.x += self.ball_x_pos*speed
            self.ball_rect.y += self.ball_y_pos*speed

        def update(self, speed, *collide_rect: pygame.Rect):
            self.collision(collide_rect)
            self.movement(speed)
            pygame.draw.ellipse(screen, self.col, self.ball_rect)

    pygame.init()
    
    screen = pygame.display.set_mode((SCR_WIDTH,SCR_HEIGHT))
    pygame.display.set_caption('IFEs Pong')
    logo = pygame.image.load('assets\\logos\\pong_logo.png')
    pygame.display.set_icon(logo)
    clock = pygame.time.Clock()

    font1 = pygame.font.Font('assets/fonts/font(1).ttf',35)
    font2 = pygame.font.Font('assets/fonts/font(2).ttf',35//2)
    font3 = pygame.font.Font('assets/fonts/font(2).ttf',50//2)

    # Pause UI text surfs
    pause_texts = {
        'Exit': mods.font_renderer('Exit', font3),
        'Options': mods.font_renderer('Options', font3),
        'Resume': mods.font_renderer('Resume', font3),
        'Help': mods.font_renderer('Help', font3),
        'Restart': mods.font_renderer('Restart', font3)
    }
    # Pause UI text rects
    pause_text_rects = {
        'Resume': mods.font_rect_renderer('Resume', FN3_SIZE,y_offset=PAUSE_TEXT_START_POS, x_offset= X_PAUSE_TEXT_OFFSET),
        'Options': mods.font_rect_renderer('Options', FN3_SIZE,y_offset=PAUSE_TEXT_START_POS + PAUSE_TEXT_SPACING, x_offset= -X_PAUSE_TEXT_OFFSET),
        'Help': mods.font_rect_renderer('Help', FN3_SIZE, y_offset=PAUSE_TEXT_START_POS + PAUSE_TEXT_SPACING*2, x_offset= X_PAUSE_TEXT_OFFSET),
        'Restart': mods.font_rect_renderer('Restart', FN3_SIZE, y_offset=PAUSE_TEXT_START_POS + (PAUSE_TEXT_SPACING*3), x_offset= -X_PAUSE_TEXT_OFFSET),
        'Exit': mods.font_rect_renderer(' Exit', FN3_SIZE, y_offset=PAUSE_TEXT_START_POS + (PAUSE_TEXT_SPACING*4))
    }

    player1 = Player(SCR_WIDTH//2, EDGE_SPACE, up=pygame.K_w, down=pygame.K_s)
    player2 = Player(SCR_WIDTH//2, SCR_WIDTH-EDGE_SPACE)

    ball = Ball()

    pause_focus = 0
    option_focus = 0
    scr_focus = 0
    mouse_pressed = False
    paused_scr = False
    options = False
    help_scr = False
    option_name_focused = True

    control_index1 = 0
    control_index2 = 0
    control_options = ['KEYS', 'AI']
    start_timer =  time.time()

    while True:
        cur_time = time.time()
        delay_time = 4

        if cur_time >= start_timer+delay_time:
            mouse = pygame.mouse.get_pos()
            mouse_rect = pygame.Rect(mouse[0],mouse[1],2,3)
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                
                if pygame.mouse.get_pressed()[0]:mouse_pressed = True
                
                keys = pygame.key.get_pressed()
                
                if keys[pygame.K_ESCAPE] and not help_scr and not options:paused_scr = not paused_scr
                
                if not paused_scr and not help_scr and not options:
                    if event.type == pygame.KEYDOWN:
                        if keys[pygame.K_a]:
                            control_index1 += 1
                            control_index1 = mods.repeat(control_index1, (len(control_options)-1), 0)
                        if keys[pygame.K_i]:
                            control_index2 += 1
                            control_index2 = mods.repeat(control_index2, (len(control_options)-1), 0)
                        
                else:
                    paused_rects = [k for k, _ in pause_text_rects.items()]
                    # option_rects = [k for k, _ in option_text_rects.items()]
                    if event.type == pygame.KEYDOWN:
                        if not help_scr and not options:
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
                                    screen.fill(BACKGROUND_COL)
                                    screen.blit(font4.render('IFES PONG', False, FOREGROUND_COL), (mods.position(SCR_WIDTH//2, 'center', 'IFES PONG',temp1_size), mods.position(SCR_HEIGHT//2, 'center', ' ',temp1_size)))
                                    player1 = Player(SCR_WIDTH//2, EDGE_SPACE, SCR_HEIGHT//2, pygame.K_w, pygame.K_s)
                                    player2 = Player(SCR_WIDTH//2, SCR_WIDTH-EDGE_SPACE, SCR_HEIGHT//2, pygame.K_UP, pygame.K_DOWN)
                                    ball = Ball()
                                    player1_score = 0
                                    player2_score = 0
                                    paused_scr = False
                                    pause_focus = 0
                                elif paused_rects[pause_focus] == 'Options':
                                    options = not options
                        else:
                            if keys[pygame.K_ESCAPE]:
                                if help_scr:
                                    paused_scr = True
                                    help_scr = False
                                elif options:
                                    paused_scr = True
                                    options = False

            fps  = clock.get_fps()                    
            if not paused_scr and not help_scr and not options:
                pygame.draw.rect(screen, BACKGROUND_COL, pygame.Rect(0,0,SCR_WIDTH,SCR_HEIGHT))
                ball_rect = ball.get_rect()
                player1_rect = player1.get_rect_vals()
                player2_rect = player2.get_rect_vals()
                player2_score, player1_score = ball.get_score()
                
                mods.draw_nums(player1_score, (SCR_WIDTH//2)-(8*FONT_CELL_SIZE), 0, FONT_CELL_SIZE, screen)
                mods.draw_nums(player2_score, (SCR_WIDTH//2)+FONT_CELL_SIZE//2, 0, FONT_CELL_SIZE, screen)
                
                player1.update(control_options[control_index1], ball_rect, True, speed= (PLAYER_SPEED*fps))
                player2.update(control_options[control_index2], ball_rect, False, speed= (PLAYER_SPEED*fps))
                ball.update(BALL_SPEED*fps, *(player1_rect, player2_rect))
                
                spacing = LINE_SPACE

                for i in range(SCR_HEIGHT//LINE_LEN):
                    l_x_pos = SCR_WIDTH//2 - (LINE_WIDTH//2)
                    pygame.draw.line(screen, FOREGROUND_COL, (l_x_pos, spacing), (l_x_pos, spacing + LINE_LEN), LINE_WIDTH)
                    spacing += LINE_LEN + LINE_SPACE
                
                screen.blit(font2.render('Click ESC to pause', False, FOREGROUND_COL), (1, 1))
                screen.blit(font2.render(control_options[control_index1], False, FOREGROUND_COL), (len(control_options[control_index1]), SCR_HEIGHT-FN2_SIZE*2))
                screen.blit(font2.render(control_options[control_index2], False, FOREGROUND_COL), (SCR_WIDTH-(FN2_SIZE*len(control_options[control_index2])+FN2_SIZE+3), SCR_HEIGHT-FN2_SIZE*2))

            else:
                timer = str(round(time.time(), 1))
                t = timer[-1]
                screen.fill(BACKGROUND_COL)
                # pygame.draw.rect(screen, BACKGROUND_COL, pygame.Rect(0,0,SCR_WIDTH,SCR_HEIGHT))
                outline = pygame.Rect(pause_text_rects[paused_rects[pause_focus]].x - EXIT_SPACE_OFFSET//2, pause_text_rects[paused_rects[pause_focus]].y,
                                    pause_texts[paused_rects[pause_focus]].get_width() + EXIT_SPACE_OFFSET, pause_texts[paused_rects[pause_focus]].get_height())
                if int(t)%4 in (0,1):col = FOREGROUND_COL
                elif int(t)%4 in (2,3):col = BACKGROUND_COL
                
                pygame.draw.rect(screen, col, outline, 2)
                screen.blit(font1.render('Game Paused', False, FOREGROUND_COL), (mods.position(SCR_WIDTH, 'center', 'Game Paused', 57//2.2), 40))
                screen.blit(font3.render('', False, FOREGROUND_COL), (0, 0))
                screen.blit(pause_texts['Options'], pause_text_rects['Options'])
                screen.blit(pause_texts['Help'], pause_text_rects['Help'])
                screen.blit(pause_texts['Restart'], pause_text_rects['Restart'])
                screen.blit(pause_texts['Resume'], pause_text_rects['Resume'])
                screen.blit(pause_texts['Exit'], pause_text_rects['Exit'])
                if help_scr:
                    if keys[pygame.K_UP]:
                        scr_focus -= 3
                    if keys[pygame.K_DOWN]:
                        scr_focus += 3
                    
                    screen.fill(BACKGROUND_COL)
                    y_val = 70
                    vals, surf, one_line = mods.multiline_write(HELP_INFO, 85, font3)
                    
                    screen.blit(font1.render('IFEs Pong', False, FOREGROUND_COL), pygame.Rect(mods.position(SCR_WIDTH, 'center', 'IFEs Pong', FN1_SIZE), -50+mods.clamp(y_val-scr_focus, y_val, -(FN3_SIZE+TXT_PAD)), 0, 0))
                    scr_focus = mods.clamp(scr_focus,((len(HELP_INFO.split('\n')) * FN3_SIZE)+y_val)*2, 0)
                    if not one_line:
                        for k, v in enumerate(surf):
                            x = mods.position(SCR_WIDTH, 'center', vals[k], FN3_SIZE)
                            y = mods.clamp(y_val-scr_focus, y_val, -(FN3_SIZE+TXT_PAD))
                            screen.blit(v, pygame.Rect(x, y, 0, 0))
                            if v.get_colorkey() != (0, 0, 0, 255):
                                txt_size = v.get_rect().size
                                link_rect = pygame.Rect(x, y, txt_size[0], txt_size[1])
                                if mouse_rect.colliderect(link_rect):
                                    pygame.draw.line(screen, LINK_COL, (x, y + FN3_SIZE*2.5), (x + txt_size[0], y + FN3_SIZE*2.5), 2)
                                    if mouse_pressed:
                                        link = vals[k].replace('!', '')
                                        link_starter = thread.Thread(target=mods.link_opener, args=(LINKS.get(link),))
                                        link_starter.start()
                                        mouse_pressed = False

                            y_val += FN3_SIZE+TXT_PAD
                    else:
                        screen.blit(surf, pygame.Rect(mods.position(SCR_WIDTH, 'center', vals, FN3_SIZE), y_val, 0, 0))
                elif options:
                    screen.fill(BACKGROUND_COL)
                    screen.blit(font4.render('To be updated', False, FOREGROUND_COL), (mods.position(SCR_WIDTH//2, 'center', ' ',temp1_size)-55, mods.position(SCR_HEIGHT//2, 'center', ' ',temp1_size)))
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(BACKGROUND_COL)
            temp1_size = -10
            temp2_size = -50
            font4 = pygame.font.Font('assets/fonts/font(1).ttf',100)
            screen.blit(font4.render('IFES PONG', False, FOREGROUND_COL), (mods.position(SCR_WIDTH//2, 'center', 'IFES PONG',temp1_size), mods.position(SCR_HEIGHT//2, 'center', ' ',temp1_size)))
            screen.blit(font3.render(f'Starting in {round((start_timer+delay_time) - cur_time)+1}', False, FOREGROUND_COL), (mods.position(SCR_WIDTH//2, 'center', 'IFES PONG',temp2_size)+40, mods.position(SCR_HEIGHT//2, 'center', ' ',temp2_size)+mods.position(SCR_HEIGHT//2, 'center', ' ',temp1_size)))
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



