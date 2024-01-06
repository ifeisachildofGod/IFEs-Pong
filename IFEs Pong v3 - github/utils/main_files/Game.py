
import pygame
import sys
import json
import random
from pathlib import Path
import threading as thread
from utils.main_files.characters import Ball, Player
from utils.main_files.widgets import TextView, Button, Selector, InputSeletor
import utils.code.constants.game_constants as gc
from utils.code.constants.game_constants import (
                            FONT1, FONT2, FONT3,
                            LINE_SPACE, LINE_LEN, LINKS,
                            FN2_SIZE, LINK_KEY, TXT_PAD,
                            SCR_WIDTH, SCR_HEIGHT, FN3_SIZE,
                            SETTINGS_DIR, HEADERS, STATS_DIR,
                            BALL_SPEED, EDGE_SPACE, FN1_SIZE,
                            HELP_INFO, FONT_CELL_SIZE, PLAYER_SPEED,
                            LINE_WIDTH, FOCUS_RECT_WIDTH, CONTROL_OPTIONS,
                            AI_DIFFICULTY_OPTIONS, CONTINUE_VARIABLE_DIR, FPS,
                            P1_START_POS, P2_START_POS
                            )
from utils.code.constants.ui_constants import (
                            ON_HOVER_OPAC, ON_CLICK_OPAC, ICON_SIZE,
                            SCROLL_SPEED, ICON_POS, PTR_Y_POS,
                            BORDER_RAD, BORDER_RAD2, BG_OFFSET,
                            PAUSE_TEXT_SPACING, MAX_TV_LEN, X_OPTION_TEXT_OFFSET,
                            EXIT_SPACE_OFFSET, PAUSE_TEXT_START_POS, X_PAUSE_TEXT_OFFSET,
                            OPTION_TEXT_SPACING, OPTION_TEXT_START_POS, Y_OPTION_SPACE_OFFSET,
                            )

from utils.code.etc import mods
import time

pygame.init()

