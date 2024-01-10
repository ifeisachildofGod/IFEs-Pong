
import pygame
from utils.game.game_constants import AI_RESPONSE_OFFSET, HIT_OFFSET, MAX_TIMER
import random
import math

class Player:
    def __init__(self, screen: pygame.Surface, pos: list|tuple, size: list|tuple, is_player_left: bool) -> None:
        self.screen = screen
        self.rect = pygame.Rect(pos[0] - (size[0] / 2), pos[1] - (size[1] / 2), *size)
        self.accel = .1
        self.go_up = 0
        self.go_down = 0
        self.speed_multiplier = 1
        self.y_dir = 0
        self.mid_point = self.screen.get_width() / 2
        self.is_player_left = is_player_left
    
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
    
    def _ai(self, ball_info: list|tuple[pygame.Rect, list|tuple], ai_difficulty: str):
        ball_rect, ball_pos = ball_info
        ball_x_dir, _ = ball_pos
        start_to_move = ball_x_dir > 0 if not self.is_player_left else ball_x_dir < 0
        match ai_difficulty:
            case 'Normal':
                new_offset = -200
                self.speed_multiplier = 1.5
                active = ball_rect.centerx > self.mid_point + (AI_RESPONSE_OFFSET-new_offset) if not self.is_player_left else ball_rect.centerx < self.mid_point - (AI_RESPONSE_OFFSET-new_offset)
                self._move(ball_rect.y >= self.rect.bottom - HIT_OFFSET, ball_rect.y <= self.rect.bottom - HIT_OFFSET, active and start_to_move)
            case 'Medium':
                new_offset = -100
                self.speed_multiplier = 1.1
                active = ball_rect.centerx > self.mid_point + (AI_RESPONSE_OFFSET-new_offset) if not self.is_player_left else ball_rect.centerx < self.mid_point - (AI_RESPONSE_OFFSET-new_offset)
                self._move(ball_rect.y >= self.rect.bottom - HIT_OFFSET, ball_rect.y <= self.rect.bottom - HIT_OFFSET, active and start_to_move)
            case 'Easy':
                new_offset = -250
                active = ball_rect.centerx > self.mid_point + (AI_RESPONSE_OFFSET-new_offset) if not self.is_player_left else ball_rect.centerx < self.mid_point - (AI_RESPONSE_OFFSET-new_offset)
                self._move(ball_rect.y >= self.rect.bottom - HIT_OFFSET, ball_rect.y <= self.rect.bottom - HIT_OFFSET, active and start_to_move)
            case 'Very Hard':
                new_offset = 10
                self.speed_multiplier = 2
                active = ball_rect.centerx > self.mid_point + (AI_RESPONSE_OFFSET-new_offset) if not self.is_player_left else ball_rect.centerx < self.mid_point - (AI_RESPONSE_OFFSET-new_offset)
                self._move(ball_rect.y >= self.rect.bottom - HIT_OFFSET, ball_rect.y <= self.rect.bottom - HIT_OFFSET, active and start_to_move)
            case 'Hard':
                new_offset = -50
                self.speed_multiplier = 2.9
                active = ball_rect.centerx > self.mid_point + (AI_RESPONSE_OFFSET-new_offset) if not self.is_player_left else ball_rect.centerx < self.mid_point - (AI_RESPONSE_OFFSET-new_offset)
                extra = math.fabs(ball_rect.y - self.rect.y) > 10
                self._move(ball_rect.y >= self.rect.bottom - HIT_OFFSET and extra, ball_rect.y <= self.rect.bottom - HIT_OFFSET and extra, active and start_to_move)
    
    def _mouse(self, mouse_pos):
        self.speed_multiplier = 1

        m_x, m_y = mouse_pos
        
        if self.is_player_left:
            if m_x < (self.screen.get_width() / 2):
                start_mouse_listen = True
            else:
                start_mouse_listen = False
        else:
            if m_x > (self.screen.get_width() / 2):
                start_mouse_listen = True
            else:
                start_mouse_listen = False
        
        self._move(m_y > self.rect.centery, m_y < self.rect.centery, start_mouse_listen)
    
    def _keys(self, keys_to_go_up_or_down: tuple[int | bool]):
        self.speed_multiplier = 1

        keys = pygame.key.get_pressed()
        up, down = keys_to_go_up_or_down
        self._move(keys[down] if not isinstance(down, bool) else down, keys[up] if not isinstance(up, bool) else up, True)

    def _player_input(self, control: str, ball_info: list|tuple[pygame.Rect, list|tuple], ai_difficulty: str, keys_to_go_up_or_down: tuple[int | bool], mouse_pos):
        match control:
            case 'KEYS':
                self._keys(keys_to_go_up_or_down)
            case 'AI':
                self._ai(ball_info, ai_difficulty)
            case 'MOUSE':
                self._mouse(mouse_pos)
    
    def _movement(self, speed):
        self.go_up = pygame.math.clamp(self.go_up, 0, 1)
        self.go_down = pygame.math.clamp(self.go_down, 0, 1)
        self.y_dir = self.go_down - self.go_up
        
        self.rect.y += (speed * self.speed_multiplier) * self.y_dir
        self.rect.y = pygame.math.clamp(self.rect.y, 0, self.screen.get_height() - self.rect.height)
    
    def draw(self, color, skin_surf: pygame.Surface = None):
        if skin_surf is None:
            pygame.draw.rect(self.screen, color, self.rect)
        else:
            skin_surf = pygame.transform.scale(skin_surf, (self.rect.width, self.rect.height))
            self.screen.blit(skin_surf, self.rect)
    
    def get_rect_info(self):
        return self.rect, self.y_dir
    
    def update(self, control: str, ball_info: list|tuple[pygame.Rect, list|tuple], mouse_pos: list|tuple, speed, keys_to_go_up_or_down: tuple[int | bool], ai_difficulty: str, color, skin_surf: pygame.Surface = None):
        self._player_input(control, ball_info, ai_difficulty, keys_to_go_up_or_down, mouse_pos)
        self._movement(speed)
        self.draw(color, skin_surf)

