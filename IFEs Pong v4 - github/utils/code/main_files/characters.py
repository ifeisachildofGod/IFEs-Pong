
import pygame
from utils.code.constants.game_constants import (
                            AI_RESPONSE_OFFSET, PLAYER_SPEED, SCR_WIDTH,
                            SCR_HEIGHT, HIT_OFFSET, PLAYER_SIZE,
                            SETTINGS_DIR, BALL_SPEED, MAX_TIMER,
                            BALL_SIZE
                            )
from utils.code.etc import mods
import random
import json
import math

with open(SETTINGS_DIR) as file:
    saved_color = json.loads(file.read())

    fg_color = saved_color['fg_color']


class Player:
    def __init__(self, screen: pygame.Surface, mid_point, pos_x, pos_y = (SCR_HEIGHT // 2) - (PLAYER_SIZE[1] / 2)) -> None:
        width, height = PLAYER_SIZE
        
        self.accel = .1
        self.go_up = 0
        self.go_down = 0
        self.speed_multiplier = 1
        self.player_rect = pygame.Rect(pos_x, pos_y, width, height)
        self.player_pos = 0.0
        self.speed = PLAYER_SPEED
        self.scr_height = SCR_HEIGHT
        self.player_ai = False
        self.offset = AI_RESPONSE_OFFSET
        self.mid_point = mid_point
        self.screen = screen
        self.skin_loaded = False
    
    def _move(self, down, up, start_when):
            if start_when:
                if down:
                    self.go_down += self.accel
                else:
                    self.go_down = 0
                if up:
                    self.go_up += self.accel
                else:
                    self.go_up = 0
            else:
                self.go_up = 0
                self.go_down = 0
        
    def _ai(self, ball_things: list[pygame.Rect, int], left: bool, ai_difficulty: str):
        ball_rect, ball_pos = ball_things
        start_to_move = ball_pos > 0 if not left else ball_pos < 0
        match ai_difficulty:
            case 'Normal':
                new_offset = -200
                self.speed_multiplier = 1.5
                active = ball_rect.x > self.mid_point+(self.offset-new_offset) if not left else ball_rect.x < self.mid_point-(self.offset-new_offset)
                self._move(ball_rect.y >= self.player_rect.bottom-HIT_OFFSET, ball_rect.y <= self.player_rect.bottom-HIT_OFFSET, active and start_to_move)
            case 'Medium':
                new_offset = -100
                self.speed_multiplier = 1.1
                active = ball_rect.x > self.mid_point+(self.offset-new_offset) if not left else ball_rect.x < self.mid_point-(self.offset-new_offset)
                self._move(ball_rect.y >= self.player_rect.bottom-HIT_OFFSET, ball_rect.y <= self.player_rect.bottom-HIT_OFFSET, active and start_to_move)
            case 'Easy':
                new_offset = -250
                active = ball_rect.x > self.mid_point+(self.offset-new_offset) if not left else ball_rect.x < self.mid_point-(self.offset-new_offset)
                self._move(ball_rect.y >= self.player_rect.bottom-HIT_OFFSET, ball_rect.y <= self.player_rect.bottom-HIT_OFFSET, active and start_to_move)
            case 'Very Hard':
                new_offset = 10
                self.speed_multiplier = 2
                active = ball_rect.x > self.mid_point+(self.offset-new_offset) if not left else ball_rect.x < self.mid_point-(self.offset-new_offset)
                self._move(ball_rect.y >= self.player_rect.bottom-HIT_OFFSET, ball_rect.y <= self.player_rect.bottom-HIT_OFFSET, active and start_to_move)
            case 'Hard':
                new_offset = -50
                self.speed_multiplier = 2.9
                active = ball_rect.x > self.mid_point+(self.offset-new_offset) if not left else ball_rect.x < self.mid_point-(self.offset-new_offset)
                extra = math.fabs(ball_rect.y - self.player_rect.y) > 10
                self._move(ball_rect.y >= self.player_rect.bottom-HIT_OFFSET and extra, ball_rect.y <= self.player_rect.bottom-HIT_OFFSET and extra, active and start_to_move)
    
    def _mouse(self, mouse, left):
        m_x, m_y = mouse
        self.speed_multiplier = 1
        
        if left:
            if m_x < (SCR_WIDTH / 2):
                start_mouse_listen = True
            else:
                start_mouse_listen = False
        else:
            if m_x > (SCR_WIDTH / 2):
                start_mouse_listen = True
            else:
                start_mouse_listen = False
        
        self._move(m_y > self.player_rect.centery, m_y < self.player_rect.centery, start_mouse_listen)
    
    def _keys(self, up, down):
        keys = pygame.key.get_pressed()
        self.speed_multiplier = 1
        
        self._move(keys[down] if not isinstance(down, bool) else down, keys[up] if not isinstance(up, bool) else up, True)

    def player_input(self, control: str, ball_things: list[pygame.Rect, int], left: bool, ai_difficulty: str, up: int, down: int, mouse):
        match control:
            case 'KEYS':
                self._keys(up, down)
            case 'AI':
                self._ai(ball_things, left, ai_difficulty)
            case 'MOUSE':
                self._mouse(mouse, left)
    
    def movement(self, speed):
        self.go_up = mods.clamp(self.go_up, 1, 0)
        self.go_down = mods.clamp(self.go_down, 1, 0)
        self.player_pos = self.go_down - self.go_up
        
        self.player_rect.y += self.player_pos*(speed * self.speed_multiplier)
        self.player_rect.y = mods.clamp(self.player_rect.y, self.scr_height-self.player_rect.height, 0)
    
    def get_rect_vals(self):
        return self.player_rect, self.player_pos
    
    def draw(self, col=fg_color, skin = None):
        if skin == 'none':
            pygame.draw.rect(self.screen, col, self.player_rect)
        else:
            if not self.skin_loaded:
                self.skin_surf = pygame.image.load(skin).convert_alpha()
                self.skin_loaded = True

            self.skin_surf = pygame.transform.scale(self.skin_surf, (self.player_rect.width, self.player_rect.height))
            self.screen.blit(self.skin_surf, self.player_rect)

    def update(self, control: str, ball_things: list[pygame.Rect, int], left: bool, mouse_pos: tuple | list, speed, up: int, down: int, ai_difficulty: str, col=fg_color, skin = None):
        self.player_input(control, ball_things, left, ai_difficulty, up, down, mouse_pos)
        self.movement(speed)
        self.draw(col, skin)

class Ball:
    def __init__(self, x, y, x_pos, y_pos, screen: pygame.Surface, orig_score1: int = 0, orig_score2: int = 0) -> None:
        self.scr_height = SCR_HEIGHT
        self.scr_width = SCR_WIDTH
        self.start_collision_check = True
        self.timer2 = 0
        self.max_mult_val = 1.7
        self.ball_rect = pygame.Rect(x, y, BALL_SIZE, BALL_SIZE)
        self.speed_multiplier = 1
        self.score1 = orig_score1
        self.score2 = orig_score2
        self.scored = False 
        self.timer = 0
        self.ball_x_pos = x_pos + .2
        self.ball_y_pos = y_pos
        self.screen = screen
        self.sfx_volume = (self.speed_multiplier/self.max_mult_val)
        self.hit_bounce = pygame.mixer.Sound('utils/sounds/player_hit.mp3')
        self.wall_bounce = pygame.mixer.Sound('utils/sounds/wall_hit.mp3')
        self._has_imported = False
        self.skin_loaded  = False
    
    def scoring(self):
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
    
    def _respawn_ball(self):
        self.timer += 1
        self.speed_multiplier = 1
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

    def vert_col(self, collide_rect: list[pygame.Rect, int]):
        player_rect, player_pos = collide_rect
        if self.ball_rect.colliderect(player_rect):
            if player_rect.top < self.ball_rect.top < player_rect.bottom:
                if player_pos != 0:
                    self.ball_y_pos = player_pos
            else:
                if player_rect.top > self.ball_rect.top:
                    self.ball_y_pos = -1
                else:
                    self.ball_y_pos = 1
            
            if player_rect.left < self.ball_rect.centerx < player_rect.right:
                if player_rect.top > self.ball_rect.top:
                    self.ball_y_pos = -1
                else:
                    self.ball_y_pos = 1

    def horiz_col(self, collide_rect: list[pygame.Rect, int]):
        player_rect, player_pos = collide_rect
        if self.ball_rect.colliderect(player_rect):
            if player_rect.left < self.ball_rect.centerx < player_rect.right:
                if self.ball_rect.centerx > self.scr_width/2:
                    self.ball_x_pos = -1.2
                    self.ball_rect.x -= 10
                    self.ball_rect.x -= player_pos
                else:
                    self.ball_x_pos = 1.2
                    self.ball_rect.x += 10
                    self.ball_rect.x += player_pos
            self.speed_multiplier += .01
            self.speed_multiplier = mods.clamp(self.speed_multiplier, self.max_mult_val, 1)
                    
    def wall_collision(self):
        if self.ball_rect.bottom >= self.scr_height or self.ball_rect.top <= 0:
            self.ball_rect.y += -5 if self.ball_rect.bottom >= self.scr_height else 5
            self.ball_y_pos *= -1
            self.wall_bounce.play()
    
    def collision(self, collide_rects: list[pygame.Rect] | None, speed):
        self.movement(speed)
        
        self.wall_collision()
        self.scoring()
        
        if (self.ball_rect.x >= self.scr_width+self.ball_rect.width) or (self.ball_rect.x <= -(self.ball_rect.width)):
            self._respawn_ball()
        
        if collide_rects is not None:
            for collide_rect in collide_rects:
                player_rect, _ = collide_rect
                if self.ball_rect.colliderect(player_rect):
                    self.vert_col(collide_rect)
                    self.horiz_col(collide_rect)
            
                    if self.start_collision_check:
                        self.hit_bounce.play()
                        self.start_collision_check = False

                if not self.start_collision_check:
                    self.timer2 += 1
                    if self.timer2 >= 30:
                        self.start_collision_check = True
                        self.timer2 = 0
        
    def get_rect(self):
        return self.ball_rect

    def get_score(self):
        return self.score1, self.score2
    
    def movement(self, speed):
        self.ball_rect.x += self.ball_x_pos*(speed * self.speed_multiplier)
        self.ball_rect.y += self.ball_y_pos*(speed * self.speed_multiplier)
    
    def draw(self, col=fg_color, skin=None):
        if skin == 'none':
            pygame.draw.ellipse(self.screen, col, self.ball_rect)
        else:
            if not self.skin_loaded:
                self.skin_surf = pygame.image.load(skin).convert_alpha()
                self.skin_loaded = True
            
            self.skin_surf = pygame.transform.scale(self.skin_surf, (self.ball_rect.width, self.ball_rect.height))
            self.blit_surf = pygame.transform.scale(self.skin_surf, (self.ball_rect.width, self.ball_rect.height))
            self.screen.blit(self.skin_surf, self.ball_rect)

    def update(self, speed, *collide_rect: pygame.Rect, col=fg_color, skin=None):
        self.collision(collide_rect, speed)
        self.draw(col, skin)



