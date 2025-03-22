
import math
import pygame
import random

class Player:
    def __init__(self, screen: pygame.Surface, pos: list|tuple, size: list|tuple, is_player_left: bool) -> None:
        self.screen = screen
        self.rect = pygame.Rect(pos[0] - (size[0] / 2), pos[1] - (size[1] / 2), *size)
        self.accel = .1
        self.go_up = 0
        self.go_down = 0
        self.x_speed_multiplier = 1
        self.y_dir = 0
        self.mid_point = self.screen.get_width() / 2
        self.is_player_left = is_player_left
        
        self.ai_response_time_offset = 100
        self.ai_response_start_offset = 30
        
        self.color = None
    
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
                self.x_speed_multiplier = 1.5
                active = ball_rect.centerx > self.mid_point + (self.ai_response_time_offset-new_offset) if not self.is_player_left else ball_rect.centerx < self.mid_point - (self.ai_response_time_offset-new_offset)
                self._move(ball_rect.y >= self.rect.bottom - self.ai_response_start_offset, ball_rect.y <= self.rect.bottom - self.ai_response_start_offset, active and start_to_move)
            case 'Medium':
                new_offset = -100
                self.x_speed_multiplier = 1.1
                active = ball_rect.centerx > self.mid_point + (self.ai_response_time_offset-new_offset) if not self.is_player_left else ball_rect.centerx < self.mid_point - (self.ai_response_time_offset-new_offset)
                self._move(ball_rect.y >= self.rect.bottom - self.ai_response_start_offset, ball_rect.y <= self.rect.bottom - self.ai_response_start_offset, active and start_to_move)
            case 'Easy':
                new_offset = -250
                active = ball_rect.centerx > self.mid_point + (self.ai_response_time_offset-new_offset) if not self.is_player_left else ball_rect.centerx < self.mid_point - (self.ai_response_time_offset-new_offset)
                self._move(ball_rect.y >= self.rect.bottom - self.ai_response_start_offset, ball_rect.y <= self.rect.bottom - self.ai_response_start_offset, active and start_to_move)
            case 'Very Hard':
                new_offset = 10
                self.x_speed_multiplier = 2
                active = ball_rect.centerx > self.mid_point + (self.ai_response_time_offset-new_offset) if not self.is_player_left else ball_rect.centerx < self.mid_point - (self.ai_response_time_offset-new_offset)
                self._move(ball_rect.y >= self.rect.bottom - self.ai_response_start_offset, ball_rect.y <= self.rect.bottom - self.ai_response_start_offset, active and start_to_move)
            case 'Hard':
                new_offset = -50
                self.x_speed_multiplier = 2.9
                active = ball_rect.centerx > self.mid_point + (self.ai_response_time_offset-new_offset) if not self.is_player_left else ball_rect.centerx < self.mid_point - (self.ai_response_time_offset-new_offset)
                extra = math.fabs(ball_rect.y - self.rect.y) > 10
                self._move(ball_rect.y >= self.rect.bottom - self.ai_response_start_offset and extra, ball_rect.y <= self.rect.bottom - self.ai_response_start_offset and extra, active and start_to_move)
    
    def _mouse(self, mouse_pos):
        self.x_speed_multiplier = 1

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
    
    def _keys(self, keys_to_go_up_or_down: tuple[tuple[str, int | bool], tuple[str, int | bool]]):
        self.x_speed_multiplier = 1

        keys = pygame.key.get_pressed()
        (_, up), (_, down) = keys_to_go_up_or_down
        
        self._move(keys[down] if not isinstance(down, bool) else down, keys[up] if not isinstance(up, bool) else up, True)

    def _player_input(self, control: str, ball_info: list|tuple[pygame.Rect, list|tuple], ai_difficulty: str, keys_to_go_up_or_down: tuple[tuple[str, int | bool], tuple[str, int | bool]], mouse_pos):
        match control.lower():
            case 'keyboard':
                self._keys(keys_to_go_up_or_down)
            case 'ai':
                self._ai(ball_info, ai_difficulty)
            case 'mouse':
                self._mouse(mouse_pos)
            case _:
                raise KeyError(f"Control type: {control} not recognized")
    
    def _update_movement(self, speed):
        self.go_up = pygame.math.clamp(self.go_up, 0, 1)
        self.go_down = pygame.math.clamp(self.go_down, 0, 1)
        self.y_dir = self.go_down - self.go_up
        
        self.rect.y += (speed * self.x_speed_multiplier) * self.y_dir
        self.rect.y = int(pygame.math.clamp(self.rect.y, 0, self.screen.get_height() - self.rect.height))
    
    def draw(self):
        if self.color is not None:
            pygame.draw.rect(self.screen, self.color, self.rect)
    
    def get_rect_info(self):
        return self.rect, self.y_dir
    
    def update(self, control: str, ball_info: list|tuple[pygame.Rect, list|tuple], mouse_pos: list|tuple, speed, keys_to_go_up_or_down: tuple[tuple[str, int | bool], tuple[str, int | bool]], ai_difficulty: str, color):
        self._player_input(control, ball_info, ai_difficulty, keys_to_go_up_or_down, mouse_pos)
        self._update_movement(speed)
        self.color = color