class Ball:
    def __init__(self, screen: pygame.Surface, pos: tuple|list, radius: int, direction: list|tuple, scores: list|tuple[int] = (0, 0)) -> None:
        self.screen = screen
        self.rect = pygame.Rect(pos[0] - radius, pos[1] - radius, radius * 2, radius * 2)
        self.p1_score, self.p2_score = scores
        self.x_dir, self.y_dir = direction
        self.speed_multiplier = 1
        self.max_mult_val = 1.7
        self.collission_timer = 0
        self.respawn_timer = 0
        self.sfx_volume = self.speed_multiplier / self.max_mult_val
        self.hit_bounce = pygame.mixer.Sound('utils/sounds/player_hit.mp3')
        self.wall_bounce = pygame.mixer.Sound('utils/sounds/wall_hit.mp3')
        self.scored = False
        self.start_collision_check = True
    
    def _scoring(self):
        p1_scored = self.rect.centerx < self.screen.get_width() / 2
        
        if self.scored:
            if p1_scored:
                self.p1_score += 1
            else:
                self.p2_score += 1
            self.scored = False
    
    def _respawn_ball(self):
        self.respawn_timer += 1
        self.speed_multiplier = 1
        if self.respawn_timer >= MAX_TIMER:
            self.x_dir = 1 if self.rect.centerx < self.screen.get_width() / 2 else -1
            self.y_dir = random.choice([-1, 1])
            self.rect.centerx = self.screen.get_width() / 2
            self.rect.centery = self.screen.get_height() / 2
            self.respawn_timer = 0
        else:
            self.rect.centery = self.screen.get_height() / 2
            self.x_dir = 0
            self.y_dir = 0
    
    def _vertical_collission(self, collide_rect_info: list|tuple[pygame.Rect, int]):
        player_rect, player_pos = collide_rect_info
        if self.rect.colliderect(player_rect):
            if player_rect.top < self.rect.centery < player_rect.bottom:
                if player_pos != 0:
                    self.y_dir = player_pos
                else:
                    self.y_dir = random.uniform(-1, 1)
            else:
                self.y_dir -1 if player_rect.centery > self.rect.top else 1
            
            if player_rect.left < self.rect.centerx < player_rect.right:
                self.y_dir -1 if player_rect.centery > self.rect.top else 1
    
    def _horizontal_collision(self, collide_rect_info: list|tuple[pygame.Rect, int]):
        player_rect, player_pos = collide_rect_info
        if self.rect.colliderect(player_rect):
            if player_rect.left < self.rect.centerx < player_rect.right:
                if self.rect.centerx > self.screen.get_width() / 2:
                    self.x_dir = -1.2
                    self.rect.x -= 10
                    self.rect.x -= player_pos
                else:
                    self.x_dir = 1.2
                    self.rect.x += 10
                    self.rect.x += player_pos
            self.speed_multiplier += .01
            self.speed_multiplier = pygame.math.clamp(self.speed_multiplier, 1, self.max_mult_val)
    
    def _wall_collision(self):
        if self.rect.bottom >= self.screen.get_height() or self.rect.top <= 0:
            self.rect.y += -5 if self.rect.bottom >= self.screen.get_height() else 5
            self.y_dir *= -1
            self.wall_bounce.play()
    
    def _collision(self, collide_rects_info: list|tuple[pygame.Rect, int] | None):
        if (self.rect.centerx >= self.screen.get_width() + (self.rect.width / 2)) or (self.rect.centerx <= -(self.rect.width / 2)):
            if self.x_dir != 0 and self.y_dir != 0:
                self.scored = True
            self._respawn_ball()
        
        for collide_rect_info in collide_rects_info:
            player_rect, _ = collide_rect_info
            if self.rect.colliderect(player_rect):
                self._vertical_collission(collide_rect_info)
                self._horizontal_collision(collide_rect_info)
        
                if self.start_collision_check:
                    self.hit_bounce.play()
                    self.start_collision_check = False

            if not self.start_collision_check:
                self.collission_timer += 1
                if self.collission_timer >= 30:
                    self.start_collision_check = True
                    self.collission_timer = 0
    
    def _movement(self, speed):
        self.rect.x += (speed * self.speed_multiplier) * self.x_dir
        self.rect.y += (speed * self.speed_multiplier) * self.y_dir
    
    def draw(self, color, skin_surf: pygame.Surface = None):
        if skin_surf is None:
            pygame.draw.ellipse(self.screen, color, self.rect)
        else:
            skin_surf = pygame.transform.scale(skin_surf, (self.rect.width, self.rect.height))
            self.screen.blit(skin_surf, self.rect)
    
    def get_rect_info(self):
        return self.rect, (self.x_dir, self.y_dir)
    
    def get_score(self):
        return self.p1_score, self.p2_score
    
    def update(self, speed, collide_rect_info: list|tuple[pygame.Rect, int], color, skin_surf: pygame.Surface=None):
        self._movement(speed)
        self._wall_collision()
        self._scoring()
        self._collision(collide_rect_info)
        self.draw(color, skin_surf)



