class Game:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
        
        title = 'IFEs Pong'
        pygame.display.set_caption(title)
        
        logo = pygame.image.load('utils/logos/pong_logo.png')
        pygame.display.set_icon(logo)
        self.clock = pygame.time.Clock()
        
        self._load_saved_values()
        self.skin_path = [i.as_posix() for i in list(Path('SKINS').glob('*.*'))]
        self.in_next_update = False
        
        self.start_time = int(pygame.time.get_ticks() / 1000)
        self.started_timing = False
        self.other_start_time = int(pygame.time.get_ticks() / 1000)
        self.time_not_played = int(pygame.time.get_ticks() / 1000)-self.other_start_time
        self.play_timer = 0
                
        self.bg_key = 'Background Color'
        self.bg_opt_key = f'{self.bg_key} opt'
        self.fg_key = 'Foreground Color'
        self.fg_opt_key = f'{self.fg_key} opt'
        self.ai_key = 'AI Difficulty'
        self.ai_key_opt = f'{self.ai_key} opt'
        self.p1c_key = 'Player one Control'
        self.p1c_key_opt = f'{self.p1c_key} opt'
        self.p2c_key = 'Player two Control'
        self.p2c_key_opt = f'{self.p2c_key} opt'
        
        self.pob_key = 'Player one Binding a'
        self.pob_up_key_opt = 'Player one Binding opt '
        self.pob_down_key_opt = f'{self.pob_key} opt'
        
        self.ptb_key = 'Player two Binding a'
        self.ptb_up_key_opt = 'Player two Binding opt'
        self.ptb_down_key_opt = f'{self.ptb_key} opt'
        
        self.load_skin_player = False
        self.load_skin_ball = False
        self.load_skin_bg = False
        self.load_skin_ui = False

        self.ai_difficulty = AI_DIFFICULTY_OPTIONS[self.ad_index]
        
        self.ptb_focus = 1
        self.pob_focus = 1
        
        self.p1_control = CONTROL_OPTIONS[self.pc1_index]
        self.p2_control = CONTROL_OPTIONS[self.pc2_index]

        self.tv_bg_color = [self.bg_color, self.fg_color]
        self.tv_fg_color = [self.fg_color, self.bg_color]
        self.aid_color = self.fg_color
        self.p1_color = self.fg_color
        self.p2_color = self.fg_color
        self.pob_color = self.fg_color
        self.ptb_color = self.fg_color
        self.ptr_u_d_width = FN3_SIZE
        self.ptr_u_d_height = (FN3_SIZE * 1.5) - 10
        self.ptr_u_d_x = SCR_WIDTH - 25
        self.ptr_u_y = PTR_Y_POS + 5
        self.ptr_d_y = (SCR_HEIGHT - self.ptr_u_d_height - PTR_Y_POS) - 5
        self.pohs = self.stats_val['player one high score']
        self.pths = self.stats_val['player two high score']
        self.hpt = mods.secs_to_time(self.stats_val['highest play time'])
        stats_info = gc.all_stats(self.pohs, self.pths, ltsp=self.hpt)

        _, self.info_surf, _, _ = mods.multiline_write(HELP_INFO, FONT3)
        _, self.stats_surf, _, _ = mods.multiline_write(stats_info, FONT3)

        self.y_val = 70
        self.scr_wheel_y = 0
        self.info_texts_size = self.y_val
        self.stats_texts_size = self.y_val
        
        for _ in self.info_surf:
            self.info_texts_size += FN3_SIZE+TXT_PAD
        
        for _ in self.stats_surf:
            self.stats_texts_size += FN3_SIZE+TXT_PAD
        
        self.saa_size = (150, 30)
        
        self.player1 = Player(self.screen, SCR_WIDTH/2, P1_START_POS)
        self.player2 = Player(self.screen, SCR_WIDTH/2, P2_START_POS)
        self.ball = Ball(SCR_WIDTH/2, SCR_HEIGHT/2, random.choice([1, -1]), random.choice([1, -1]), self.screen)
        
        self.bg_input = TextView(self.bg_txt_view_input, self.screen, MAX_TV_LEN)
        self.fg_input = TextView(self.fg_txt_view_input, self.screen, MAX_TV_LEN)
        self.ai_difficulty_selector = Selector(self.screen, AI_DIFFICULTY_OPTIONS, self.ad_index)
        self.p1_control_selector = Selector(self.screen, CONTROL_OPTIONS, self.pc1_index)
        self.p2_control_selector = Selector(self.screen, CONTROL_OPTIONS, self.pc2_index)
        
        self.back_button = Button(self.screen, self.fg_color, BORDER_RAD2, (ICON_POS, ICON_POS), ICON_SIZE*FN3_SIZE, sound_path=('utils/sounds/ui_sfx.mp3', .3))
        self.mp_back_button = Button(self.screen, self.fg_color, BORDER_RAD2, (ICON_POS, ICON_POS), ICON_SIZE*FN3_SIZE)
        self.saa_button = Button(self.screen, self.fg_color, BORDER_RAD2, (SCR_WIDTH - self.saa_size[0] - 50, SCR_HEIGHT - self.saa_size[1] - 30), self.saa_size, 'Save and Apply', self.bg_color)
        self.pob_up_input = InputSeletor(self.player1_up_txt_view_input, self.screen, self.bg_color, self.fg_color, 'Player one binding up', r'utils\logos\pong_logo.png')
        self.pob_down_input = InputSeletor(self.player1_down_txt_view_input, self.screen, self.bg_color, self.fg_color, 'Player one binding down', r'utils\logos\pong_logo.png')
        self.ptb_up_input = InputSeletor(self.player2_up_txt_view_input, self.screen, self.bg_color, self.fg_color, 'Player two binding up', r'utils\logos\pong_logo.png')
        self.ptb_down_input = InputSeletor(self.player2_down_txt_view_input, self.screen, self.bg_color, self.fg_color, 'Player two binding down', r'utils\logos\pong_logo.png')
        self.ptr_up = Button(self.screen, self.fg_color, 0, (self.ptr_u_d_x+1, self.ptr_u_y), (self.ptr_u_d_width, self.ptr_u_d_height))
        self.ptr_down = Button(self.screen, self.fg_color, 0, (self.ptr_u_d_x+1, self.ptr_d_y), (self.ptr_u_d_width, self.ptr_u_d_height))
        
        self.ptr_rect_up = self.ptr_up.get_rect()
        self.ptr_rect_down = self.ptr_down.get_rect()
        self.stats_scr_wheel_height = (SCR_HEIGHT * (SCR_HEIGHT / self.stats_texts_size)) - (self.ptr_rect_up.bottom + (SCR_HEIGHT - self.ptr_rect_down.top) + 6) + 23
        self.info_scr_wheel_height = (SCR_HEIGHT * (SCR_HEIGHT / self.info_texts_size)) - (self.ptr_rect_up.bottom + (SCR_HEIGHT - self.ptr_rect_down.top) + 6) + 23
        
        self.info_scroll_wheel = Button(self.screen, self.fg_color, 0, (self.ptr_u_d_x, self.scr_wheel_y), (self.ptr_u_d_width, self.info_scr_wheel_height))
        self.stats_scroll_wheel = Button(self.screen, self.fg_color, 0, (self.ptr_u_d_x, self.scr_wheel_y), (self.ptr_u_d_width, self.stats_scr_wheel_height))
        
        self.pause_focus = 0
        self.setting_focus = 0
        self.start_opt_foc = self.setting_focus

        self.cursor_counter = 1
        self.scr_focus = 0

        self.scr_whl_color_num = 255
        self.ptr_up_color_num = 255
        self.ptr_down_color_num = 255
        self.ptr1_color_num = 255
        self.ptr2_color_num = 255
        self.action_num = 255

        self.mouse_pressed = False
        self.paused_scr = False
        self.settings_scr = False
        self.info_scr = False
        self.stats_scr = False
        self.multiplayer_scr = False
        self.setting_name_focused = True
        self.thread1_started = True
        self.thread2_started = True
        self.typing = False
        self.write_to_file = True

        self.start_options = ['contnue', 'new game', 'multiplayer']

        self.start_focus = 0

        self.start_timer = time.time()
        self.words = []
        self.cursor = len(str(self.bg_txt_view_input))
        self.just_started = True

        self.apply_settings_changes = False
        self.mouse_y_speed = False
        self.rect_assigned = False
        self.started = False
        self.loaded = False
        self.removed = True
        self.start_click_check = True
        self.settings_disabled = False
        
        self.click_timer = 0
        
        self.pause_outline = pygame.Rect(SCR_WIDTH, 0, 0, 0)
        
        self.cursor_img = pygame.image.load(r'utils\img\onhover.png')
        self.cursor_img = pygame.transform.rotozoom(self.cursor_img, 0, .5)
        
        self.max_link_hit_rect = pygame.Rect(0, 0, 0, 0)
        self.mlhr_width = 0
        
        self._get_skins()
        self.t1 = time.time()

    def _load_saved_values(self):
        with open(CONTINUE_VARIABLE_DIR) as same_file:
            self.saved_vars = json.loads(same_file.read())
        with open(SETTINGS_DIR) as file:
            self.saved_data = json.loads(file.read())
            
            self.bg_txt_view_input = self.bg_color = self.saved_data['bg_color'] if not isinstance(self.saved_data['bg_color'], list) else tuple(self.saved_data['bg_color'])
            self.fg_txt_view_input = self.fg_color = col = self.saved_data['fg_color'] if not isinstance(self.saved_data['fg_color'], list) else tuple(self.saved_data['fg_color'])
            
            self.ad_index = self.saved_data['ad_index']
            self.pc1_index = self.saved_data['pc1_index']
            self.pc2_index = self.saved_data['pc2_index']
            
            self.player1_up_txt_view_input, self.player1_up = self.saved_data['key1_up']
            self.player1_down_txt_view_input, self.player1_down = self.saved_data['key1_down']
            self.player2_up_txt_view_input, self.player2_up = self.saved_data['key2_up']
            self.player2_down_txt_view_input, self.player2_down = self.saved_data['key2_down']

            self.is_a_new_game = self.saved_data['is a new game']
        with open(STATS_DIR) as stats_file:
            self.stats_val = json.loads(stats_file.read())

    def _validate_text_view(self):
        if self.apply_settings_changes:
            if len(str(self.bg_txt_view_input).split(',')) in (3, 4):
                self.bg_txt_view_input = tuple(int(i) for i in str(self.bg_txt_view_input).removeprefix('(').removesuffix(')').removeprefix('[').removesuffix(']').split(','))
            if len(str(self.fg_txt_view_input).split(',')) in (3, 4):
                self.fg_txt_view_input = tuple(int(i) for i in str(self.fg_txt_view_input).removeprefix('(').removesuffix(')').removeprefix('[').removesuffix(']').split(','))
            
            self.bg_txt_view_input = mods.check_valid_color(self.bg_txt_view_input, self.bg_color)
            self.bg_input = TextView(self.bg_txt_view_input, self.screen, MAX_TV_LEN)
            
            self.fg_txt_view_input = mods.check_valid_color(self.fg_txt_view_input, self.fg_color)
            self.fg_input = TextView(self.fg_txt_view_input, self.screen, MAX_TV_LEN)

    def _save_and_apply_settings(self):
        if self.apply_settings_changes:
            indexes_changed = (self.ad_index != self.saved_data['ad_index']) or (self.pc1_index != self.saved_data['pc1_index']) or (self.pc2_index != self.saved_data['pc2_index'])
            
            self._validate_text_view()
            
            self.bg_color = mods.check_valid_color(self.bg_txt_view_input, self.bg_color)
            self.fg_color = mods.check_valid_color(self.fg_txt_view_input, self.fg_color)
            
            if indexes_changed:
                self._reset_control_timer()
                self._restart(False, False)
                
            with open(SETTINGS_DIR, "w") as settings:
                self.saved_data['bg_color'] = self.bg_color
                self.saved_data['fg_color'] = self.fg_color
                self.saved_data['key1_up'] = (self.player1_up_txt_view_input, self.player1_up)
                self.saved_data['key1_down'] = (self.player1_down_txt_view_input, self.player1_down)
                self.saved_data['key2_up'] = (self.player2_up_txt_view_input, self.player2_up)
                self.saved_data['key2_down'] = (self.player2_down_txt_view_input, self.player2_down)
                self.saved_data['ad_index'] = self.ad_index
                self.saved_data['pc1_index'] = self.pc1_index
                self.saved_data['pc2_index'] = self.pc2_index
                
                new_info = json.dumps(self.saved_data, indent=2)
                settings.write(new_info)

    def _restart(self, resume: bool, include_pause: bool = True):
        self.player1 = Player(self.screen, SCR_WIDTH/2, P1_START_POS)
        self.player2 = Player(self.screen, SCR_WIDTH/2, P2_START_POS)
        self.ball = Ball(SCR_WIDTH/2, SCR_HEIGHT/2, random.choice([1, -1]), random.choice([1, -1]), self.screen)

        self.player1_score = 0
        self.player2_score = 0
        
        if include_pause:
            self.pause_focus = 0
        
        if resume:
            self.paused_scr = False
            self.info_scr = False
            self.stats_scr = False
            self.settings_scr = False

    def _continue_game(self):
        with open(CONTINUE_VARIABLE_DIR) as file:
            self.cvd_vals = json.loads(file.read())
            
            score1 = self.cvd_vals['player 1 score']
            score2 = self.cvd_vals['player 2 score']
            y1 = self.cvd_vals['player 1 pos']
            y2 = self.cvd_vals['player 2 pos']
            bxp = self.cvd_vals['self.ball x pos']
            byp = self.cvd_vals['self.ball y pos']
            bx = self.cvd_vals['self.ball x']
            by = self.cvd_vals['self.ball y']
        
        self.player1 = Player(self.screen, SCR_WIDTH/2, P1_START_POS, y1)
        self.player2 = Player(self.screen, SCR_WIDTH/2, P2_START_POS, y2)
        self.ball = Ball(bx, by, bxp, byp, self.screen, score1, score2)

    def _save_and_exit(self, exit_only: bool = False):
        if not exit_only:
            with open(CONTINUE_VARIABLE_DIR, "w") as file:
                p1_pos, _ = self.player1.get_rect_vals()
                p2_pos, _ = self.player2.get_rect_vals()
                bxp = self.ball.ball_x_pos
                byp = self.ball.ball_y_pos
                bx = self.ball.get_rect().x
                by = self.ball.get_rect().y
                
                self.saved_vars['player 1 score'] = self.player2_score
                self.saved_vars['player 2 score'] = self.player1_score
                self.saved_vars['player 1 pos'] = p1_pos.y
                self.saved_vars['player 2 pos'] = p2_pos.y
                self.saved_vars['self.ball x pos'] = bxp
                self.saved_vars['self.ball y pos'] = byp
                self.saved_vars['self.ball x'] = bx
                self.saved_vars['self.ball y'] = by
                
                new_var_info = json.dumps(self.saved_vars, indent=2)
                file.write(new_var_info)
            self._save_and_apply_settings()
        
        if self.is_a_new_game:
            with open(SETTINGS_DIR, 'w') as file:
                self.saved_data['is a new game'] = False

                new_vals = json.dumps(self.saved_data, indent=2)
                file.write(new_vals)

        pygame.quit()
        sys.exit()

    def _pause_actions(self, action):
        match action:
            case 'Exit':
                self._save_and_exit()
            case 'Information':
                self.info_scr = True
            case 'Resume':
                self.paused_scr = False
            case 'Restart':
                self._restart(True)
                self._reset_control_timer()
            case 'Settings':
                self.settings_scr = True
            case 'Statistics':
                self.stats_scr = True
    
    def _scroll_up_down(self, up: bool):
        if up:
            self.scr_wheel_y -= self.s_speed
            if self.scr_wheel_y != self.ptr_rect_up.bottom:
                self.scr_focus -= self.s_speed * (1 / (SCR_HEIGHT / self.y_val))
        else:
            self.scr_wheel_y += self.s_speed
            if self.scr_wheel_rect.bottom != self.ptr_rect_down.top:
                self.scr_focus += self.s_speed * (1 / (SCR_HEIGHT / self.y_val))
    
    def _pbo_mouse_func(self, person, val):
        if self.use_mouse and not self.settings_disabled and val != (self.pob_focus if person == 'pob' else self.ptb_focus):
            if person == 'pob':
                self.pob_focus = val
            elif person == 'ptb':
                self.ptb_focus = val
    
    def _setting_mouse_func(self, i):
        if self.use_mouse and not self.settings_disabled and self.setting_option_background_rects.index(i) != self.setting_focus:
            self.pob_focus = 1
            self.ptb_focus = 1
            self.setting_focus = self.setting_option_background_rects.index(i)
            self.apply_settings_changes = True
            self._validate_text_view()
        
    def _pause_mouse_func(self, i):
        if self.use_mouse and self.pause_focus != self.new_pause_rects.index(i):
            self.pause_focus = self.new_pause_rects.index(i)

    def _link_click(self, x, y):
        pygame.draw.line(self.screen, self.link_color, (x, y + FN3_SIZE*2.5), (x + self.txt_width, y + FN3_SIZE*2.5), 2)
        pygame.mouse.set_visible(False)
        self.screen.blit(self.cursor_img, (self.mouse_rect.x, self.mouse_rect.y))
        self.cursor_counter += 1

    def _start_options(self):
        if self.rects_name[self.start_focus] == 'Continue':
            self._continue_game()
            self.started = True
        elif self.rects_name[self.start_focus] == 'New Game':
            self._restart(True)
            self.started = True
        elif self.rects_name[self.start_focus] == 'Multiplayer':
            self.multiplayer_scr = True

    def _start_mouse_func(self, i):
        if self.start_use_mouse and self.rects_rects.index(i) != self.start_focus:
            self.start_focus = self.rects_rects.index(i)

    def _go_back(self):
        if self.started:
            if not self.paused_scr and not self.settings_scr and not self.info_scr and not self.stats_scr:
                self.paused_scr = True
            else:
                if self.paused_scr:
                    self.paused_scr = False
                if self.settings_scr and not self.settings_disabled:
                    self.settings_scr = False
                    self.apply_settings_changes = True
                    self.paused_scr = True
                if self.info_scr:
                    self.paused_scr = True
                    self.info_scr = False
                if self.stats_scr:
                    self.stats_scr = False
                    self.paused_scr = True
        else:
            if self.multiplayer_scr:
                self.multiplayer_scr = False
    
    def _get_skins(self):
        for i in self.skin_path:
            if '/player.png' in i.lower() or '/player.jpg' in i.lower():
                self.load_skin_player = True
                self.player_skin_path = i
            if '/background.png' in i.lower() or '/background.jpg' in i.lower():
                self.load_skin_bg = True
                self.bg_skin_path = i
                self.bg_img = pygame.image.load(self.bg_skin_path)
                self.bg_img = pygame.transform.scale(self.bg_img, (SCR_WIDTH, SCR_HEIGHT))
            if '/ball.png' in i.lower() or '/ball.jpg' in i.lower():
                self.load_skin_ball = True
                self.ball_skin_path = i
            if '/ui.png' in i.lower() or '/ui.jpg' in i.lower():
                self.load_skin_ui = True
                self.ui_skin_path = i
                self.ui_img = pygame.image.load(self.ui_skin_path)
    
    def _ptr_up_assign(self):
        self.ptr_up_color_num = ON_HOVER_OPAC
    
    def _ptr_down_assign(self):
        self.ptr_down_color_num = ON_HOVER_OPAC
    
    def _control_timer(self):
        if not self.started_timing:
            self.other_start_time = int(pygame.time.get_ticks() / 1000)-self.time_not_played
            self.started_timing = True
        
        self.time_not_played = int(pygame.time.get_ticks() / 1000)-self.other_start_time
    
    def _reset_control_timer(self):
        self.start_time = int(pygame.time.get_ticks() / 1000)
        self.started_timing = False
        self.other_start_time = int(pygame.time.get_ticks() / 1000)
        self.time_not_played = int(pygame.time.get_ticks() / 1000)-self.other_start_time
        self.play_timer = 0
    
    def _draw_bg(self):
        self.screen.fill(self.bg_color)
        if self.load_skin_bg:
            self.screen.blit(self.bg_img, (0, 0))
    
    
    def game_play(self):
        self.play_timer = (int(pygame.time.get_ticks() / 1000)-self.start_time) - self.time_not_played
        
        self.started_timing = False
        self.write_to_file = True
        
        ball_rect = self.ball.get_rect()
        player1_rect = self.player1.get_rect_vals()
        player2_rect = self.player2.get_rect_vals()
        self.player2_score, self.player1_score = self.ball.get_score()
        
        mods.draw_nums(self.player1_score, SCR_WIDTH, 0, FONT_CELL_SIZE, self.screen, col=self.fg_color, left=True, img=self.ui_img if self.load_skin_ui else None)
        mods.draw_nums(self.player2_score, SCR_WIDTH, 0, FONT_CELL_SIZE, self.screen, col=self.fg_color, left=False, img=self.ui_img if self.load_skin_ui else None)
        
        self.ball.update(BALL_SPEED*self.delta_time, *(player1_rect, player2_rect), col=self.fg_color, skin=self.ball_skin_path if self.load_skin_ball else 'none')
        self.player1.update(self.p1_control, [ball_rect, self.ball.ball_x_pos], True, self.mouse, speed=(PLAYER_SPEED*self.delta_time), col=self.fg_color, ai_difficulty=self.ai_difficulty, skin=self.player_skin_path if self.load_skin_player else 'none', up=self.player1_up, down=self.player1_down)
        self.player2.update(self.p2_control, [ball_rect, self.ball.ball_x_pos], False, self.mouse, speed=(PLAYER_SPEED*self.delta_time), col=self.fg_color, ai_difficulty=self.ai_difficulty, skin=self.player_skin_path if self.load_skin_player else 'none', up=self.player2_up, down=self.player2_down)
        
        spacing = LINE_SPACE
        
        for _ in range(SCR_HEIGHT//LINE_LEN):
            l_x_pos = SCR_WIDTH/2 - (LINE_WIDTH / 2)
            if self.load_skin_ui:
                self.screen.blit(pygame.transform.scale(self.ui_img, (LINE_WIDTH, LINE_LEN)), (l_x_pos, spacing))
            else:
                pygame.draw.line(self.screen, self.fg_color, (l_x_pos, spacing), (l_x_pos, spacing + LINE_LEN), LINE_WIDTH)
                
            spacing += LINE_LEN + LINE_SPACE
        
        self.screen.blit(FONT2.render(CONTROL_OPTIONS[self.pc1_index], False, self.fg_color), (len(CONTROL_OPTIONS[self.pc1_index]), SCR_HEIGHT-FN2_SIZE*2))
        self.screen.blit(FONT2.render(CONTROL_OPTIONS[self.pc2_index], False, self.fg_color), (SCR_WIDTH-(FN2_SIZE*len(CONTROL_OPTIONS[self.pc2_index])+FN2_SIZE+3), SCR_HEIGHT-FN2_SIZE*2))
    
    def pause(self):
        if self.write_to_file:
            with open(STATS_DIR, 'w') as file:
                self.stats_val['player one high score'] = max(self.stats_val['player one high score'], self.player1_score)
                self.stats_val['player two high score'] = max(self.stats_val['player two high score'], self.player2_score)
                self.stats_val['highest play time'] = max(self.stats_val['highest play time'], self.play_time)
                
                self.pohs = self.stats_val['player one high score']
                self.pths = self.stats_val['player two high score']
                self.hpt = mods.secs_to_time(self.stats_val['highest play time'])
                
                new_stats = json.dumps(self.stats_val, indent=2)
                file.write(new_stats)
            self.write_to_file = False
    
        
        self.pause_outline = pygame.Rect(self.pause_text_rects[self.paused_rects[self.pause_focus]].x - EXIT_SPACE_OFFSET//2,
                                    self.pause_text_rects[self.paused_rects[self.pause_focus]].y,
                                    self.pause_texts[self.paused_rects[self.pause_focus]].get_width() + EXIT_SPACE_OFFSET,
                                    self.pause_texts[self.paused_rects[self.pause_focus]].get_height())
        
        pygame.draw.rect(self.screen, self.fg_color, self.pause_outline, FOCUS_RECT_WIDTH, BORDER_RAD, BORDER_RAD, BORDER_RAD, BORDER_RAD, BORDER_RAD)
        
        self.screen.blit(FONT1.render('Game Paused', False, self.fg_color), (mods.position(SCR_WIDTH, 'center', 'Game Paused', 57//2.2), 40))
        
        for i in [k for k, _ in self.pause_texts.items()]:
            self.screen.blit(self.pause_texts[i], self.pause_text_rects[i])
    
    def information(self):
        if self.in_stats_or_help:
            self.scr_focus = 0
            self.scr_wheel_y = self.ptr_rect_up.bottom
            self.in_stats_or_help = False
        
        self.y_val = 70
        self.vals, self.surf, self.list_val, _ = mods.multiline_write(HELP_INFO, FONT3, self.link_color, self.fg_color)
        
        self.screen.blit(FONT1.render('Information', False, self.fg_color), pygame.Rect(mods.position(SCR_WIDTH, 'center', 'IFEs Pong', FN1_SIZE), -50+mods.clamp(self.y_val-self.scr_focus, self.y_val, -(FN3_SIZE+TXT_PAD)), 0, 0))
        
        self.scr_focus = max(self.scr_focus, 0)
        
        self.scr_wheel_y = mods.clamp(self.scr_wheel_y, (self.ptr_rect_down.top - self.info_scr_wheel_height) + 1, self.ptr_rect_up.bottom)
        self.scr_wheel_rect = pygame.Rect(self.ptr_u_d_x, self.scr_wheel_y, self.ptr_u_d_width, self.info_scr_wheel_height)
        
        self.info_scroll_wheel.activate_button(pos=(self.scr_wheel_rect.x, self.scr_wheel_rect.y), color=self.fg_color)
        
        if self.mouse_rect.colliderect(self.scr_wheel_rect):
            self.scr_whl_color_num = ON_HOVER_OPAC
            if self.mouse_was_clicked:
                self.mouse_y_speed = True
            else:
                self.mouse_y_speed = False
        else:
            self.scr_whl_color_num = 255
            
        if not self.mouse_was_clicked:
            self.mouse_y_speed = False
        
        self.scr_focus = (self.scr_focus - ((self.scr_wheel_rect.top / (round((self.ptr_rect_down.top - self.info_scr_wheel_height))+1)) * self.scr_focus)) + ((self.scr_wheel_rect.top / (round((self.ptr_rect_down.top - self.info_scr_wheel_height))+1)) * self.scr_focus)

        list_of_linkrects_x = []
        list_of_linkrects_width = []
        for k, v in enumerate(self.surf):
            x = mods.position(SCR_WIDTH, 'center', self.vals[k], FN3_SIZE)
            y = mods.clamp(self.y_val-self.scr_focus, self.y_val, -(FN3_SIZE+TXT_PAD + 5))
            if self.list_val[k] in LINK_KEY:
                t_s_x, t_s_y = v.get_rect().size
                rects = pygame.Rect(x, y, t_s_x, t_s_y)
                list_of_linkrects_x.append(rects.x)
                list_of_linkrects_width.append(rects.width)
        
        list_of_linkrects: list[pygame.Rect] = []
        for k, v in enumerate(self.surf):
            x = mods.position(SCR_WIDTH, 'center', self.vals[k], FN3_SIZE)
            y = mods.clamp(self.y_val-self.scr_focus, self.y_val, -(FN3_SIZE+TXT_PAD + 5))
            self.screen.blit(v, pygame.Rect(x, y, 0, 0))
            self.txt_width, _ = v.get_rect().size
            
            
            if self.list_val[k] in HEADERS:
                pygame.draw.line(self.screen, self.fg_color, (x, y + FN3_SIZE*2.5), (x + self.txt_width, y + FN3_SIZE*2.5), 1)

            if self.list_val[k] in LINK_KEY:
                t_s_x, t_s_y = v.get_rect().size
                link_rect = pygame.Rect(x, y, t_s_x, t_s_y)
                
                if len(list_of_linkrects) <= len(LINK_KEY):
                    list_of_linkrects.append(link_rect)
                
                if t_s_x > self.mlhr_width:
                    self.mlhr_width = t_s_x
                
                self.max_link_hit_rect.left = min(list_of_linkrects_x)
                
                if self.list_val[k] == LINK_KEY[0]:
                    self.max_link_hit_rect.y = link_rect.top
                    self.max_link_hit_rect.width = self.mlhr_width
                
                if self.list_val[k] == LINK_KEY[-1]:
                    self.max_link_hit_rect.height =  link_rect.bottom - self.max_link_hit_rect.y
                
                dead_zone_list = []
                for k, v in enumerate(list_of_linkrects):
                    if k != len(list_of_linkrects) - 1:
                        cords = v.x, v.bottom, self.mlhr_width, list_of_linkrects[k + 1].top - v.bottom
                    else:
                        cords = v.x, v.bottom, self.mlhr_width, 0
                    dead_zone_list.append(cords)
            
                        
                if not self.mouse_rect.colliderect(self.max_link_hit_rect):
                    pygame.mouse.set_visible(True)
                else:
                    for i in dead_zone_list:
                        if self.mouse_rect.colliderect(i):
                            pygame.mouse.set_visible(True)
                
                if self.mouse_rect.colliderect(link_rect):
                    if mods.isclicked(self.mouse_rect, link_rect, self.mouse_was_clicked, lambda: self._link_click(x, y)):
                        if self.mouse_pressed:
                            link = self.vals[k].replace('!', '')
                            link_starter = thread.Thread(target=mods.link_opener, args=(LINKS.get(link), ))
                            link_starter.start()
                            self.mouse_pressed = False

            self.y_val += FN3_SIZE+TXT_PAD
        
        self.s_speed = SCROLL_SPEED / (1 / (SCR_HEIGHT / self.y_val))

        self.ptr_up.activate_button(lambda: self._scroll_up_down(True), no_bounce=True, color=self.fg_color)
        self.ptr_down.activate_button(lambda: self._scroll_up_down(False), no_bounce=True, color=self.fg_color)
        
        if self.keys[pygame.K_UP]:
            self._scroll_up_down(True)
        if self.keys[pygame.K_DOWN]:
            self._scroll_up_down(False)
        
        end_of_scr = 2952
        
        if self.keys[pygame.K_HOME]:
            self.scr_focus = 0
            self.scr_wheel_y = self.ptr_rect_up.bottom
        elif self.keys[pygame.K_END]:
            self.scr_focus = end_of_scr
            self.scr_wheel_y = (self.ptr_rect_down.top - self.info_scr_wheel_height) + 1
        
        self.s_speed = (SCROLL_SPEED / SCR_HEIGHT) * (self.ptr_rect_up.bottom + (SCR_HEIGHT - self.ptr_rect_down.top))
        
        if self.mouse_y_speed:
            self.scr_whl_color_num = ON_CLICK_OPAC
            self.s_speed = pygame.mouse.get_rel()[1]
            self.scr_wheel_y += self.s_speed
            if (self.scr_wheel_rect.bottom != self.ptr_rect_down.top) and (self.scr_wheel_y != self.ptr_rect_up.bottom):
                self.scr_focus += self.s_speed * (1 / (SCR_HEIGHT / self.y_val))
        
        if self.load_skin_ui:
            self.screen.blit(pygame.transform.scale(self.ui_img, (self.scr_wheel_rect.width, self.scr_wheel_rect.height)), self.scr_wheel_rect)
            self.screen.blit(pygame.transform.scale(self.ui_img, (self.ptr_rect_up.width, self.ptr_rect_up.height)), self.ptr_rect_up)
            self.screen.blit(pygame.transform.scale(self.ui_img, (self.ptr_rect_down.width, self.ptr_rect_down.height)), self.ptr_rect_down)
        
    def statistics(self):
        if not self.in_next_update:
            self.font4 = pygame.font.Font('utils/fonts/font(1).ttf',100)
            self.screen.blit(self.coming_soon, self.coming_soon_pos)
        else:
            stats_info = gc.all_stats(self.pohs, self.pths, ltsp=self.hpt)
            
            self.ptr_rect_up = pygame.Rect(self.ptr_u_d_x, self.ptr_u_y, self.ptr_u_d_width, self.ptr_u_d_height)
            self.ptr_rect_down = pygame.Rect(self.ptr_u_d_x, self.ptr_d_y, self.ptr_u_d_width, self.ptr_u_d_height)
            
            if self.in_stats_or_help:
                self.scr_focus = 0
                self.scr_wheel_y = self.ptr_rect_up.bottom
                self.in_stats_or_help = False
            
            self.y_val = 70
            self.vals, self.surf, self.list_val, _ = mods.multiline_write(stats_info, FONT3, self.link_color, self.fg_color)
            
            self.screen.blit(FONT1.render('Statistics', False, self.fg_color), pygame.Rect(mods.position(SCR_WIDTH, 'center', 'Statistics', FN1_SIZE), -50 + mods.clamp(self.y_val-self.scr_focus, self.y_val, -(FN3_SIZE+TXT_PAD)), 0, 0))
            
            self.scr_focus = max(self.scr_focus, 0)
            
            self.scr_wheel_y = mods.clamp(self.scr_wheel_y, (self.ptr_rect_down.top - self.stats_scr_wheel_height) + 1, self.ptr_rect_up.bottom)
            self.scr_wheel_rect = pygame.Rect(self.ptr_u_d_x, self.scr_wheel_y, self.ptr_u_d_width, self.stats_scr_wheel_height)
            
            self.stats_scroll_wheel.activate_button(pos=(self.scr_wheel_rect.x, self.scr_wheel_rect.y), color=self.fg_color)
            
            if self.mouse_rect.colliderect(self.scr_wheel_rect):
                self.scr_whl_color_num = ON_HOVER_OPAC
                if self.mouse_was_clicked:
                    self.mouse_y_speed = True
                else:
                    self.mouse_y_speed = False
            else:
                self.scr_whl_color_num = 255
                
            if not self.mouse_was_clicked:
                self.mouse_y_speed = False
            
            self.scr_focus = (self.scr_focus - ((self.scr_wheel_rect.top / (round((self.ptr_rect_down.top - self.stats_scr_wheel_height))+1)) * self.scr_focus)) + ((self.scr_wheel_rect.top / (round((self.ptr_rect_down.top - self.stats_scr_wheel_height))+1)) * self.scr_focus)
            
            for k, v in enumerate(self.surf):
                x = mods.position(SCR_WIDTH, 'center', self.vals[k], FN3_SIZE)
                y = mods.clamp(self.y_val-self.scr_focus, self.y_val, -(FN3_SIZE+TXT_PAD + 5))
                self.screen.blit(v, pygame.Rect(x, y, 0, 0))
                self.txt_width, _ = v.get_rect().size
                
                self.y_val += FN3_SIZE+TXT_PAD
            
            self.s_speed = SCROLL_SPEED / (1 / (SCR_HEIGHT / self.y_val))

            self.ptr_up.activate_button(lambda: self._scroll_up_down(True), no_bounce=True, color=self.fg_color)
            self.ptr_down.activate_button(lambda: self._scroll_up_down(False), no_bounce=True, color=self.fg_color)
            
            if self.keys[pygame.K_UP]:
                self._scroll_up_down(True)
            if self.keys[pygame.K_DOWN]:
                self._scroll_up_down(False)
            
            if self.keys[pygame.K_HOME]:
                self.scr_focus = 0
                self.scr_wheel_y = self.ptr_rect_up.bottom
            elif self.keys[pygame.K_END]:
                self.scr_focus = len(stats_info.split('\n')) * (FONT3.get_height() / 2)
                self.scr_wheel_y = (self.ptr_rect_down.top - self.stats_scr_wheel_height) + 1
            
            self.s_speed = (SCROLL_SPEED / SCR_HEIGHT) * (self.ptr_rect_up.bottom + (SCR_HEIGHT - self.ptr_rect_down.top))
            
            if self.mouse_y_speed:
                self.scr_whl_color_num = ON_CLICK_OPAC
                self.s_speed = pygame.mouse.get_rel()[1]
                self.scr_wheel_y += self.s_speed
                if (self.scr_wheel_rect.bottom != self.ptr_rect_down.top) and (self.scr_wheel_y != self.ptr_rect_up.bottom):
                    self.scr_focus += self.s_speed * (1 / (SCR_HEIGHT / self.y_val))
            
            if self.load_skin_ui:
                self.screen.blit(pygame.transform.scale(self.ui_img, (self.scr_wheel_rect.width, self.scr_wheel_rect.height)), self.scr_wheel_rect)
                self.screen.blit(pygame.transform.scale(self.ui_img, (self.ptr_rect_up.width, self.ptr_rect_up.height)), self.ptr_rect_up)
                self.screen.blit(pygame.transform.scale(self.ui_img, (self.ptr_rect_down.width, self.ptr_rect_down.height)), self.ptr_rect_down)
        
    def settings(self):
        self.warnig_surf = pygame.font.Font('utils/fonts/font(2).ttf', 10).render('Changes made will reset the game', False, self.bg_color)
        
        height = 55
        x = height
        width = SCR_WIDTH - (x * 2)
        
        self.settings_background = pygame.Rect(x,
                                          self.setting_text_rects[self.setting_rects[self.setting_focus]].y - Y_OPTION_SPACE_OFFSET/2,
                                          width,
                                          height
                                          )
        
        pygame.draw.rect(self.screen, self.fg_color, self.settings_background)
        if self.load_skin_ui:
            self.screen.blit(pygame.transform.scale(self.action_ui_img, (self.settings_background.width, self.settings_background.height)), (self.settings_background.x, self.settings_background.y))
        
        is_index_changed = (((self.saved_data['ad_index'] != self.ad_index) and (f'{self.setting_rects[self.setting_focus]} opt' == self.ai_key_opt)) or
                            ((self.saved_data['pc1_index'] != self.pc1_index) and (f'{self.setting_rects[self.setting_focus]} opt' == self.p1c_key_opt))or
                            ((self.saved_data['pc2_index'] != self.pc2_index) and (f'{self.setting_rects[self.setting_focus]} opt' == self.p2c_key_opt)))
        
        if is_index_changed:
            warning_pos = (self.setting_text_rects[f'{self.setting_rects[self.setting_focus]} opt'].centerx - (self.warnig_surf.get_width() / 2),
                           self.settings_background.bottom - self.warnig_surf.get_height())
            self.screen.blit(self.warnig_surf, warning_pos)
        
        self.tv_bg_color = [self.fg_color, self.bg_color]
        self.tv_fg_color = [self.fg_color, self.bg_color]
        self.aid_color = self.fg_color
        self.p1_color = self.fg_color
        self.p2_color = self.fg_color
        self.pob_color = self.fg_color
        self.ptb_color = self.fg_color
    
        for i in self.setting_texts.keys():
            self.screen.blit(self.setting_texts[i], self.setting_text_rects[i])
        
        match self.setting_rects[self.setting_focus]:
            case self.bg_key:
                self.tv_bg_color = [self.bg_color, self.fg_color]
                self.bg_txt_view_input = self.bg_input.activate_text_view(self.setting_texts[self.bg_opt_key], self.setting_text_rects[self.bg_opt_key], self.tv_bg_color[0], self.tv_bg_color[1])
            case self.fg_key:
                self.tv_fg_color = [self.bg_color, self.fg_color]
                self.fg_txt_view_input = self.fg_input.activate_text_view(self.setting_texts[self.fg_opt_key], self.setting_text_rects[self.fg_opt_key], self.tv_fg_color[0], self.tv_fg_color[1])
            case self.p1c_key:
                self.p1_color = self.bg_color
                self.p1_control, self.pc1_index = self.p1_control_selector.activate_selector(self.setting_texts[self.p1c_key_opt], self.setting_text_rects[self.p1c_key_opt], self.p1_color)
            case self.p2c_key:
                self.p2_color = self.bg_color
                self.p2_control, self.pc2_index = self.p2_control_selector.activate_selector(self.setting_texts[self.p2c_key_opt], self.setting_text_rects[self.p2c_key_opt], self.p2_color)
            case self.ai_key:
                self.aid_color = self.bg_color
                self.ai_difficulty, self.ad_index = self.ai_difficulty_selector.activate_selector(self.setting_texts[self.ai_key_opt], self.setting_text_rects[self.ai_key_opt], self.aid_color)
            case self.pob_key:
                mini_win_bg_color = mods.set_color(self.bg_color, 220) if self.bg_color not in ('black', [0, 0, 0], [0, 0, 0, 0], (0, 0, 0), (0, 0, 0, 0)) else 'grey20'
                self.pob_color = self.bg_color
                if self.pob_focus == 1:
                    self.player1_up_txt_view_input, self.player1_up = self.pob_up_input.activate_input_selector(self.setting_texts[self.pob_up_key_opt],
                                                                                                                self.setting_text_rects[self.pob_up_key_opt],
                                                                                                                self.mouse_rect,
                                                                                                                self.mouse_was_clicked,
                                                                                                                self.pob_color,
                                                                                                                self.rel,
                                                                                                                mini_win_bg_color,
                                                                                                                self.fg_color)
                elif self.pob_focus == 2:
                    self.player1_down_txt_view_input, self.player1_down = self.pob_down_input.activate_input_selector(self.setting_texts[self.pob_down_key_opt],
                                                                                                                      self.setting_text_rects[self.pob_down_key_opt],
                                                                                                                      self.mouse_rect,
                                                                                                                      self.mouse_was_clicked,
                                                                                                                      self.pob_color,
                                                                                                                      self.rel,
                                                                                                                      mini_win_bg_color,
                                                                                                                      self.fg_color)
                self.settings_disabled = self.pob_up_input.mini_win.isactive() or self.pob_down_input.mini_win.isactive()
            case self.ptb_key:
                mini_win_bg_color = mods.set_color(self.bg_color, 220) if self.bg_color not in ('black', [0, 0, 0], [0, 0, 0, 0], (0, 0, 0), (0, 0, 0, 0)) else 'grey20'
                self.ptb_color = self.bg_color
                if self.ptb_focus == 1:
                    self.player2_up_txt_view_input, self.player2_up = self.ptb_up_input.activate_input_selector(self.setting_texts[self.ptb_up_key_opt],
                                                                                                                self.setting_text_rects[self.ptb_up_key_opt],
                                                                                                                self.mouse_rect,
                                                                                                                self.mouse_was_clicked,
                                                                                                                self.ptb_color,
                                                                                                                self.rel,
                                                                                                                mini_win_bg_color,
                                                                                                                self.fg_color)
                elif self.ptb_focus == 2:
                    self.player2_down_txt_view_input, self.player2_down = self.ptb_down_input.activate_input_selector(self.setting_texts[self.ptb_down_key_opt],
                                                                                                                      self.setting_text_rects[self.ptb_down_key_opt],
                                                                                                                      self.mouse_rect,
                                                                                                                      self.mouse_was_clicked,
                                                                                                                      self.ptb_color,
                                                                                                                      self.rel,
                                                                                                                      mini_win_bg_color,
                                                                                                                      self.fg_color)
                self.settings_disabled = self.ptb_up_input.mini_win.isactive() or self.ptb_down_input.mini_win.isactive()

        self.saa_button.disabled = self.settings_disabled
        self.saa_button.activate_button(self._save_and_apply_settings, color=(self.fg_color, self.bg_color))
         
    
    def const_main_update(self):
        self._draw_bg()

        self.delta_time = self.clock.tick(FPS)
        self.play_time = round(time.time() - self.t1)
         
        if not self.rect_assigned:
            rect_div = pygame.Rect(ICON_POS, ICON_POS, ICON_SIZE * FN2_SIZE, ICON_SIZE * FN2_SIZE)
            self.action_button_bg = pygame.Rect(rect_div.x - (BG_OFFSET/2), rect_div.y - (BG_OFFSET/2), rect_div.width + BG_OFFSET, rect_div.height + BG_OFFSET)
            if self.load_skin_ui:
                self.action_ui_img = pygame.transform.scale(self.ui_img, (self.action_button_bg.width, self.action_button_bg.height))
            
            self.rect_assigned = True
        
        self.back_button.disabled = self.settings_disabled
        self.back_button.activate_button(self._go_back, color=self.fg_color)
        if self.load_skin_ui:
            self.screen.blit(self.action_ui_img, self.action_button_bg)
        
        self.mouse_was_clicked = pygame.mouse.get_pressed()[0]
        self.mouse = pygame.mouse.get_pos()
        m_x, m_y = self.mouse
        self.mouse_rect = pygame.Rect(m_x, m_y, 1, 1)
        self.link_color = mods.set_color(self.fg_color,  105)
        
        self.pause_texts = {
            'Resume': mods.font_renderer('Resume', FONT3, self.fg_color),
            'Information': mods.font_renderer('Information', FONT3, self.fg_color),
            'Settings': mods.font_renderer('Settings', FONT3, self.fg_color),
            'Statistics': mods.font_renderer('Statistics', FONT3, self.fg_color),
            'Restart': mods.font_renderer('Restart', FONT3, self.fg_color), 
            'Exit': mods.font_renderer('Exit', FONT3, self.fg_color),
        }
        self.pause_text_rects = {
            'Resume': mods.font_rect_renderer('Resume', FN3_SIZE,y_offset=PAUSE_TEXT_START_POS, x_offset= X_PAUSE_TEXT_OFFSET),
            'Information': mods.font_rect_renderer('Information', FN3_SIZE, y_offset=PAUSE_TEXT_START_POS + PAUSE_TEXT_SPACING, x_offset= -X_PAUSE_TEXT_OFFSET),
            'Settings': mods.font_rect_renderer('Settings', FN3_SIZE,y_offset=PAUSE_TEXT_START_POS + PAUSE_TEXT_SPACING*2, x_offset= X_PAUSE_TEXT_OFFSET),
            'Statistics': mods.font_rect_renderer('Statistics', FN3_SIZE,y_offset=PAUSE_TEXT_START_POS + PAUSE_TEXT_SPACING*3, x_offset= -X_PAUSE_TEXT_OFFSET),
            'Restart': mods.font_rect_renderer('Restart', FN3_SIZE, y_offset=PAUSE_TEXT_START_POS + (PAUSE_TEXT_SPACING*4), x_offset= X_PAUSE_TEXT_OFFSET),
            'Exit': mods.font_rect_renderer(' Exit', FN3_SIZE, y_offset=PAUSE_TEXT_START_POS + (PAUSE_TEXT_SPACING*5))
        }
        
        self.setting_texts = {
            self.bg_key: mods.font_renderer(self.bg_key, FONT3, self.tv_bg_color[0]),
            self.fg_key: mods.font_renderer(self.fg_key, FONT3, self.tv_fg_color[0]),
            self.pob_key: mods.font_renderer(self.pob_key, FONT3, self.pob_color),
            self.ptb_key: mods.font_renderer(self.ptb_key, FONT3, self.ptb_color),
            self.ai_key: mods.font_renderer(self.ai_key, FONT3, self.aid_color),
            self.p1c_key: mods.font_renderer(self.p1c_key, FONT3, self.p1_color),
            self.p2c_key: mods.font_renderer(self.p2c_key, FONT3, self.p2_color),
            
            self.bg_opt_key: mods.font_renderer(self.bg_txt_view_input, FONT3, self.tv_bg_color[0]),
            self.fg_opt_key: mods.font_renderer(self.fg_txt_view_input, FONT3, self.tv_fg_color[0]),
            
            self.pob_up_key_opt: mods.font_renderer(f'Up: {self.player1_up_txt_view_input}', FONT3, self.pob_color),
            self.ptb_up_key_opt: mods.font_renderer(f'Up: {self.player2_up_txt_view_input}', FONT3, self.ptb_color),
            self.pob_down_key_opt: mods.font_renderer(f'Down: {self.player1_down_txt_view_input}', FONT3, self.pob_color),
            self.ptb_down_key_opt: mods.font_renderer(f'Down: {self.player2_down_txt_view_input}', FONT3, self.ptb_color),
            
            self.ai_key_opt: mods.font_renderer(self.ai_difficulty, FONT3, self.aid_color),
            self.p1c_key_opt: mods.font_renderer(self.p1_control, FONT3, self.p1_color),
            self.p2c_key_opt: mods.font_renderer(self.p2_control, FONT3, self.p2_color),
        }
        self.setting_text_rects = {
            self.bg_key: mods.font_rect_renderer(self.bg_key, FN3_SIZE,y_offset=OPTION_TEXT_START_POS, x_offset= -X_OPTION_TEXT_OFFSET),
            self.fg_key: mods.font_rect_renderer(self.fg_key, FN3_SIZE,y_offset=OPTION_TEXT_START_POS + OPTION_TEXT_SPACING, x_offset= -X_OPTION_TEXT_OFFSET),
            self.pob_key: mods.font_rect_renderer(self.pob_up_key_opt, FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*2), x_offset= -X_OPTION_TEXT_OFFSET),
            self.ptb_key: mods.font_rect_renderer(self.ptb_up_key_opt, FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*3), x_offset= -X_OPTION_TEXT_OFFSET),
            self.ai_key: mods.font_rect_renderer(self.ai_key, FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*4), x_offset= -X_OPTION_TEXT_OFFSET),
            self.p1c_key: mods.font_rect_renderer(self.p1c_key, FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*5), x_offset= -X_OPTION_TEXT_OFFSET),
            self.p2c_key: mods.font_rect_renderer(self.p2c_key, FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*6), x_offset= -X_OPTION_TEXT_OFFSET),
            
            self.bg_opt_key: mods.font_rect_renderer(self.bg_txt_view_input, FN3_SIZE,y_offset=OPTION_TEXT_START_POS, x_offset= X_OPTION_TEXT_OFFSET),
            self.fg_opt_key: mods.font_rect_renderer(self.fg_txt_view_input, FN3_SIZE,y_offset=OPTION_TEXT_START_POS + OPTION_TEXT_SPACING, x_offset= X_OPTION_TEXT_OFFSET),
            self.ai_key_opt: mods.font_rect_renderer(self.ai_difficulty, FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*4), x_offset= X_OPTION_TEXT_OFFSET),
            
            self.p1c_key_opt: mods.font_rect_renderer(self.p1_control, FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*5), x_offset= X_OPTION_TEXT_OFFSET),
            self.p2c_key_opt: mods.font_rect_renderer(self.p2_control, FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*6), x_offset= X_OPTION_TEXT_OFFSET),

            self.pob_up_key_opt: mods.font_rect_renderer(f'Up: {self.player1_up_txt_view_input}', FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*2), x_offset= X_OPTION_TEXT_OFFSET - FN3_SIZE*6),#*len('UP: ')),
            self.ptb_up_key_opt: mods.font_rect_renderer(f'Up: {self.player2_up_txt_view_input}', FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*3), x_offset= X_OPTION_TEXT_OFFSET - FN3_SIZE*6),#*len(f'UP: ')),
            self.pob_down_key_opt: mods.font_rect_renderer(f'Down: {self.player1_down_txt_view_input}', FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*2), x_offset= X_OPTION_TEXT_OFFSET + FN3_SIZE*8.5),
            self.ptb_down_key_opt: mods.font_rect_renderer(f'Down: {self.player2_down_txt_view_input}', FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*3), x_offset= X_OPTION_TEXT_OFFSET + FN3_SIZE*8.5),
        }
        
        self.paused_rects = [k for k, _ in self.pause_text_rects.items()]
        self.setting_rects = [k for k, _ in self.setting_text_rects.items()]

        self.new_pause_rects = [k for _, k in self.pause_text_rects.items()]

        self.rel = pygame.mouse.get_rel()
        self.use_mouse = self.rel != (0, 0)

    def main_event_loop(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self._save_and_exit()
        
        if self.mouse_was_clicked:
            self.mouse_pressed = True

        self.keys = pygame.key.get_pressed()

        if event.type == pygame.KEYDOWN:
            if self.keys[pygame.K_ESCAPE]:
                self._go_back()
        
        mods.isclicked(self.mouse_rect, self.setting_text_rects[self.pob_up_key_opt], self.mouse_was_clicked, lambda: self._pbo_mouse_func('pob', 1))
        mods.isclicked(self.mouse_rect, self.setting_text_rects[self.pob_down_key_opt], self.mouse_was_clicked, lambda: self._pbo_mouse_func('pob', 2))
        mods.isclicked(self.mouse_rect, self.setting_text_rects[self.ptb_up_key_opt], self.mouse_was_clicked, lambda: self._pbo_mouse_func('ptb', 1))
        mods.isclicked(self.mouse_rect, self.setting_text_rects[self.ptb_down_key_opt], self.mouse_was_clicked, lambda: self._pbo_mouse_func('ptb', 2))
        
        if not self.paused_scr and not self.info_scr and not self.settings_scr and not self.stats_scr:
            pass
        else:
            if not self.settings_scr:
                self.apply_settings_changes = True
                self._save_and_apply_settings()
            
            self.setting_option_background_rects = []
            
            if not self.info_scr and not self.stats_scr:
                self.in_stats_or_help = True
            
            for i in [(i, k) if ' opt' not in i else 'skip' for i, k in self.setting_text_rects.items()]:
                if i != 'skip':
                    height = 55
                    x = height
                    width = SCR_WIDTH - (x * 2)
                    
                    background_rect = pygame.Rect(x,
                                                  i[1].y - Y_OPTION_SPACE_OFFSET/2,
                                                  width,
                                                  height
                                                 )
                    self.setting_option_background_rects.append(background_rect)
            
            if self.paused_scr:
                for i in self.new_pause_rects:
                    if mods.isclicked(self.mouse_rect, i, self.mouse_was_clicked, lambda: self._pause_mouse_func(i)):
                        self._pause_actions(self.paused_rects[self.pause_focus])
            
            if self.settings_scr:
                for i in self.setting_option_background_rects:
                    mods.isclicked(self.mouse_rect, i, self.mouse_was_clicked, lambda: self._setting_mouse_func(i))
            else:
                self.setting_focus = 0
            
            if event.type == pygame.KEYDOWN:
                if not self.info_scr and not self.settings_scr and not self.stats_scr:
                    if self.keys[pygame.K_UP]:
                        self.pause_focus -= 1
                        self.pause_focus = mods.clamp(self.pause_focus, len(self.paused_rects)-1, 0)
                        self.use_mouse = False
                    elif self.keys[pygame.K_DOWN]:
                        self.pause_focus += 1
                        self.pause_focus = mods.clamp(self.pause_focus, len(self.paused_rects)-1, 0)
                        self.use_mouse = False
                        
                    if self.keys[pygame.K_RETURN]:
                        self._pause_actions(self.paused_rects[self.pause_focus])
                else:
                    if self.settings_scr:
                        if self.keys[pygame.K_UP] and not self.settings_disabled:
                            self.pob_focus = 1
                            self.ptb_focus = 1
                            self.temp = self.setting_focus
                            self.setting_focus-=1
                            self.setting_focus = mods.clamp(self.setting_focus, (len(self.setting_rects)-3)//2, 0)
                            if self.temp != self.setting_focus:
                                self.apply_settings_changes = True
                            
                            self._validate_text_view()
                        elif self.keys[pygame.K_DOWN] and not self.settings_disabled:
                            self.pob_focus = 1
                            self.ptb_focus = 1
                            self.temp = self.setting_focus
                            self.setting_focus+=1
                            self.setting_focus = mods.clamp(self.setting_focus, (len(self.setting_rects)-3)//2, 0)
                            if self.temp != self.setting_focus:
                                self.apply_settings_changes = True
                            
                            self._validate_text_view()
                        
                        match self.setting_rects[self.setting_focus]:
                            case self.pob_key:
                                if self.keys[pygame.K_LEFT]:
                                    self.pob_focus -= 1
                                elif self.keys[pygame.K_RIGHT]:
                                    self.pob_focus += 1
                                self.pob_focus = mods.clamp(self.pob_focus, 2, 1)
                            case self.ptb_key:
                                if self.keys[pygame.K_LEFT]:
                                    self.ptb_focus -= 1
                                elif self.keys[pygame.K_RIGHT]:
                                    self.ptb_focus += 1
                                self.ptb_focus = mods.clamp(self.ptb_focus, 2, 1)
                            case _:
                                if not self.settings_disabled:
                                    if self.keys[pygame.K_RETURN]:
                                        self._save_and_apply_settings()
    
    def main_loop(self):
        if not self.paused_scr and not self.info_scr and not self.settings_scr and not self.stats_scr:
            self.game_play()
        else:
            self._control_timer()
            if self.info_scr:
                self.information()
            elif self.stats_scr:
                self.statistics()
            elif self.settings_scr:
                self.settings()
            else:
                self.pause()

    
    def const_started_update(self):
        self._control_timer()
        
        self.font4 = pygame.font.Font('utils/fonts/font(1).ttf',100)
        self.coming_soon = self.font4.render('Coming Soon', False, self.fg_color)
        x = (self.screen.get_width() / 2) - (self.coming_soon.get_width() / 2)
        y = (self.screen.get_height() / 2) - (self.coming_soon.get_height() / 2)
        self.coming_soon_pos = x, y
        
        const_offset = 50
        
        if self.is_a_new_game:
            self.start_texts = {
                'New Game': mods.font_renderer('New Game', FONT3, self.fg_color),
                'Multiplayer': mods.font_renderer('Multiplayer', FONT3, self.fg_color),
            }
            self.start_text_rects = {
                'New Game': mods.font_rect_renderer('New Game', FN3_SIZE,y_offset=(self.coming_soon_pos[0]/2) + PAUSE_TEXT_START_POS + const_offset),
                'Multiplayer': mods.font_rect_renderer('mulplayer', FN3_SIZE,y_offset=(self.coming_soon_pos[0]/2) + PAUSE_TEXT_START_POS + PAUSE_TEXT_SPACING + const_offset)
            }
        else:
            self.start_texts = {
                'Continue': mods.font_renderer('Continue', FONT3, self.fg_color),
                'New Game': mods.font_renderer('New Game', FONT3, self.fg_color),
                'Multiplayer': mods.font_renderer('Multiplayer', FONT3, self.fg_color),
            }
            self.start_text_rects = {
                'Continue': mods.font_rect_renderer('Continue', FN3_SIZE, y_offset=(self.coming_soon_pos[0]/2) + PAUSE_TEXT_START_POS + const_offset),
                'New Game': mods.font_rect_renderer('New Game', FN3_SIZE, y_offset=(self.coming_soon_pos[0]/2) + PAUSE_TEXT_START_POS + PAUSE_TEXT_SPACING + const_offset, x_offset=-3),
                'Multiplayer': mods.font_rect_renderer('mulplayer', FN3_SIZE, y_offset=(self.coming_soon_pos[0]/2) + PAUSE_TEXT_START_POS + PAUSE_TEXT_SPACING*2 + const_offset),
            }
        
        self.rects_name = [k for k, _ in self.start_text_rects.items()]
        self.rects_rects = [k for _, k in self.start_text_rects.items()]
    
    def started_event_loop(self, event: pygame.event.Event):
        self.keys = pygame.key.get_pressed()
        self.start_use_mouse = pygame.mouse.get_rel() != (0, 0)
        
        if event.type == pygame.QUIT:
            self._save_and_exit(True)
        if self.multiplayer_scr:
            if self.keys[pygame.K_ESCAPE] or mods.isclicked(self.mouse_rect, self.action_button_bg, self.mouse_was_clicked):
                self.multiplayer_scr = False
                
        for i in self.rects_rects:
            if mods.isclicked(self.mouse_rect, i, self.mouse_was_clicked, lambda: self._start_mouse_func(i)):
                self._start_options()
        
        if event.type == pygame.KEYDOWN:
            if self.keys[pygame.K_RETURN]:
                self._start_options()
            if self.keys[pygame.K_UP]:
                self.start_focus -= 1
                self.start_focus = mods.clamp(self.start_focus, len(self.rects_name)-1, 0)
            if self.keys[pygame.K_DOWN]:
                self.start_focus += 1
                self.start_focus = mods.clamp(self.start_focus, len(self.rects_name)-1, 0)

    def started_main_loop(self):
        start_outline = pygame.Rect(self.start_text_rects[self.rects_name[self.start_focus]].x - EXIT_SPACE_OFFSET//2,
                                    self.start_text_rects[self.rects_name[self.start_focus]].y,
                                    self.start_texts[self.rects_name[self.start_focus]].get_width() + EXIT_SPACE_OFFSET,
                                    self.start_texts[self.rects_name[self.start_focus]].get_height())
        
        self._draw_bg()
        pygame.draw.rect(self.screen, self.fg_color, start_outline, FOCUS_RECT_WIDTH, BORDER_RAD, BORDER_RAD, BORDER_RAD, BORDER_RAD, BORDER_RAD)
        
        temp1_size = -10
        self.ifes_pong_pos = mods.position(SCR_WIDTH//2, 'center', 'IFES PONG', temp1_size),  mods.position(SCR_HEIGHT//2, 'center', ' ', temp1_size) + temp1_size
        
        self.screen.blit(self.font4.render('IFES PONG', False, self.fg_color), self.ifes_pong_pos)
        
        for i in [k for k, _ in self.start_texts.items()]:
            self.screen.blit(self.start_texts[i], self.start_text_rects[i])
        
        if self.multiplayer_scr:
            self._draw_bg()
            self.mp_back_button.activate_button(self._go_back)
            
            ################       ######          ###               ################       ####          ####       ##################               ######          ###       ##################        ####                 ####       ################
            ################       #######         ###               ################       ####          ####       ##################               #######         ###       ##################          ####             ####         ################
                  ####             ### ####        ###                     ####             ####          ####       ####                             ### ####        ###       ####                          ####         ####                 ####
                  ####             ###  ####       ###                     ####             ####          ####       ####                             ###  ####       ###       ####                            ####     ####                   ####
                  ####             ###   ####      ###                     ####             ####          ####       ####                             ###   ####      ###       ####                              #### ####                     ####
                  ####             ###    ####     ###                     ####             #### ######## ####       ################                 ###    ####     ###       ################                    #####                       ####
                  ####             ###     ####    ###                     ####             #### ######## ####       ################                 ###     ####    ###       ################                  #### ####                     ####
                  ####             ###      ####   ###                     ####             ####          ####       ####                             ###      ####   ###       ####                            ####     ####                   ####
                  ####             ###       ####  ###                     ####             ####          ####       ####                             ###       ####  ###       ####                          ####         ####                 ####
                  ####             ###        #### ###                     ####             ####          ####       ####                             ###        #### ###       ####                        ####             ####               ####
            ################       ###         #######                     ####             ####          ####       ##################               ###         #######       ##################        ####                 ####             ####
            ################       ###          ######                     ####             ####          ####       ##################               ###          ######       ##################      ####                     ####           ####

            self.screen.blit(self.coming_soon, self.coming_soon_pos)


    def is_started(self):
        return self.started


    def run(self):
        while True:
            self.const_main_update()

            if self.is_started():
                for event in pygame.event.get():
                    self.main_event_loop(event)
                
                self.main_loop()
            
            else:
                self.const_started_update()

                for event in pygame.event.get():
                    self.started_event_loop(event)
                
                self.started_main_loop()
            
            pygame.display.update()