class Ball:
    def __init__(self, screen: pygame.Surface, pos: tuple[float, float], radius: float, direction: tuple[float, float], scores: tuple[float, float] = (0, 0)) -> None:
        self.screen = screen
        self.rect = pygame.Rect(pos[0] - (radius / 2), pos[1] - (radius / 2), radius, radius)
        self.p1_score, self.p2_score = scores
        self.x_dir, self.y_dir = direction
        self.terminal_speed = 0.7
        self.collission_timer = 0
        self.respawn_timer = 0
        self.hit_bounce = pygame.mixer.Sound('src/audio/player_hit.mp3')
        self.wall_bounce = pygame.mixer.Sound('src/audio/wall_hit.mp3')
        self.scored = False
        self.start_collision_check = True
        self.respawn_time = 100
        self.speed = 0.4
        
        self.color = None
        
        self.future_x = 0
        self.future_y = 0
        
        self.player1_y_prev = 0
        self.player2_y_prev = 0
        self.player1_y_curr = 0
        self.player2_y_curr = 0
    
    def _update_scoring(self):
        p1_scored = self.rect.centerx < self.screen.get_width() / 2
        
        if self.scored:
            if p1_scored:
                self.p1_score += 1
            else:
                self.p2_score += 1
            self.scored = False
    
    def _respawn_ball(self):
        self.speed = 0.4
        
        self.respawn_timer += 1
        if self.respawn_timer >= self.respawn_time:
            self.x_dir = 1 if self.rect.centerx < self.screen.get_width() / 2 else -1
            self.y_dir = random.choice([-1, 1])
            self.rect.centerx = self.screen.get_width() // 2
            self.rect.centery = self.screen.get_height() // 2
            self.respawn_timer = 0
        else:
            self.rect.centery = self.screen.get_height() // 2
            self.x_dir = 0
            self.y_dir = 0
    
    def _vertical_collission(self, collide_rect_info: tuple[pygame.Rect, int | float]):
        player_rect, player_pos = collide_rect_info
        if self.rect.colliderect(player_rect):
            if player_rect.top < self.rect.centery < player_rect.bottom:
                player_dir = (self.player1_y_vel if self.rect.centerx < self.screen.get_width() / 2 else self.player2_y_vel) / 100
                self.y_dir += player_pos + player_dir
                # if player_pos != 0:
                # self.y_speed_multiplier += math.fabs(self.player1_y_vel if self.rect.centerx < self.screen.get_width() / 2 else self.player2_y_vel) / 10
            else:
                self.y_dir -1 if player_rect.centery > self.rect.top else 1
            
            if player_rect.left < self.rect.centerx < player_rect.right:
                self.y_dir -1 if player_rect.centery > self.rect.top else 1
    
    def _horizontal_collision(self, collide_rect_info: tuple[pygame.Rect, int | float]):
        player_rect, player_pos = collide_rect_info
        if self.rect.colliderect(player_rect):
            if player_rect.left < self.rect.centerx < player_rect.right:
                if self.rect.centerx > self.screen.get_width() / 2:
                    self.x_dir = -1
                    self.rect.x -= 10
                    # self.rect.x -= player_pos # type: ignore
                else:
                    self.x_dir = 1
                    self.rect.x += 10
                    # self.rect.x += player_pos # type: ignore
            self.speed += .1
            self.speed = pygame.math.clamp(self.speed, 1, self.terminal_speed)
    
    def _update_wall_collision(self):
        if self.rect.bottom >= self.screen.get_height() or self.rect.top <= 0:
            self.rect.y += -5 if self.rect.bottom >= self.screen.get_height() else 5
            self.y_dir *= -1
            self.wall_bounce.play()
    
    def _update_collision(self, collide_rects_info: tuple[tuple[pygame.Rect, int | float], tuple[pygame.Rect, int | float]] | None):
        if (self.rect.centerx >= self.screen.get_width() + (self.rect.width / 2)) or (self.rect.centerx <= -(self.rect.width / 2)):
            if self.x_dir != 0 and self.y_dir != 0:
                self.scored = True
            self._respawn_ball()
        
        if collide_rects_info is not None:
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
        
    def _update_movement(self):
        x_vel = (self.speed * self.delta_time) * self.x_dir
        y_vel = (self.speed * self.delta_time) * self.y_dir
        
        self.rect.x += x_vel # type: ignore
        self.rect.y += y_vel # type: ignore
    
    def _get_ball_future_pos(self, x_dir: float, y_dir: float):
        x_vel = (self.speed * self.delta_time) * x_dir
        y_vel = (self.speed * self.delta_time) * y_dir
        
        x_sign = x_vel / (math.fabs(x_vel) if x_vel else 1)
        y_sign = y_vel / (math.fabs(y_vel) if y_vel else 1)
        
        x_ref_pos = self.screen.get_width() * (x_sign + 1) / 2
        y_ref_pos = self.screen.get_height() * (y_sign + 1) / 2
        
        theta = (math.degrees(math.atan2(y_vel, x_vel))) % 360
        
        x_wall_dist = math.fabs(self.rect.centerx - x_ref_pos)
        y_wall_dist = math.fabs(self.rect.centery - y_ref_pos)
        
        opposite = math.fabs(y_wall_dist * (math.tan(math.radians(theta)) if math.tan(math.radians(theta)) else 1))
        hypotenuse = math.fabs(y_wall_dist / (math.sin(math.radians(theta)) if math.sin(math.radians(theta)) else 1))
        
        print(x_wall_dist, opposite)
        
        return self.rect.centerx + (opposite * math.cos(math.radians(theta))), self.rect.centery + (hypotenuse * math.sin(math.radians(theta)))
    
    def draw(self):
        if self.color is not None:
            pygame.draw.ellipse(self.screen, self.color, self.rect)
        
        future_ball_positions = []
        
        for i in range(0, 1000):
            latest_pos = self._get_ball_future_pos(self.x_dir, self.y_dir)
            future_ball_positions.append(latest_pos)
            if not (self.player1_rect.right + (self.rect.width / 2) <= future_ball_positions[-1][0] <= self.player2_rect.left - (self.rect.width / 2)):
                # print(future_ball_positions[-1][0])
                break
        
        for index, positions in enumerate(future_ball_positions):
            start_pos = future_ball_positions[index - 1] if index else self.rect.center
            pygame.draw.line(self.screen, "white", start_pos, positions)
    
    def get_rect_info(self):
        return self.rect, (self.x_dir, self.y_dir)
    
    def get_score(self):
        return self.p1_score, self.p2_score
    
    def update(self, delta_time: float, collide_rect_info: tuple[tuple[pygame.Rect, int | float], tuple[pygame.Rect, int | float]], color):
        (self.player1_rect, _), (self.player2_rect, _) = collide_rect_info
        
        self.delta_time = delta_time
        
        self.player1_y_prev = self.player1_rect.y
        self.player2_y_prev = self.player2_rect.y
        
        self._update_movement()
        self._update_wall_collision()
        self._update_scoring()
        self._update_collision(collide_rect_info)
        self.color = color
        
        self.player1_y_vel = self.player1_y_curr - self.player1_y_prev
        self.player2_y_vel = self.player2_y_curr - self.player2_y_prev
        
        self.player1_y_curr = self.player1_rect.y
        self.player2_y_curr = self.player2_rect.y