# class BaseParticleEffects:
#     def __init__(self, screen: pygame.Surface, partcle_speed: int, default_particle_size: int, partcle_rad: int) -> None:
#         self.screen = screen
#         self.particles = []
#         self.partcle_speed = partcle_speed
#         self.default_particle_size = default_particle_size
#         self.partcle_rad = partcle_rad
#         self.color_func = self._spawn_particles_colors
#         self.direction_func = self._spawn_particles_direction
#         self.reason_for_not_removal = True
    
#     def _spawn_particles_direction(self):
#         return [random.uniform(-1, 1), random.uniform(-1, 1)]
    
#     def _spawn_particles_colors(self):
#         return [random.uniform(0, 1) * 255, random.uniform(0, 1) * 255, random.uniform(0, 1) * 255]
    
#     def add_particles(self):
#         direction = self.direction_func()
#         color = self.color_func()
#         rad = [self.default_particle_size, self.default_particle_size]
        
#         particle = [direction, color, list|tuple(self.start_pos), rad]
#         self.particles.append(particle)
    
#     def update_particle_physics(self, particle_info: int, delta_time: int):
#         direction, _, pos, rad = particle_info
#         rad[0] -= 1 / self.partcle_rad
#         rad[1] -= 1 / self.partcle_rad
#         pos[0] += self.partcle_speed * direction[0] * delta_time
#         pos[1] += self.partcle_speed * direction[1] * delta_time
        
#         return sum(rad) >= self.partcle_speed and (0 < pos[0] < self.screen.get_width() and 0 < pos[1] < self.screen.get_height())
    
#     def _draw(self, particle_info):
#         _, color, pos, rad = particle_info
#         pygame.draw.ellipse(self.screen, color, (pos[0] - (rad[0] / 2), pos[1] - (rad[1] / 2), *rad))
    
#     def update(self, start_pos: list|tuple, delta_time):
#         self.start_pos = start_pos
        
#         for particle_info in self.particles:
#             if self.reason_for_not_removal:
#                 self._draw(particle_info)
#                 self.reason_for_removal = self.update_particle_physics(particle_info, delta_time)
#             else:
#                 self.particles.remove(particle_info)
        
#         self.add_particles()























































# class Timer:
#     def __init__(self) -> None:
#         self.t1 = time.time()
#         self.timer = time.time()
#         self.time = round(self.t1 - self.timer)
#         self.paused = False
#         self.a = 0
#         self.minus = 0
    
#     def time_it(self):
#         self.a += 1
#         if not self.paused:
#             self.pause_timer = time.time()
#             self.time = round((time.time() - self.timer) - self.minus)
#         else:
#             self.minus = round(time.time() - self.pause_timer)
    
#     def pause(self):
#         self.paused = True
    
#     def unpause(self):
#         self.paused = False
    
#     def reset(self):
#         self.timer = time.time()






