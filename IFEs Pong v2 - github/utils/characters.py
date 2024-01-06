import pygame
from utils.constants import (
                            AI_RESPONSE_OFFSET, BALL_SPEED, MAX_TIMER,
                            PLAYER_SPEED, SCR_WIDTH, SCR_HEIGHT,
                            HIT_OFFSET, PLAYER_SIZE
                            )
import utils.mods as mods
import random
import json

with open('utils/settings.json') as file:
    saved_color = json.loads(file.read())

    fg_color = saved_color['fg_color']

# Characters
class Player:
    width, height = PLAYER_SIZE

    def __init__(self, screen: pygame.Surface, mid_point, pos_x, pos_y = SCR_HEIGHT // 2, player_width=width, player_height=height) -> None:
        self.player_rect = pygame.Rect(pos_x, pos_y,player_width,player_height)
        self.player_pos = 0
        self.speed = PLAYER_SPEED
        self.scr_height = SCR_HEIGHT
        self.player_ai = False
        self.offset = AI_RESPONSE_OFFSET
        self.mid_point = mid_point
        self.screen = screen
        self.skin_loaded = False

    def _enemy_ai(self, ball_things: list[pygame.Rect, int], left: bool, ai_difficulty: str):
        start_to_move = ball_things[1] > 0 if not left else ball_things[1] < 0
        if ai_difficulty == 'Normal':
            something = 0
            active = ball_things[0].x > self.mid_point+self.offset-something if not left else ball_things[0].x < self.mid_point-self.offset-something
            if active and start_to_move:
                if ball_things[0].y >= self.player_rect.bottom-HIT_OFFSET: self.player_pos = 1
                elif ball_things[0].y <= self.player_rect.top+HIT_OFFSET: self.player_pos = -1
                else: self.player_pos = 0
            else:
                self.player_pos = 0
        elif ai_difficulty == 'Medium':
            something = -200
            active = ball_things[0].x > self.mid_point+(self.offset-something) if not left else ball_things[0].x < self.mid_point-(self.offset-something)
            if active and start_to_move:
                if ball_things[0].y >= self.player_rect.bottom-HIT_OFFSET: self.player_pos = 1
                elif ball_things[0].y <= self.player_rect.top+HIT_OFFSET: self.player_pos = -1
                else: self.player_pos = 0
            else:
                self.player_pos = 0
        elif ai_difficulty == 'Easy':
            something = -300
            active = ball_things[0].x > self.mid_point+(self.offset-something) if not left else ball_things[0].x < self.mid_point-(self.offset-something)
            if active and start_to_move:
                if ball_things[0].y >= self.player_rect.bottom-HIT_OFFSET: self.player_pos = 1
                elif ball_things[0].y <= self.player_rect.top+HIT_OFFSET: self.player_pos = -1
                else: self.player_pos = 0
            else:
                self.player_pos = 0
        elif ai_difficulty == 'Hard':
            something = self.offset
            active = ball_things[0].x > self.mid_point+(self.offset-something) if not left else ball_things[0].x < self.mid_point-(self.offset-something)
            
            if active and start_to_move:
                if ball_things[0].y >= self.player_rect.bottom-HIT_OFFSET: self.player_pos = 1
                elif ball_things[0].y <= self.player_rect.top+HIT_OFFSET: self.player_pos = -1
                else: self.player_pos = 0
            else:
                self.player_pos = 0
        elif ai_difficulty == 'Impossible':
            something = self.offset + 100
            active = ball_things[0].x > self.mid_point+(self.offset-something) if not left else ball_things[0].x < self.mid_point-(self.offset-something)
            if active and start_to_move:
                if ball_things[0].y >= self.player_rect.bottom-HIT_OFFSET: self.player_pos = 1.2
                elif ball_things[0].y <= self.player_rect.top+HIT_OFFSET: self.player_pos = -1.2
                else: self.player_pos = 0
            else:
                self.player_pos = 0
    
    def player_input(self, control: str, ball_things: list[pygame.Rect, int], left: bool, ai_difficulty: str, up: int, down: int):
        keys = pygame.key.get_pressed()
        if control == 'KEYS':
                if keys[up]:go_up = 1
                else:go_up = 0
                if keys[down]:go_down = 1
                else:go_down = 0
                self.player_pos = go_down - go_up
        elif control == 'AI':
            self._enemy_ai(ball_things, left, ai_difficulty)

    def movement(self, speed):
        self.player_rect.y += (self.player_pos*speed)
        self.player_rect.y = mods.clamp(self.player_rect.y, self.scr_height-self.player_rect.height, 0)
    
    def get_rect_vals(self):
        return self.player_rect, self.player_pos
    
    def update(self, control: str, ball_things: list[pygame.Rect, int], left: bool, speed, up: int, down: int, ai_difficulty: str, col=fg_color, skin = None):
        self.player_input(control, ball_things, left, ai_difficulty, up, down)
        self.movement(speed)
        if skin == 'none':
            pygame.draw.rect(self.screen, col, self.player_rect)
        else:
            if not self.skin_loaded:
                self.skin_surf = pygame.image.load(skin)
                self.skin_loaded = True

            self.skin_surf = pygame.transform.scale(self.skin_surf, (self.player_rect.width, self.player_rect.height))
            self.screen.blit(self.skin_surf, self.player_rect)

class Ball:
    def __init__(self, screen: pygame.Surface) -> None:
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
        self.screen = screen
        
    def collision(self, collide_rects):
        wall_hit = pygame.mixer.Sound(r'utils\sounds\wall_bounce.mp3')
        hit_bounce = pygame.mixer.Sound(r'utils\sounds\\player_bounce.mp3')
        wall_hit.set_volume(.5)
        if self.ball_rect.y >= self.scr_height-self.ball_rect.height:
            self.ball_y_pos = -1
            wall_hit.play()
        elif self.ball_rect.y <= 0:
            self.ball_y_pos = 1
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
                player_rect, player_pos = collide_rect
                if self.ball_rect.colliderect(player_rect):
                    if self.ball_x_pos < 0:self.ball_rect.x += 5
                    elif self.ball_x_pos > 0:self.ball_rect.x -= 5
                    self.ball_x_pos *= -1
                    if (self.ball_rect.top - player_rect.top) > (player_rect.height // 2):self.ball_y_pos = 1
                    else:self.ball_y_pos *= -(random.choice([.2, .3, .4, .5, .6, .7, .8, .9, 1]))
                    
                    if (player_pos == -1 and self.ball_y_pos == 1) or (player_pos == 1 and self.ball_y_pos == -1):
                        self.ball_y_pos = player_pos
                    
                    hit_bounce.play()

    def get_rect(self):
        return self.ball_rect

    def get_score(self):
        return self.score1, self.score2
    
    def movement(self, speed):
        self.ball_rect.x += self.ball_x_pos*speed
        self.ball_rect.y += self.ball_y_pos*speed

    def update(self, speed, *collide_rect: pygame.Rect, col=fg_color):
        self.collision(collide_rect)
        self.movement(speed)
        pygame.draw.ellipse(self.screen, col, self.ball_rect)



