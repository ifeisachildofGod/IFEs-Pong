
import socket
import pygame
import sys
import json
import random
from pathlib import Path
import threading as thread
from utils.code.main_files.characters import Ball, Player
from utils.code.main_files.widgets import Button, Input, Selector, InputSeletor, Text, ClickableText
import utils.code.constants.game_constants as gc
from utils.code.constants.game_constants import *
from utils.code.constants.ui_constants import *
import bluetooth as bt
import bleak as bk
import utils.code.etc.mods as mods
import time
import asyncio
import pyuac
import pywintypes
import os

pygame.init()

class Game:
    def __init__(self):
        self._init_scr_()
        
        self._init_saved_values()
        
        self._init_timer_vars()
        
        self._init_settings_vars()
        
        self._init_skins()
        
        self._init_global_bool_vars()
        
        self._init_some_very_important_buttons()
        
        self._init_bt_vars()
        
        self._init_multiplayer_scr_vars()
        
        self._init_misc_vars()
        
        self.update()
        
        self._init_characters()
        
        self._init_text_view()
        
        # Don't ever remove these statements
        self.multiplayer_scr = True
        
        self.beginning_update()
        
        # Ever at all
        self.multiplayer_scr = False
        
        self._init_other_widgets_in_settings()
        
        self._init_serv_vars()
        
        self._init_help_info_scr_vars()
        
        self._init_pause_vars()
        
    def _init_scr_(self):
        self.screen = pygame.display.set_mode((SCR_WIDTH, SCR_HEIGHT))
        
        title = 'IFEs Pong'
        pygame.display.set_caption(title)
        
        logo = pygame.image.load('utils/logos/logo.png')
        pygame.display.set_icon(logo)
        self.clock = pygame.time.Clock()
    
    def _init_global_bool_vars(self):
        self.apply_settings_changes = False
        self.mouse_y_speed = False
        self.rect_assigned = False
        self.started = False
        self.settings_disabled = False
        self.start_blitting = False
        self.continue_drawing_button = False
        self.changed_ctrl_state = False
        self.mouse_pressed = False
        self.paused_scr = False
        self.settings_scr = False
        self.info_scr = False
        self.stats_scr = False
        self.multiplayer_scr = False
        self.write_to_file = True
        self.init_once = True
        self.permission_error = False
        
        # self.just_started = False
        # self.loaded = False
        # self.removed = False
        # self.start_click_check = False
        # self.setting_name_focused = False
        # self.thread1_started = False
        # self.thread2_started = False
        # self.typing = False
        # self.help_play_sound = False
    
    def _init_multiplayer_scr_vars(self):
        self.efsb_size = (200, 50)
        self.exit_failed_scr_button = Button(self.screen, self.FG_COLOR, ((SCR_WIDTH / 2) - (self.saa_size[0] / 2), (SCR_HEIGHT / 2) + self.saa_size[1] + 100), self.efsb_size, txt='Go Back', txt_color=self.BG_COLOR, sound_info=self.button_sound_info)
        
        self.multiplayer_scr_bt = False
        self.multiplayer_scr_serv = False
        self.do_once = True
        self.failed_auth = False
        self.start_bt_check = True
    
    def _init_characters(self):
        self.player1 = Player(self.screen, SCR_WIDTH/2, P1_START_POS)
        self.player2 = Player(self.screen, SCR_WIDTH/2, P2_START_POS)
        self.ball = Ball(SCR_WIDTH/2, SCR_HEIGHT/2, random.choice([1, -1]), random.choice([1, -1]), self.screen)
    
    def _init_settings_vars(self):
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
        
        self.mpo_key = 'Multiplayer type'
        self.mpo_opt = f'{self.mpo_key} opt'
            
        self.pob_key = 'Player one Binding'
        self.pob_up_key_opt = f'{self.pob_key} opt up'
        self.pob_down_key_opt = f'{self.pob_key} opt down'
        
        self.ptb_key = 'Player two Binding'
        self.ptb_up_key_opt = f'{self.ptb_key} opt up'
        self.ptb_down_key_opt = f'{self.ptb_key} opt down'
        
        self.ai_difficulty = AI_DIFFICULTY_OPTIONS[self.ad_index]
        
        self.ptb_focus = 1
        self.pob_focus = 1
        
        self.controller_opts = CONTROL_OPTIONS
        
        self.p1_control = self.controller_opts[self.pc1_index]
        self.p2_control = self.controller_opts[self.pc2_index]

        self.tv_bg_color = self.BG_COLOR
        self.tv_fg_color = self.FG_COLOR
        self.aid_color = self.FG_COLOR
        self.p1_color = self.FG_COLOR
        self.p2_color = self.FG_COLOR
        self.pob_color = self.FG_COLOR
        self.ptb_color = self.FG_COLOR
        self.mpo_color = self.FG_COLOR
    
    def _init_skins(self):
        self.skin_path = [i.as_posix() for i in list(Path('SKINS').glob('*.*'))]
        
        self.load_skin_player = False
        self.load_skin_ball = False
        self.load_skin_bg = False
        self.load_skin_ui = False
        
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
    
    def _init_some_very_important_buttons(self):
        self.saa_size = (150, 30)
        self.peb_size = (200, 50)
        
        self.on_focus_widg_vol = .2
        self.on_clicked_widg_vol = .2
        
        self.button_sound_info = ((BUTTON_CLICKED_SOUND_PATH, self.on_clicked_widg_vol), (BUTTON_HOVERED_SOUND_PATH, self.on_focus_widg_vol))
        
        self.back_button = Button(self.screen, self.FG_COLOR, (ICON_POS, ICON_POS), ICON_SIZE*FN3_SIZE, sound_info=self.button_sound_info)
        self.saa_button = Button(self.screen, self.FG_COLOR, (SCR_WIDTH - self.saa_size[0] - 50, SCR_HEIGHT - self.saa_size[1] - 30), self.saa_size, txt='Save and Apply', txt_color=self.BG_COLOR, sound_info=self.button_sound_info)
        self.permission_button = Button(self.screen, self.FG_COLOR, ((SCR_WIDTH / 2) - (self.peb_size[0] / 2), (SCR_HEIGHT / 2) + self.peb_size[1] + 100), self.peb_size, txt='Exit Game', txt_color=self.BG_COLOR, sound_info=self.button_sound_info)
    
    def _init_serv_vars(self):
        width = pygame.font.Font(size=self.saa_size[1]).render('Join', False, 'red').get_width()
        self.jh_size = (width * 2, width)
        
        self.join_button = Button(self.screen, self.FG_COLOR, (SCR_WIDTH - self.saa_size[0] - 200, SCR_HEIGHT - self.saa_size[1] - 30), self.jh_size, txt='Join', txt_color=self.BG_COLOR, sound_info=self.button_sound_info)
        self.host_button = Button(self.screen, self.FG_COLOR, (SCR_WIDTH - self.saa_size[0] - 500, SCR_HEIGHT - self.saa_size[1] - 30), self.jh_size, txt='Host', txt_color=self.BG_COLOR, sound_info=self.button_sound_info)
        
        self.user_name_prompt = FONT4.render('Input user name', False, self.FG_COLOR)
        self.mult_player_x = (self.screen.get_width() / 2) - (self.user_name_prompt.get_width() / 2)
        self.mult_player_y = (self.screen.get_height() / 2) - (self.user_name_prompt.get_height() / 2)
        self.mult_player_y -= self.mult_player_y / 2
        self.mult_player_y -= self.mult_player_y / 4
        self.user_name_prompt_pos = [self.mult_player_x, self.mult_player_y]
        
        self.user_name_tv_width = FONT3.render('Name', False, 'red').get_width()
        self.user_name_tv_width = 700
        self.user_name_tv_pos = (self.screen.get_width() / 2) - (self.user_name_tv_width / 2), self.mult_player_y * 2
        
        self.user_name_tv = Input(self.screen, 'Name', 50, self.user_name_tv_pos, FONT3, self.FG_COLOR, op_space_offset=10, width=self.user_name_tv_width, border_radius=0)
        self.user_name_prompt = Text(self.screen, 'User Name', self.user_name_prompt_pos, FONT4, self.FG_COLOR, key='self.user_name_prompt', directory='utils/json/debug.json', debug=True)
        
        self.join_button.set_rect(centerx=(self.screen.get_width() / 2) - 150, centery=self.user_name_tv_pos[1] * 2)
        self.host_button.set_rect(centerx=(self.screen.get_width() / 2) + 150, centery=self.user_name_tv_pos[1] * 2)
    
    def _init_help_info_scr_vars(self):
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
        
        self.cursor_counter = 1
        self.scr_focus = 0
        
        self.scr_whl_color_num = 255
        self.ptr_up_color_num = 255
        self.ptr_down_color_num = 255
        
        self.y_val = 70
        self.scr_wheel_y = 0
        self.info_texts_size = self.y_val
        self.stats_texts_size = self.y_val
        
        for _ in self.info_surf:
            self.info_texts_size += FN3_SIZE+TXT_PAD
        
        for _ in self.stats_surf:
            self.stats_texts_size += FN3_SIZE+TXT_PAD
        
        self.ptr_up = Button(self.screen, self.FG_COLOR, (self.ptr_u_d_x+1, self.ptr_u_y), (self.ptr_u_d_width, self.ptr_u_d_height), border_radius=0)
        self.ptr_down = Button(self.screen, self.FG_COLOR, (self.ptr_u_d_x+1, self.ptr_d_y), (self.ptr_u_d_width, self.ptr_u_d_height), border_radius=0)
        self.mp_back_button = Button(self.screen, self.FG_COLOR, (ICON_POS, ICON_POS), ICON_SIZE*FN3_SIZE)
        
        self.ptr_rect_up = self.ptr_up.get_rect()
        self.ptr_rect_down = self.ptr_down.get_rect()
        self.stats_scr_wheel_height = (SCR_HEIGHT * (SCR_HEIGHT / self.stats_texts_size)) - (self.ptr_rect_up.bottom + (SCR_HEIGHT - self.ptr_rect_down.top) + 6) + 23
        self.info_scr_wheel_height = (SCR_HEIGHT * (SCR_HEIGHT / self.info_texts_size)) - (self.ptr_rect_up.bottom + (SCR_HEIGHT - self.ptr_rect_down.top) + 6) + 23
        
        self.info_scroll_wheel = Button(self.screen, self.FG_COLOR, (self.ptr_u_d_x, self.scr_wheel_y), (self.ptr_u_d_width, self.info_scr_wheel_height), border_radius=0)
        self.stats_scroll_wheel = Button(self.screen, self.FG_COLOR, (self.ptr_u_d_x, self.scr_wheel_y), (self.ptr_u_d_width, self.stats_scr_wheel_height), border_radius=0)
        
        self.cursor_img = pygame.image.load('utils/img/onhover.png')
        self.cursor_img = pygame.transform.rotozoom(self.cursor_img, 0, .5)
        
        self.max_link_hit_rect = pygame.Rect(0, 0, 0, 0)
    
    def _init_bt_vars(self):
        self.load_timer = 1
        self.load_dot_amount = 1
        self.bt_address_info = []
        self.addresses = []
        self.bt_addr_offset_val = 20
        self.searched = False
        self.opponent_addr = None
        self.authenticated = False
        self.bt_is_not_on = False
        self.customised = False
        self.start_bt_mult_game_timer = 0
        self.retry_timer = 1
        self.start_bt_check_timer = 0
        self.scanner = bk.BleakScanner()
        self.exitting_mult_game = 'false'
        
        self.bt_exit_button = Button(self.screen, self.FG_COLOR, (ICON_POS, ICON_POS), ((ICON_SIZE*FN3_SIZE) * 4, ICON_SIZE*FN3_SIZE), txt='Exit', txt_color=self.BG_COLOR, sound_info=self.button_sound_info)
        self.multiplayer_b_buton = Button(self.screen, self.FG_COLOR, (SCR_WIDTH - (ICON_SIZE*FN3_SIZE) - ICON_POS, ICON_POS), ICON_SIZE*FN3_SIZE, sound_info=self.button_sound_info)
        
    def _init_text_view(self):
        self.fg_input = Input(self.screen, self.fg_txt_view_input, MAX_TV_LEN, (self.fg_t_v.x, self.fg_t_v.y), FONT3, self.FG_COLOR)
        self.bg_input = Input(self.screen, self.bg_txt_view_input, MAX_TV_LEN, (self.bg_t_v.x, self.bg_t_v.y), FONT3, self.FG_COLOR)
    
    def _init_other_widgets_in_settings(self):
        self.ai_difficulty_selector = Selector(self.screen, AI_DIFFICULTY_OPTIONS, self.ad_index, (self.ai_t_v.x, self.ai_t_v.y), FONT3, self.FG_COLOR, circular=True)
        self.p1_control_selector = Selector(self.screen, self.controller_opts, self.pc1_index, (self.p1c_t_v.x, self.p1c_t_v.y), FONT3, self.FG_COLOR, circular=True)
        self.p2_control_selector = Selector(self.screen, self.controller_opts, self.pc2_index, (self.p2c_t_v.x, self.p2c_t_v.y), FONT3, self.FG_COLOR, circular=True)
        self.mpo_selector = Selector(self.screen, ['Server', 'Bluetooth'], self.mpo_index, (self.mpo_s_v.x, self.mpo_s_v.y), FONT3, self.FG_COLOR, circular=True)
        self.pob_up_input = InputSeletor(self.screen, self.player1_up_txt_view_input, self.BG_COLOR, self.FG_COLOR, 'Player one binding up', (self.puko1.x, self.puko1.y), FONT3, self.FG_COLOR, mini_win_logo_path = PONG_LOGO_PNG, _prefix='Up: ')
        self.pob_down_input = InputSeletor(self.screen, self.player1_down_txt_view_input, self.BG_COLOR, self.FG_COLOR, 'Player one binding down', (self.puko2.x, self.puko2.y), FONT3, self.FG_COLOR, mini_win_logo_path = PONG_LOGO_PNG, _prefix='Down: ')
        self.ptb_up_input = InputSeletor(self.screen, self.player2_up_txt_view_input, self.BG_COLOR, self.FG_COLOR, 'Player two binding up', (self.pdko1.x, self.pdko1.y), FONT3, self.FG_COLOR, mini_win_logo_path = PONG_LOGO_PNG, _prefix='Up: ')
        self.ptb_down_input = InputSeletor(self.screen, self.player2_down_txt_view_input, self.BG_COLOR, self.FG_COLOR, 'Player two binding down', (self.pdko2.x, self.pdko2.y), FONT3, self.FG_COLOR, mini_win_logo_path = PONG_LOGO_PNG, _prefix='Down: ')
    
    def _init_pause_vars(self):
        self.mouse_move = 0
        self.pause_focus = 0
        self.setting_focus = 0
        self.start_opt_foc = self.setting_focus
        
    def _init_saved_values(self):
        with open(CONTINUE_VARIABLE_DIR) as same_file:
            self.saved_vars = json.loads(same_file.read())
        with open(SETTINGS_DIR) as file:
            self.saved_data = json.loads(file.read())
            
            self.bg_txt_view_input = self.BG_COLOR = self.saved_data['bg_color'] if not isinstance(self.saved_data['bg_color'], list) else tuple(self.saved_data['bg_color'])
            self.fg_txt_view_input = self.FG_COLOR = self.saved_data['fg_color'] if not isinstance(self.saved_data['fg_color'], list) else tuple(self.saved_data['fg_color'])
            
            self.ad_index = self.saved_data['ad_index']
            self.pc1_index = self.saved_data['pc1_index']
            self.pc2_index = self.saved_data['pc2_index']
            
            self.player1_up_txt_view_input, self.player1_up = self.saved_data['key1_up']
            self.player1_down_txt_view_input, self.player1_down = self.saved_data['key1_down']
            self.player2_up_txt_view_input, self.player2_up = self.saved_data['key2_up']
            self.player2_down_txt_view_input, self.player2_down = self.saved_data['key2_down']

            self.is_a_new_game = self.saved_data['is a new game']
            self.mpo = 'Bluetooth'
            self.mpo_index = 1
        with open(STATS_DIR) as stats_file:
            self.stats_val = json.loads(stats_file.read())

    def _init_timer_vars(self):
        self.start_time = int(pygame.time.get_ticks() / 1000)
        self.started_timing = False
        self.other_start_time = int(pygame.time.get_ticks() / 1000)
        self.time_not_played = int(pygame.time.get_ticks() / 1000)-self.other_start_time
        self.play_timer = 0
    
    def _init_misc_vars(self):
        self.start_focus = 0
        self.t1 = time.time()
        self.in_next_update = False
        self.pause_outline = pygame.Rect(SCR_WIDTH, 0, 0, 0)
        self.mlhr_width = 0
        self.start_blitting_timer = 0
        
        self.coming_soon_surf = mods.make_font(3, 100).render('Coming Soon', False, self.FG_COLOR)
        self.coming_soon_rect = self.coming_soon_surf.get_rect(center=(SCR_WIDTH / 2, SCR_HEIGHT / 2))
        
        self.widg_focused_sound = pygame.mixer.Sound(BUTTON_HOVERED_SOUND_PATH)
        self.widg_focused_sound.set_volume(self.on_focus_widg_vol)
        self.widg_clicked_sound = pygame.mixer.Sound(BUTTON_CLICKED_SOUND_PATH)
        self.widg_clicked_sound.set_volume(self.on_clicked_widg_vol)
    
    
    def _validate_text_view(self):
        if self.apply_settings_changes:
            if len(str(self.bg_txt_view_input).split(',')) in (3, 4):
                self.bg_txt_view_input = tuple(int(i) for i in str(self.bg_txt_view_input).removeprefix('(').removesuffix(')').removeprefix('[').removesuffix(']').split(','))
            if len(str(self.fg_txt_view_input).split(',')) in (3, 4):
                self.fg_txt_view_input = tuple(int(i) for i in str(self.fg_txt_view_input).removeprefix('(').removesuffix(')').removeprefix('[').removesuffix(']').split(','))
            
            self.bg_txt_view_input = mods.check_valid_color(self.bg_txt_view_input, self.BG_COLOR)
            self.fg_txt_view_input = mods.check_valid_color(self.fg_txt_view_input, self.FG_COLOR)
            self._init_text_view()

    def _save_and_apply_settings(self):
        if self.apply_settings_changes:
            indexes_changed = (self.ad_index != self.saved_data['ad_index']) or (self.pc1_index != self.saved_data['pc1_index']) or (self.pc2_index != self.saved_data['pc2_index'])
            
            self._validate_text_view()
            
            self.BG_COLOR = mods.check_valid_color(self.bg_txt_view_input, self.BG_COLOR)
            self.FG_COLOR = mods.check_valid_color(self.fg_txt_view_input, self.FG_COLOR)
            
            if indexes_changed:
                self._reset_control_timer()
                self._restart(False, False)
            try:
                with open(SETTINGS_DIR, "w") as settings:
                    self.saved_data['bg_color'] = self.BG_COLOR
                    self.saved_data['fg_color'] = self.FG_COLOR
                    self.saved_data['key1_up'] = (self.player1_up_txt_view_input, self.player1_up)
                    self.saved_data['key1_down'] = (self.player1_down_txt_view_input, self.player1_down)
                    self.saved_data['key2_up'] = (self.player2_up_txt_view_input, self.player2_up)
                    self.saved_data['key2_down'] = (self.player2_down_txt_view_input, self.player2_down)
                    self.saved_data['ad_index'] = self.ad_index
                    self.saved_data['pc1_index'] = self.pc1_index
                    self.saved_data['pc2_index'] = self.pc2_index
                    
                    new_info = json.dumps(self.saved_data, indent=2)
                    settings.write(new_info)
                    self.permission_error = False
            except PermissionError:
                self.permission_error = True

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
            try:
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
                    self.permission_error = False
            except PermissionError:
                self.permission_error = True
            self._save_and_apply_settings()
        
        if self.is_a_new_game:
            try:
                with open(SETTINGS_DIR, 'w') as file:
                    self.saved_data['is a new game'] = False
                    
                    new_vals = json.dumps(self.saved_data, indent=2)
                    file.write(new_vals)
                    self.permission_error = False
            except PermissionError:
                self.permission_error = True

        pygame.quit()
        sys.exit()

    def _start_actions(self):
        match self.rects_name[self.start_focus]:
            case 'Continue':
                self.widg_clicked_sound.play()
                self._continue_game()
                self.started = True
                self.start_blitting = False
            case 'New Game':
                self.widg_clicked_sound.play()
                self._restart(True)
                self.started = True
                self.start_blitting = False
            case 'Multiplayer':
                self.widg_clicked_sound.play()
                self.multiplayer_scr = True
                self.start_blitting = False
                self.init_once = True
            case 'Exit':
                self.widg_clicked_sound.play()
                self._save_and_exit(True)
    
    def _pause_actions(self, action):
        self.widg_clicked_sound.play()
        match action:
            case 'Exit':
                self._save_and_exit()
            case 'Restart':
                self._restart(True)
                self._reset_control_timer()
                self.start_blitting = False
            case 'Main menu':
                self.start_focus = 0
                self.started = False
                self.paused_scr = False
                self.start_blitting = False
            case 'Information':
                self.info_scr = True
                self.paused_scr = False
            case 'Settings':
                self.settings_scr = True
                self.paused_scr = False
            case 'Statistics':
                self.stats_scr = True
                self.paused_scr = False
            case 'Resume':
                self.paused_scr = False
    
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
        self.use_mouse = self.use_mouse if not self.multiplayer_scr else self.start_use_mouse
        if self.use_mouse and not self.settings_disabled and val != (self.pob_focus if person == 'pob' else self.ptb_focus):
            if person == 'pob':
                self.widg_focused_sound.play()
                self.pob_focus = val
            elif person == 'ptb':
                self.widg_focused_sound.play()
                self.ptb_focus = val
    
    def _setting_mouse_func(self, i):
        self.use_mouse = self.use_mouse if not self.multiplayer_scr else self.start_use_mouse
        if self.use_mouse and not self.settings_disabled and self.setting_option_background_rects.index(i) != self.setting_focus:
            self.widg_focused_sound.play()
            self.pob_focus = 1
            self.ptb_focus = 1
            self.setting_focus = self.setting_option_background_rects.index(i)
            self.apply_settings_changes = True
            self._validate_text_view()
        
    def _pause_mouse_func(self, i):
        if self.use_mouse and self.pause_focus != self.new_pause_rects.index(i):
            self.widg_focused_sound.play()
            self.pause_focus = self.new_pause_rects.index(i)
    
    def _link_click(self, x, y):
        pygame.draw.line(self.screen, self.link_color, (x, y + FN3_SIZE*2.5), (x + self.txt_width, y + FN3_SIZE*2.5), 2)
        pygame.mouse.set_visible(False)
        self.screen.blit(self.cursor_img, (self.mouse_rect.x, self.mouse_rect.y))
        self.cursor_counter += 1
    
    def _start_mouse_func(self, i):
        if self.start_use_mouse and self.rects_rects.index(i) != self.start_focus:
            self.widg_focused_sound.play()
            self.start_focus = self.rects_rects.index(i)

    def _exit_button_was_pressed(self):
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
                self.start_blitting = False
            elif self.multiplayer_scr_serv:
                self.multiplayer_scr_serv = False
                self.multiplayer_scr = True
            elif self.multiplayer_scr_bt:
                self.multiplayer_scr_bt = False
                self.multiplayer_scr = True
                self.searched = False
                self.do_once = True
    
    def _activate_mult_scr(self, pos):
        self.multiplayer_scr = False
        if pos == 1:
            self.multiplayer_scr_bt = True
            self.multiplayer_scr_serv = False
        elif pos == 2:
            self.multiplayer_scr_serv = True
            self.multiplayer_scr_bt = False
    
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
        self.screen.fill(self.BG_COLOR)
        if self.load_skin_bg:
            self.screen.blit(self.bg_img, (0, 0))
    
    def _scroll(self):
        self.scr_wheel_y -= self.mouse_move
        if self.scr_wheel_y != self.ptr_rect_up.bottom:
            self.scr_focus -= self.mouse_move * (1 / (SCR_HEIGHT / self.y_val))
        if self.keys[pygame.K_UP]:
            self._scroll_up_down(True)
        if self.keys[pygame.K_DOWN]:
            self._scroll_up_down(False)
        
        self.mouse_move = mods.special_calcualation(self.mouse_move, 0, .000000001)
    
    def _load_timer(self, timer: int):
        if self.start_blitting_timer >= timer:
            self.start_blitting_timer = 0
            self.start_blitting = True
        else:
            self.start_blitting_timer += 1
    
    def _randomize_load_timer(self):
        self.loading_timer = random.randint(100, 700)
    
    # Server multiplayer section
    def _server_multiplayer__blitting(self):
        self.multiplayer_b_buton.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_was_clicked, on_click=self._exit_button_was_pressed, color=self.FG_COLOR)
        self.controller_opts = CONTROL_OPTIONS[0], CONTROL_OPTIONS[2]
        self.next_update = False
        if self.in_next_update:
            self.mp_back_button.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_was_clicked, on_click=self._exit_button_was_pressed)
            
            self.user_name_prompt.activate_label(self.mouse_rect, self.mouse_was_clicked, self.mouse_rel)
            
            self.user_name_tv.activate_text_view(self.mouse_rect, self.mouse_was_clicked)
            self.join_button.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_was_clicked)
            self.host_button.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_was_clicked)
        else:
            self.screen.blit(self.coming_soon_surf, self.coming_soon_rect)
    
    # BT multiplayer section
    def _stop_bt_mult_game(self, mult_scr=True):
        self.started = False
        self.multiplayer_scr = mult_scr
        self.multiplayer_scr_bt = False
        self.multiplayer_scr_serv = False
        self.opponent_addr = None
        self.customised = False
        self.authenticated = False
        self.failed_auth = False
        self.bt_is_not_on = False
        self.searched = False
        self.start_blitting = False
        self.continue_drawing_button = True
        self.exitting_mult_game = 'true'
        
        self.apply_settings_changes = True
        self._save_and_apply_settings()
    
    def _search_for_bt(self):
        try:
            if self.do_once:
                def bt_search():
                    try:
                        b_address_info = bt.discover_devices(lookup_names=True)
                        ble_address_info = [(i.address, i.name) for i in asyncio.run(self.scanner.discover())]
                        
                        self.bt_address_info = mods.list_intersect(b_address_info, ble_address_info)
                    except OSError:
                        self.bt_is_not_on = True
                    
                    if self.bt_is_not_on:
                        self.searched = True
                        self.do_once = False
                        return
                    
                    self.addresses = []
                    
                    for key, clickable_texts in enumerate(self.bt_address_info):
                        ct = ClickableText(
                                        self.screen,
                                        f'{clickable_texts[1] if clickable_texts[1] else '_'} : {clickable_texts[0]}',
                                        FONT3,
                                        self.FG_COLOR,
                                        self.BG_COLOR,
                                        (
                                            130,
                                            (FONT3.render(f'{clickable_texts[1]} : {clickable_texts[0]}', False, self.FG_COLOR).get_height() + self.bt_addr_offset_val) * key + self.bt_addr_y_pos
                                        ),
                                        sound_info=self.button_sound_info,
                                        )
                        sn = FONT3.render(f'{key + 1}.', False, self.FG_COLOR)
                        sn_rect = sn.get_rect(midright=(ct.hover_rect.left - 30 , ct.hover_rect.centery))
                        
                        bt_info = (ct, (sn, sn_rect))
                        
                        if bt_info not in self.addresses:
                            self.addresses.append(bt_info)
                    
                    self.searched = True

                self.start_bt_search = thread.Thread(target=bt_search)
                self.start_bt_search.daemon = True
                self.start_bt_search.start()
                
                self.do_once = False
            
            if self.bt_is_not_on:
                return
        except Exception:
            return
    
    def _find_and_assign_bt_opponent__blitting(self):
        self.bt_info_font = mods.make_font(2, 30)
        self.bt_addr_y_pos = 130
        
        if not self.searched:
            self._search_for_bt()
        
        if not self.start_bt_search.is_alive():
            self.do_once = True
            self._search_for_bt()
        
        if self.searched:
            if not self.bt_is_not_on:
                self.multiplayer_b_buton.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_was_clicked, on_click=self._exit_button_was_pressed, color=self.FG_COLOR)
                
                self.bt_lists_title_surf = mods.make_font(1, 50).render('Bluetooth Lobby', False, self.FG_COLOR)
                self.bt_lists_title_rect = self.bt_lists_title_surf.get_rect(center=(SCR_WIDTH / 2, self.bt_lists_title_surf.get_height()))
                
                self.screen.blit(self.bt_lists_title_surf, self.bt_lists_title_rect)
                    
                for key, bt_info in enumerate(self.addresses):
                    ct, nums = bt_info
                    def assign_bt_opponent():
                        self.opponent_addr = self.bt_address_info[key][0]
                    
                    ct.activate_text(self.mouse_rect, self.mouse_was_clicked, assign_bt_opponent)
                    self.screen.blit(*nums)
            else:
                self._bt_multiplayer_bt_is_not_on__blitting()
                self.exit_failed_scr_button.activate_button(self.mouse_rect, self.mouse_was_clicked, on_click=self._stop_bt_mult_game, color=(self.FG_COLOR, self.BG_COLOR))
        else:
            self.loading_scr('Loading')
    
    def _bt_authenticate(self, opponent_addr: str):
        bluetooth_address = opponent_addr
        key_send = 'Ifechukwu is the oga and there is nothing anyone can do about that'
        
        with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as s:
            try:
                s.connect((bluetooth_address, 2))
                
                s.send(key_send.encode())
                key_recv = s.recv(1024).decode()
                
                if key_recv == key_send:
                    self.authenticated = True
                    self.load_scr = True
                    self.failed_auth = False
                    self.continue_drawing_button = False
                    self.exitting_mult_game = 'false'
                else:
                    self.retry_timer += 1
                
                if self.retry_timer >= 4:
                    self.authenticated = False
                    self.failed_auth = True
                    return
            
            except (TimeoutError, OSError):
                self.authenticated = False
                self.failed_auth = True
    
    def _bt_get_info(self, opponent_addr: str):
        bluetooth_address = opponent_addr
        all_info = '\
            {\
                "movement": ' + str((self.player1_up, self.player1_down)) + ',\
                "color": ' + self.FG_COLOR +',\
                "mouse_pos": ' + str((self.mouse_rect.x, self.mouse_rect.y)) +',\
                "exitting": ' + self.exitting_mult_game +'\
            }'

        with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as s:
            s.connect((bluetooth_address, 2))
            
            if self.authenticated:
                s.send(all_info)
                self.info = json.loads(s.recv(1024).decode())
                
                if self.info['exitting']:
                    self._stop_bt_mult_game()
                    return
    
    def _bt_multiplayer_failed__blitting(self):
        failed_surf1 = mods.make_font(2, 30).render('Failed to Authenticate', False, self.FG_COLOR)
        failed_surf2 = mods.make_font(2, 30).render('The problem might come from choosing the wrong bluetooth address', False, self.FG_COLOR)
        
        failed_rect1 = failed_surf1.get_rect(center=(SCR_WIDTH / 2, (SCR_HEIGHT / 2) - (failed_surf1.get_height() / 2)))
        failed_rect2 = failed_surf2.get_rect(center=(SCR_WIDTH / 2, (SCR_HEIGHT / 2) + (failed_surf2.get_height() / 2)))
        
        self.screen.blit(failed_surf1, failed_rect1)
        self.screen.blit(failed_surf2, failed_rect2)
    
    def _bt_multiplayer__blitting(self):
        if self.opponent_addr is None:
            self._find_and_assign_bt_opponent__blitting()
        else:
            if not self.failed_auth:
                if not self.authenticated:
                    if not self.start_bt_check:
                        self.start_bt_check_timer += 1
                        if self.start_bt_check_timer >= 700:
                            self.start_bt_check_timer = 0
                            self.start_bt_check = True
                    
                    if self.start_bt_check:
                        bt_auth_info = thread.Thread(target=lambda: self._bt_authenticate(self.opponent_addr))
                        bt_auth_info.daemon = True
                        bt_auth_info.start()
                        self.start_bt_check = False
                    
                    self.loading_scr('Authenticating')
                else:
                    self._bt_get_info(self.opponent_addr)
                    self.started = True
                    self.multiplayer_scr = False
                    self.load_scr = False
                    self.multiplayer_scr_serv = False
                    self.multiplayer_scr_bt = False
                    self.continue_drawing_button = False
                    self.start_blitting = False
            else:
                self._bt_multiplayer_failed__blitting()
                self.exit_failed_scr_button.activate_button(self.mouse_rect, self.mouse_was_clicked, on_click=lambda: self._stop_bt_mult_game(False), color=(self.FG_COLOR, self.BG_COLOR))
    
    def _bt_multiplayer_bt_is_not_on__blitting(self):
        bt_not_on_info1 = self.bt_info_font.render('Bluetooth address scan failed', False, self.FG_COLOR)
        bt_not_on_info2 = self.bt_info_font.render('Either blutooth is not turned on or there was an error during the scan', False, self.FG_COLOR)
        
        bt_not_on_info_rect1 = bt_not_on_info1.get_rect(center=(SCR_WIDTH / 2, (SCR_HEIGHT / 2) - bt_not_on_info1.get_height()))
        bt_not_on_info_rect2 = bt_not_on_info2.get_rect(center=(SCR_WIDTH / 2, (SCR_HEIGHT / 2) + bt_not_on_info2.get_height()))
        
        self.screen.blit(bt_not_on_info1, bt_not_on_info_rect1)
        self.screen.blit(bt_not_on_info2, bt_not_on_info_rect2)
    
    
    def permission_error_scr(self):
        self.apply_settings_changes = False
        self.mouse_y_speed = False
        self.rect_assigned = False
        self.started = False
        self.settings_disabled = False
        self.start_blitting = False
        self.continue_drawing_button = False
        self.changed_ctrl_state = False
        self.mouse_pressed = False
        self.paused_scr = False
        self.settings_scr = False
        self.info_scr = False
        self.stats_scr = False
        self.multiplayer_scr = False
        self.write_to_file = False
        self.init_once = False
        
        info_up = FONT3.render('It seems like we do not have enough permissions to write to certain files.', False, self.FG_COLOR)
        info_middle = FONT3.render('Restart the game in administrator mode for it to work properly.', False, self.FG_COLOR)
        info_down = FONT3.render('I could ask for permissions everytime you start the game but it costs money, soo..yeah', False, self.FG_COLOR)
        
        info_rect_up = info_up.get_rect(center=(SCR_WIDTH / 2, info_up.get_height() - (SCR_HEIGHT / 2)))
        info_rect_middle = info_middle.get_rect(center=(SCR_WIDTH / 2, SCR_HEIGHT / 2))
        info_rect_down = info_up.get_rect(center=(SCR_WIDTH / 2, info_down.get_height() + (SCR_HEIGHT / 2)))
        
        self.screen.blit(info_up, info_rect_up)
        self.screen.blit(info_middle, info_rect_middle)
        self.screen.blit(info_down, info_rect_down)
        
        self.permission_button.activate_button(self.mouse_rect, self.mouse_was_clicked, on_click=lambda: self._save_and_exit(True))
    
    def loading_scr(self, info: str):
        self.load_timer += 1
        if self.load_timer % 50 == 0:
            self.load_dot_amount += 1
            self.load_timer = 1
        if self.load_dot_amount > 5:
            self.load_dot_amount = 1
        
        load_surf = mods.make_font(2, 30).render(f'{info}{'.' * self.load_dot_amount}', False, self.FG_COLOR)
        load_rect = load_surf.get_rect(center=(SCR_WIDTH / 2, SCR_HEIGHT / 2))
        
        self.screen.blit(load_surf, load_rect)
    
    
    def multiplayer(self):
        if self.start_blitting:
            self.settings(True)
        else:
            self.continue_drawing_button = False
            self.loading_timer = 100
            self.loading_scr('Please wait')
            self._load_timer(self.loading_timer)
    
    def game_play(self):
        self.play_timer = (int(pygame.time.get_ticks() / 1000)-self.start_time) - self.time_not_played
        
        self.started_timing = False
        self.write_to_file = True
        
        ball_rect = self.ball.get_rect()
        player1_rect = self.player1.get_rect_vals()
        player2_rect = self.player2.get_rect_vals()
        self.player2_score, self.player1_score = self.ball.get_score()
        
        mods.draw_nums(self.player1_score, SCR_WIDTH, 0, FONT_CELL_SIZE, self.screen, col=self.FG_COLOR, left=True, img=self.ui_img if self.load_skin_ui else None)
        mods.draw_nums(self.player2_score, SCR_WIDTH, 0, FONT_CELL_SIZE, self.screen, col=self.FG_COLOR, left=False, img=self.ui_img if self.load_skin_ui else None)
        
        self.ball.update(BALL_SPEED*self.delta_time, *(player1_rect, player2_rect), col=self.FG_COLOR, skin=self.ball_skin_path if self.load_skin_ball else 'none')
        self.player1.update(self.p1_control, [ball_rect, self.ball.ball_x_pos], True, self.mouse, speed=(PLAYER_SPEED*self.delta_time), col=self.FG_COLOR, ai_difficulty=self.ai_difficulty, skin=self.player_skin_path if self.load_skin_player else 'none', up=self.player1_up, down=self.player1_down)
        
        if self.authenticated:
            up, down = self.info['movement']
            mouse = self.info['mouse']
            color = self.info['color']
            self.player2.update(self.p2_control, [ball_rect, self.ball.ball_x_pos], False, mouse, speed=(PLAYER_SPEED*self.delta_time), col=color, ai_difficulty=self.ai_difficulty, skin=self.player_skin_path if self.load_skin_player else 'none', up=up, down=down)
        else:
            self.player2.update(self.p2_control, [ball_rect, self.ball.ball_x_pos], False, self.mouse, speed=(PLAYER_SPEED*self.delta_time), col=self.FG_COLOR, ai_difficulty=self.ai_difficulty, skin=self.player_skin_path if self.load_skin_player else 'none', up=self.player2_up, down=self.player2_down)
            
        spacing = LINE_SPACE
        
        for _ in range(SCR_HEIGHT//LINE_LEN):
            l_x_pos = SCR_WIDTH/2 - (LINE_WIDTH / 2)
            if self.load_skin_ui:
                self.screen.blit(pygame.transform.scale(self.ui_img, (LINE_WIDTH, LINE_LEN)), (l_x_pos, spacing))
            else:
                pygame.draw.line(self.screen, self.FG_COLOR, (l_x_pos, spacing), (l_x_pos, spacing + LINE_LEN), LINE_WIDTH)
                
            spacing += LINE_LEN + LINE_SPACE
        
        self.screen.blit(FONT2.render(self.controller_opts[self.pc1_index], False, self.FG_COLOR), (len(self.controller_opts[self.pc1_index]), SCR_HEIGHT-FN2_SIZE*2))
        self.screen.blit(FONT2.render(self.controller_opts[self.pc2_index], False, self.FG_COLOR), (SCR_WIDTH-(FN2_SIZE*len(self.controller_opts[self.pc2_index])+FN2_SIZE+3), SCR_HEIGHT-FN2_SIZE*2))
    
    def pause(self):
        if self.write_to_file:
            try:
                with open(STATS_DIR, 'w') as file:
                    self.stats_val['player one high score'] = max(self.stats_val['player one high score'], self.player1_score)
                    self.stats_val['player two high score'] = max(self.stats_val['player two high score'], self.player2_score)
                    self.stats_val['highest play time'] = max(self.stats_val['highest play time'], self.play_time)
                    
                    self.pohs = self.stats_val['player one high score']
                    self.pths = self.stats_val['player two high score']
                    self.hpt = mods.secs_to_time(self.stats_val['highest play time'])
                    
                    new_stats = json.dumps(self.stats_val, indent=2)
                    file.write(new_stats)
                    self.permission_error = False
            except PermissionError:
                self.permission_error = True
            
            self.write_to_file = False
        
        self.pause_outline = pygame.Rect(self.pause_text_rects[self.paused_rects[self.pause_focus]].x - EXIT_SPACE_OFFSET//2,
                                        self.pause_text_rects[self.paused_rects[self.pause_focus]].y,
                                        self.pause_texts[self.paused_rects[self.pause_focus]].get_width() + EXIT_SPACE_OFFSET,
                                        self.pause_texts[self.paused_rects[self.pause_focus]].get_height())
        
        pygame.draw.rect(self.screen, self.FG_COLOR, self.pause_outline, FOCUS_RECT_WIDTH, BORDER_RAD, BORDER_RAD, BORDER_RAD, BORDER_RAD, BORDER_RAD)
        
        self.screen.blit(FONT1.render('Game Paused', False, self.FG_COLOR), (mods.position(SCR_WIDTH, 'center', 'Game Paused', 57//2.2), 40))
        
        for i in [k for k, _ in self.pause_texts.items()]:
            self.screen.blit(self.pause_texts[i], self.pause_text_rects[i])
    
    def information(self):
        if self.in_stats_or_help:
            self.scr_focus = 0
            self.scr_wheel_y = self.ptr_rect_up.bottom
            self.in_stats_or_help = False
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                self.mouse_move = event.dict['precise_y']
        
        self.y_val = 70
        self.vals, self.surf, self.list_val, _ = mods.multiline_write(HELP_INFO, FONT3, self.link_color, self.FG_COLOR)
        
        self.screen.blit(FONT1.render('Information', False, self.FG_COLOR), pygame.Rect(mods.position(SCR_WIDTH, 'center', 'IFEs Pong', FN1_SIZE), -50+mods.clamp(self.y_val-self.scr_focus, self.y_val, -(FN3_SIZE+TXT_PAD)), 0, 0))
        
        end_of_scr = ((len(HELP_INFO.split('\n')) + 2) * FN3_SIZE) * SCROLL_WEIGHT

        self.scr_focus = pygame.math.clamp(self.scr_focus, 0, end_of_scr)
        
        self.scr_wheel_y = mods.clamp(self.scr_wheel_y, (self.ptr_rect_down.top - self.info_scr_wheel_height) + 1, self.ptr_rect_up.bottom)
        self.scr_wheel_rect = pygame.Rect(self.ptr_u_d_x, self.scr_wheel_y, self.ptr_u_d_width, self.info_scr_wheel_height)
        
        self.info_scroll_wheel.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_was_clicked, pos=(self.scr_wheel_rect.x, self.scr_wheel_rect.y), color=self.FG_COLOR)
        
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
                pygame.draw.line(self.screen, self.FG_COLOR, (x, y + FN3_SIZE*2.5), (x + self.txt_width, y + FN3_SIZE*2.5), 1)

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

        self.ptr_up.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_was_clicked, on_click=lambda: self._scroll_up_down(True), no_bounce=True, color=self.FG_COLOR)
        self.ptr_down.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_was_clicked, on_click=lambda: self._scroll_up_down(False), no_bounce=True, color=self.FG_COLOR)
        
        self._scroll()
        
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
        if self.in_next_update:
            stats_info = gc.all_stats(self.pohs, self.pths, ltsp=self.hpt)
            
            self.ptr_rect_up = pygame.Rect(self.ptr_u_d_x, self.ptr_u_y, self.ptr_u_d_width, self.ptr_u_d_height)
            self.ptr_rect_down = pygame.Rect(self.ptr_u_d_x, self.ptr_d_y, self.ptr_u_d_width, self.ptr_u_d_height)
            
            if self.in_stats_or_help:
                self.scr_focus = 0
                self.scr_wheel_y = self.ptr_rect_up.bottom
                self.in_stats_or_help = False
            
            self.y_val = 70
            self.vals, self.surf, self.list_val, _ = mods.multiline_write(stats_info, FONT3, self.link_color, self.FG_COLOR)
            
            self.screen.blit(FONT1.render('Statistics', False, self.FG_COLOR), pygame.Rect(mods.position(SCR_WIDTH, 'center', 'Statistics', FN1_SIZE), -50 + mods.clamp(self.y_val-self.scr_focus, self.y_val, -(FN3_SIZE+TXT_PAD)), 0, 0))
            
            self.scr_focus = max(self.scr_focus, 0)
            
            self.scr_wheel_y = mods.clamp(self.scr_wheel_y, (self.ptr_rect_down.top - self.stats_scr_wheel_height) + 1, self.ptr_rect_up.bottom)
            self.scr_wheel_rect = pygame.Rect(self.ptr_u_d_x, self.scr_wheel_y, self.ptr_u_d_width, self.stats_scr_wheel_height)
            
            self.stats_scroll_wheel.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_was_clicked, pos=(self.scr_wheel_rect.x, self.scr_wheel_rect.y), color=self.FG_COLOR)
            
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

            self.ptr_up.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_was_clicked, on_click=lambda: self._scroll_up_down(True), no_bounce=True, color=self.FG_COLOR)
            self.ptr_down.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_was_clicked, on_click=lambda: self._scroll_up_down(False), no_bounce=True, color=self.FG_COLOR)
            
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
        else:
            self.screen.blit(self.coming_soon_surf, self.coming_soon_rect)
        
    def settings(self, multiplayer=False):
        if multiplayer:
            self._draw_bg()
            self.multiplayer_b_buton.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_was_clicked, on_click=self._exit_button_was_pressed, color=self.FG_COLOR)
            self.controller_opts = CONTROL_OPTIONS[0], CONTROL_OPTIONS[2]
            self.pc1_index = pygame.math.clamp(self.pc1_index, 0, 1)
        
        if not multiplayer:
            self.warnig_surf = mods.make_font(2, 10).render('Changes made will reset the game', False, self.BG_COLOR)
        
            if self.init_once:
                self._init_text_view()
                self._init_other_widgets_in_settings()
                self.init_once = False
            
        height = 55
        x = height
        width = SCR_WIDTH - (x * 2)
        
        self.settings_background = pygame.Rect(
                                          x,
                                          self.setting_text_rects[self.setting_rects[self.setting_focus]].y - Y_OPTION_SPACE_OFFSET/2,
                                          width,
                                          height
                                          )
        
        if self.load_skin_ui:
            self.screen.blit(pygame.transform.scale(self.action_ui_img, (self.settings_background.width, self.settings_background.height)), (self.settings_background.x, self.settings_background.y))
        
        if not multiplayer:
            self.is_index_changed = (((self.saved_data['ad_index'] != self.ad_index) and (f'{self.setting_rects[self.setting_focus]} opt' == self.ai_key_opt)) or
                                ((self.saved_data['pc1_index'] != self.pc1_index) and (f'{self.setting_rects[self.setting_focus]} opt' == self.p1c_key_opt))or
                                ((self.saved_data['pc2_index'] != self.pc2_index) and (f'{self.setting_rects[self.setting_focus]} opt' == self.p2c_key_opt)))
            
            self.tv_bg_color = self.FG_COLOR
            self.tv_fg_color = self.FG_COLOR
            self.aid_color = self.FG_COLOR
            self.p1_color = self.FG_COLOR
            self.p2_color = self.FG_COLOR
            self.pob_color = self.FG_COLOR
            self.ptb_color = self.FG_COLOR
        else:
            self.is_index_changed = True
            self.tv_bg_color = self.FG_COLOR
            self.tv_fg_color = self.FG_COLOR
            self.p1_color = self.FG_COLOR
            self.pob_color = self.FG_COLOR
            self.mpo_color = self.FG_COLOR
        
        mini_win_bg_color = mods.set_color(self.BG_COLOR, 200) if self.BG_COLOR not in ('black', [0, 0, 0], [0, 0, 0, 0], (0, 0, 0), (0, 0, 0, 0)) else 'grey20'

        pygame.draw.rect(self.screen, self.FG_COLOR, self.settings_background)
        
        for i in self.setting_texts.keys():
            if f'{self.setting_rects[self.setting_focus]} opt' not in i:
                self.screen.blit(self.setting_texts[i], self.setting_text_rects[i])
        
        match self.setting_rects[self.setting_focus]:
            case self.bg_key:
                self.tv_bg_color = self.BG_COLOR
                self.bg_txt_view_input = self.bg_input.partial_activate_text_view(mouse_rect=self.mouse_rect, fg_color=self.tv_bg_color)
            
            case self.fg_key:
                self.tv_fg_color = self.BG_COLOR
                self.fg_txt_view_input = self.fg_input.partial_activate_text_view(mouse_rect=self.mouse_rect, fg_color=self.tv_fg_color)
            
            case self.p1c_key:
                self.p1_color = self.BG_COLOR
                if multiplayer:
                    self.p1_control, self.pc1_index = self.p1_control_selector.activate_selector(self.mouse_rect, self.mouse_was_clicked, pos=self.setting_text_rects[self.p1c_key_opt].topleft, color=self.p1_color, options=(CONTROL_OPTIONS[0], CONTROL_OPTIONS[2]))
                else:
                    self.p1_control, self.pc1_index = self.p1_control_selector.activate_selector(self.mouse_rect, self.mouse_was_clicked, color=self.p1_color)
                    self.warning_indexes_pos = (
                            self.p1_control_selector.text_rect.centerx,
                            self.settings_background.bottom - self.warnig_surf.get_height()
                        )
            
            case self.p2c_key:
                if not multiplayer:
                    self.p2_color = self.BG_COLOR
                    self.p2_control, self.pc2_index = self.p2_control_selector.activate_selector(self.mouse_rect, self.mouse_was_clicked, color=self.p2_color)
                    self.warning_indexes_pos = (
                        self.p2_control_selector.text_rect.centerx,
                        self.settings_background.bottom - self.warnig_surf.get_height()
                        )
            
            case self.ai_key:
                if not multiplayer:
                    self.aid_color = self.BG_COLOR
                    self.ai_difficulty, self.ad_index = self.ai_difficulty_selector.activate_selector(self.mouse_rect, self.mouse_was_clicked, color=self.aid_color)
                    self.warning_indexes_pos = (
                            self.ai_difficulty_selector.text_rect.centerx,
                            self.settings_background.bottom - self.warnig_surf.get_height()
                            )
                
            case self.pob_key:
                self.pob_color = self.BG_COLOR
                if self.pob_focus == 1:
                    self.screen.blit(self.setting_texts[self.pob_down_key_opt], self.setting_text_rects[self.pob_down_key_opt])
                    self.player1_up_txt_view_input, self.player1_up = self.pob_up_input.activate_input_selector(self.mouse_rect,
                                                                                                                self.mouse_was_clicked,
                                                                                                                self.mouse_rel,
                                                                                                                self.pob_color,
                                                                                                                mini_win_bg_color,
                                                                                                                self.FG_COLOR)
                
                elif self.pob_focus == 2:
                    self.screen.blit(self.setting_texts[self.pob_up_key_opt], self.setting_text_rects[self.pob_up_key_opt])
                    self.player1_down_txt_view_input, self.player1_down = self.pob_down_input.activate_input_selector(self.mouse_rect,
                                                                                                                      self.mouse_was_clicked,
                                                                                                                      self.mouse_rel,
                                                                                                                      self.pob_color,
                                                                                                                      mini_win_bg_color,
                                                                                                                      self.FG_COLOR)

            case self.ptb_key:
                if not multiplayer:
                    self.ptb_color = self.BG_COLOR
                    if self.ptb_focus == 1:
                        self.screen.blit(self.setting_texts[self.ptb_down_key_opt], self.setting_text_rects[self.ptb_down_key_opt])
                        self.player2_up_txt_view_input, self.player2_up = self.ptb_up_input.activate_input_selector(self.mouse_rect,
                                                                                                                    self.mouse_was_clicked,
                                                                                                                    self.mouse_rel,
                                                                                                                    self.ptb_color,
                                                                                                                    mini_win_bg_color,
                                                                                                                    self.FG_COLOR,)
                    
                    elif self.ptb_focus == 2:
                        self.screen.blit(self.setting_texts[self.ptb_up_key_opt], self.setting_text_rects[self.ptb_up_key_opt])
                        self.player2_down_txt_view_input, self.player2_down = self.ptb_down_input.activate_input_selector(self.mouse_rect,
                                                                                                                      self.mouse_was_clicked,
                                                                                                                      self.mouse_rel,
                                                                                                                      self.ptb_color,
                                                                                                                      mini_win_bg_color,
                                                                                                                      self.FG_COLOR)

            case self.mpo_key:
                self.mpo_color = self.BG_COLOR
                self.mpo, _ = self.mpo_selector.activate_selector(self.mouse_rect, self.mouse_was_clicked, color=self.mpo_color)
            
        if not multiplayer:
            if self.is_index_changed:
                self.warning_indexes_rect = self.warnig_surf.get_rect(midtop=(self.warning_indexes_pos))
                self.screen.blit(self.warnig_surf, self.warning_indexes_rect)
        
        self.settings_disabled = self.ptb_up_input.mini_win.isactive() or self.ptb_down_input.mini_win.isactive() or self.pob_up_input.mini_win.isactive() or self.pob_down_input.mini_win.isactive()
        self.saa_button.disabled = self.settings_disabled
        
        if multiplayer:
            def _mult_save_and_apply():
                self._save_and_apply_settings()
                self.multiplayer_scr = False
                if self.mpo == 'Bluetooth':
                    self.multiplayer_scr_bt = True
                    self.multiplayer_scr_serv = False
                    
                elif self.mpo == 'Server':
                    self.multiplayer_scr_bt = False
                    self.multiplayer_scr_serv = True
                
            self.saa_button.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_was_clicked, on_click=_mult_save_and_apply, color=(self.FG_COLOR, self.BG_COLOR), text="Let's be going")
        else:
            self.saa_button.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_was_clicked, on_click=self._save_and_apply_settings, color=(self.FG_COLOR, self.BG_COLOR), text='Save and apply')
    
    
    def update(self):
        self._draw_bg()
    	
        self.mouse = pygame.mouse.get_pos()
        m_x, m_y = self.mouse
        self.mouse_rect = pygame.Rect(m_x, m_y, 1, 1)
        self.mouse_was_clicked = pygame.mouse.get_pressed()[0]
        
        if self.authenticated:
            self._bt_get_info(self.opponent_addr)
            self.bt_exit_button.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_was_clicked, on_click=self._stop_bt_mult_game, color=self.FG_COLOR)
        else:
            if not self.multiplayer_scr and not self.multiplayer_scr_bt and not self.multiplayer_scr_serv:
                if not self.rect_assigned:
                    rect_div = pygame.Rect(ICON_POS, ICON_POS, ICON_SIZE * FN2_SIZE, ICON_SIZE * FN2_SIZE)
                    self.action_button_bg = pygame.Rect(rect_div.x - (BG_OFFSET/2), rect_div.y - (BG_OFFSET/2), rect_div.width + BG_OFFSET, rect_div.height + BG_OFFSET)
                    if self.load_skin_ui:
                        self.action_ui_img = pygame.transform.scale(self.ui_img, (self.action_button_bg.width, self.action_button_bg.height))
                    
                    self.rect_assigned = True
                self.controller_opts = CONTROL_OPTIONS
                self.back_button.disabled = self.settings_disabled
                if self.continue_drawing_button:
                    self.back_button.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_was_clicked, on_click=self._exit_button_was_pressed, color=self.FG_COLOR)
                if self.load_skin_ui:
                    self.screen.blit(self.action_ui_img, self.action_button_bg)
            
        self.delta_time = self.clock.tick(FPS)
        self.play_time = round(time.time() - self.t1)
        
        self.option_txt_colors = mods.set_color(self.FG_COLOR, 180)
        
        self.link_color = mods.set_color(self.FG_COLOR,  105)
        
        self.pause_texts = {
            'Resume': mods.font_renderer('Resume', FONT3, self.option_txt_colors),
            'Information': mods.font_renderer('Information', FONT3, self.option_txt_colors),
            'Settings': mods.font_renderer('Settings', FONT3, self.option_txt_colors),
            'Statistics': mods.font_renderer('Statistics', FONT3, self.option_txt_colors),
            'Main menu': mods.font_renderer('Main menu', FONT3, self.option_txt_colors),
            'Restart': mods.font_renderer('Restart', FONT3, self.option_txt_colors), 
            'Exit': mods.font_renderer('Exit', FONT3, self.option_txt_colors),
        }
        self.pause_text_rects = {
            'Resume': mods.font_rect_renderer('Resume', FN3_SIZE,y_offset=PAUSE_TEXT_START_POS, x_offset= X_PAUSE_TEXT_OFFSET),
            'Settings': mods.font_rect_renderer('Settings', FN3_SIZE, y_offset=PAUSE_TEXT_START_POS + PAUSE_TEXT_SPACING, x_offset= -X_PAUSE_TEXT_OFFSET),
            'Information': mods.font_rect_renderer('Information', FN3_SIZE,y_offset=PAUSE_TEXT_START_POS + PAUSE_TEXT_SPACING*2, x_offset= X_PAUSE_TEXT_OFFSET),
            'Statistics': mods.font_rect_renderer('Statistics', FN3_SIZE,y_offset=PAUSE_TEXT_START_POS + PAUSE_TEXT_SPACING*3, x_offset= -X_PAUSE_TEXT_OFFSET),
            'Main menu': mods.font_rect_renderer('Main menu', FN3_SIZE,y_offset=PAUSE_TEXT_START_POS + PAUSE_TEXT_SPACING*4, x_offset= X_PAUSE_TEXT_OFFSET),
            'Restart': mods.font_rect_renderer('Restart', FN3_SIZE, y_offset=PAUSE_TEXT_START_POS + (PAUSE_TEXT_SPACING*5), x_offset= -X_PAUSE_TEXT_OFFSET),
            'Exit': mods.font_rect_renderer(' Exit', FN3_SIZE, y_offset=PAUSE_TEXT_START_POS + (PAUSE_TEXT_SPACING*6))
        }
        
        if self.multiplayer_scr or self.multiplayer_scr_bt or self.multiplayer_scr_serv:
            if self.p1_control == 'AI':
                self.pc1_index = self.controller_opts.index('KEYS')
                self.p1_control = 'KEYS'
                self.changed_ctrl_state = True
        else:
            if self.started:
                if self.changed_ctrl_state:
                    self.pc1_index = self.controller_opts.index('AI')
                    self.p1_control = 'AI'
                    self.changed_ctrl_state = False
        
        
        self.setting_texts = {
            self.bg_key: mods.font_renderer(self.bg_key, FONT3, self.tv_bg_color),
            self.fg_key: mods.font_renderer(self.fg_key, FONT3, self.tv_fg_color),
            self.pob_key: mods.font_renderer(self.pob_key, FONT3, self.pob_color),
            self.ptb_key: mods.font_renderer(self.ptb_key, FONT3, self.ptb_color),
            self.ai_key: mods.font_renderer(self.ai_key, FONT3, self.aid_color),
            self.p1c_key: mods.font_renderer(self.p1c_key, FONT3, self.p1_color),
            self.p2c_key: mods.font_renderer(self.p2c_key, FONT3, self.p2_color),
            
            self.bg_opt_key: mods.font_renderer(self.bg_txt_view_input, FONT3, self.tv_bg_color),
            self.fg_opt_key: mods.font_renderer(self.fg_txt_view_input, FONT3, self.tv_fg_color),
            
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
        
        self.bg_t_v = self.setting_text_rects[self.bg_opt_key]
        self.fg_t_v = self.setting_text_rects[self.fg_opt_key]
        self.ai_t_v = self.setting_text_rects[self.ai_key_opt]
        self.p1c_t_v = self.setting_text_rects[self.p1c_key_opt]
        self.p2c_t_v = self.setting_text_rects[self.p2c_key_opt]
        self.puko1 = self.setting_text_rects[self.pob_up_key_opt]
        self.pdko1 = self.setting_text_rects[self.ptb_up_key_opt]
        self.puko2 = self.setting_text_rects[self.pob_down_key_opt]
        self.pdko2 = self.setting_text_rects[self.ptb_down_key_opt]
        self.paused_rects = [k for k, _ in self.pause_text_rects.items()]
        self.setting_rects = [k for k, _ in self.setting_text_rects.items()]

        self.new_pause_rects = [k for _, k in self.pause_text_rects.items()]

        self.mouse_rel = pygame.mouse.get_rel()
        self.use_mouse = self.mouse_rel != (0, 0)
        
        if self.permission_error:
            self.permission_error_scr()

    def game_event_loop(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self._save_and_exit()
        
        if self.start_blitting:
            if self.mouse_was_clicked:
                self.mouse_pressed = True
            
            self.keys = pygame.key.get_pressed()

            if event.type == pygame.KEYDOWN:
                if self.keys[pygame.K_ESCAPE]:
                    self._exit_button_was_pressed()
            
            if self.settings_scr:
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
                    for pause_widg_rect in self.new_pause_rects:
                        # click_area = pygame.Rect(
                        #                             pause_widg_rect.x - ((self.pause_outline.width - pause_widg_rect.width) / 2),
                        #                             pause_widg_rect.y - ((self.pause_outline.height - pause_widg_rect.height) / 2),
                        #                             self.pause_outline.width,
                        #                             self.pause_outline.height,
                        #                         )
                        if mods.isclicked(self.mouse_rect, pause_widg_rect, self.mouse_was_clicked, lambda: self._pause_mouse_func(pause_widg_rect)):
                            self._pause_actions(self.paused_rects[self.pause_focus])
                
                if self.settings_scr:
                    for i in self.setting_option_background_rects:
                        mods.isclicked(self.mouse_rect, i, self.mouse_was_clicked, lambda: self._setting_mouse_func(i))
                else:
                    self.setting_focus = 0
                
                self.pob_focus
                if event.type == pygame.KEYDOWN:
                    if self.paused_scr:
                        last_widg_index = len(self.paused_rects) - 1
                        if self.keys[pygame.K_UP] and self.pause_focus != 0:
                            self.widg_focused_sound.play()
                            self.pause_focus -= 1
                            self.use_mouse = False
                        elif self.keys[pygame.K_DOWN] and self.pause_focus != last_widg_index:
                            self.widg_focused_sound.play()
                            self.pause_focus += 1
                            self.use_mouse = False
                            
                        if self.keys[pygame.K_RETURN]:
                            self._pause_actions(self.paused_rects[self.pause_focus])
                    else:
                        if self.settings_scr:
                            last_opt_index = (len(self.setting_rects) -3 ) // 2
                            if self.keys[pygame.K_UP] and not self.settings_disabled and self.setting_focus != 0:
                                self.widg_focused_sound.play()
                                self.pob_focus = 1
                                self.ptb_focus = 1
                                self.temp = self.setting_focus
                                self.setting_focus -= 1
                                if self.temp != self.setting_focus:
                                    self.apply_settings_changes = True
                                
                                self._validate_text_view()
                            elif self.keys[pygame.K_DOWN] and not self.settings_disabled and self.setting_focus != last_opt_index:
                                self.widg_focused_sound.play()
                                self.pob_focus = 1
                                self.ptb_focus = 1
                                self.temp = self.setting_focus
                                self.setting_focus += 1
                                self.setting_focus = mods.clamp(self.setting_focus, (len(self.setting_rects)-3)//2, 0)
                                if self.temp != self.setting_focus:
                                    self.apply_settings_changes = True
                                
                                self._validate_text_view()
                            
                            match self.setting_rects[self.setting_focus]:
                                case self.pob_key:
                                    if not self.settings_disabled:
                                        if self.keys[pygame.K_LEFT]:
                                            self.pob_focus -= 1
                                            self.widg_focused_sound.play()
                                        elif self.keys[pygame.K_RIGHT]:
                                            self.pob_focus += 1
                                            self.widg_focused_sound.play()
                                        self.pob_focus = mods.clamp(self.pob_focus, 2, 1)
                                    
                                    if self.keys[pygame.K_RETURN]:
                                        self.widg_clicked_sound.play()
                                case self.ptb_key:
                                    if not self.settings_disabled:
                                        if self.keys[pygame.K_LEFT]:
                                            self.ptb_focus -= 1
                                            self.widg_focused_sound.play()
                                        elif self.keys[pygame.K_RIGHT]:
                                            self.ptb_focus += 1
                                            self.widg_focused_sound.play()
                                        self.ptb_focus = mods.clamp(self.ptb_focus, 2, 1)
                                    
                                    if self.keys[pygame.K_RETURN]:
                                        self.widg_clicked_sound.play()
                                case _:
                                    if not self.settings_disabled:
                                        if self.keys[pygame.K_RETURN]:
                                            self._save_and_apply_settings()
    
    def game_main_loop(self):
        if self.start_blitting:
            if not self.authenticated:
                self.continue_drawing_button = True
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
        
        else:
            self.continue_drawing_button = False
            if not self.authenticated:
                self._randomize_load_timer()
            else:
                self.loading_timer = 200
            self.loading_scr('Loading')
            self._load_timer(self.loading_timer)
    
    
    def beginning_update(self):
        self._control_timer()
        
        self.main_title_surf = mods.make_font(4, 200).render('IFEs PONG', False, self.FG_COLOR)
        self.main_title_rect = self.main_title_surf.get_rect(center=(SCR_WIDTH / 2, self.main_title_surf.get_height() - (self.main_title_surf.get_height() / 4)))
        
        if self.is_a_new_game:
            self.start_texts = {
                'New Game': mods.font_renderer('New Game', FONT3, self.option_txt_colors),
                'Multiplayer': mods.font_renderer('Multiplayer', FONT3, self.option_txt_colors),
                'Exit': mods.font_renderer('Exit', FONT3, self.option_txt_colors),
            }
            self.start_text_rects = {
                'New Game': mods.font_rect_renderer('New Game', FN3_SIZE, y_offset=(self.main_title_rect.bottom) + START_TEXT_START_POS + START_TEXT_Y_SPACE_OFFSET, x_offset=START_X_SPACING_OFFSET),
                'Multiplayer': mods.font_rect_renderer('Mulplayer', FN3_SIZE, y_offset=(self.main_title_rect.bottom) + START_TEXT_START_POS + START_TEXT_SPACING + START_TEXT_Y_SPACE_OFFSET, x_offset=-START_X_SPACING_OFFSET),
                'Exit': mods.font_rect_renderer('Exit', FN3_SIZE, y_offset=(self.main_title_rect.bottom) + START_TEXT_START_POS + START_TEXT_SPACING*2 + START_TEXT_Y_SPACE_OFFSET, x_offset=START_X_SPACING_OFFSET),
            }
        else:
            self.start_texts = {
                'Continue': mods.font_renderer('Continue', FONT3, self.option_txt_colors),
                'New Game': mods.font_renderer('New Game', FONT3, self.option_txt_colors),
                'Multiplayer': mods.font_renderer('Multiplayer', FONT3, self.option_txt_colors),
                'Exit': mods.font_renderer('Exit', FONT3, self.option_txt_colors),
                }
            self.start_text_rects = {
                'Continue': mods.font_rect_renderer('Continue', FN3_SIZE, y_offset=(self.main_title_rect.bottom) + START_TEXT_START_POS + START_TEXT_Y_SPACE_OFFSET, x_offset=START_X_SPACING_OFFSET),
                'New Game': mods.font_rect_renderer('New Game', FN3_SIZE, y_offset=(self.main_title_rect.bottom) + START_TEXT_START_POS + START_TEXT_SPACING + START_TEXT_Y_SPACE_OFFSET, x_offset=-START_X_SPACING_OFFSET),
                'Multiplayer': mods.font_rect_renderer('mulplayer', FN3_SIZE, y_offset=(self.main_title_rect.bottom) + START_TEXT_START_POS + START_TEXT_SPACING*2 + START_TEXT_Y_SPACE_OFFSET, x_offset=START_X_SPACING_OFFSET),
                'Exit': mods.font_rect_renderer('Exit', FN3_SIZE,y_offset=(self.main_title_rect.bottom) + START_TEXT_START_POS + START_TEXT_SPACING*3 + START_TEXT_Y_SPACE_OFFSET, x_offset=-START_X_SPACING_OFFSET),
            }

        self.rects_name = [k for k, _ in self.start_text_rects.items()]
        self.rects_rects = [k for _, k in self.start_text_rects.items()]
        
        if self.multiplayer_scr:
            self.setting_texts = {
                self.bg_key: mods.font_renderer(self.bg_key, FONT3, self.tv_bg_color),
                self.fg_key: mods.font_renderer(self.fg_key, FONT3, self.tv_fg_color),
                self.pob_key: mods.font_renderer(self.pob_key, FONT3, self.pob_color),
                self.p1c_key: mods.font_renderer(self.p1c_key, FONT3, self.p1_color),
                self.mpo_key: mods.font_renderer(self.mpo_key, FONT3, self.mpo_color),
                
                self.bg_opt_key: mods.font_renderer(self.bg_txt_view_input, FONT3, self.tv_bg_color),
                self.fg_opt_key: mods.font_renderer(self.fg_txt_view_input, FONT3, self.tv_fg_color),
                self.pob_up_key_opt: mods.font_renderer(f'Up: {self.player1_up_txt_view_input}', FONT3, self.pob_color),
                self.pob_down_key_opt: mods.font_renderer(f'Down: {self.player1_down_txt_view_input}', FONT3, self.pob_color),
                self.p1c_key_opt: mods.font_renderer(self.p1_control, FONT3, self.p1_color),
                self.mpo_opt: mods.font_renderer(self.mpo, FONT3, self.mpo_color)
                }
            self.setting_text_rects = {
                self.bg_key: mods.font_rect_renderer(self.bg_key, FN3_SIZE,y_offset=OPTION_TEXT_START_POS, x_offset= -X_OPTION_TEXT_OFFSET),
                self.fg_key: mods.font_rect_renderer(self.fg_key, FN3_SIZE,y_offset=OPTION_TEXT_START_POS + OPTION_TEXT_SPACING, x_offset= -X_OPTION_TEXT_OFFSET),
                self.pob_key: mods.font_rect_renderer(self.pob_up_key_opt, FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*2), x_offset= -X_OPTION_TEXT_OFFSET),
                self.p1c_key: mods.font_rect_renderer(self.p1c_key, FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*3), x_offset= -X_OPTION_TEXT_OFFSET),
                self.mpo_key: mods.font_rect_renderer(self.mpo_key, FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*4), x_offset= -X_OPTION_TEXT_OFFSET),
                
                self.bg_opt_key: mods.font_rect_renderer(self.bg_txt_view_input, FN3_SIZE,y_offset=OPTION_TEXT_START_POS, x_offset= X_OPTION_TEXT_OFFSET),
                self.fg_opt_key: mods.font_rect_renderer(self.fg_txt_view_input, FN3_SIZE,y_offset=OPTION_TEXT_START_POS + OPTION_TEXT_SPACING, x_offset= X_OPTION_TEXT_OFFSET),
                self.pob_up_key_opt: mods.font_rect_renderer(f'Up: {self.player1_up_txt_view_input}', FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*2), x_offset= X_OPTION_TEXT_OFFSET - FN3_SIZE*6),
                self.pob_down_key_opt: mods.font_rect_renderer(f'Down: {self.player1_down_txt_view_input}', FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*2), x_offset= X_OPTION_TEXT_OFFSET + FN3_SIZE*8.5),
                self.p1c_key_opt: mods.font_rect_renderer(self.p1_control, FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*3), x_offset= X_OPTION_TEXT_OFFSET),
                self.mpo_opt: mods.font_rect_renderer(self.mpo, FN3_SIZE, y_offset=OPTION_TEXT_START_POS + (OPTION_TEXT_SPACING*4), x_offset= X_OPTION_TEXT_OFFSET)
            }
            
            self.bg_t_v = self.setting_text_rects[self.bg_opt_key]
            self.fg_t_v = self.setting_text_rects[self.fg_opt_key]
            self.p1c_t_v = self.setting_text_rects[self.p1c_key_opt]
            self.puko1 = self.setting_text_rects[self.pob_up_key_opt]
            self.pdko1 = self.setting_text_rects[self.pob_down_key_opt]
            self.mpo_s_v = self.setting_text_rects[self.mpo_opt]
            
            self.setting_rects = [k for k, _ in self.setting_text_rects.items()]

        if self.permission_error:
            self.permission_error_scr()
    
    def beginning_event_loop(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self._save_and_exit(True)
        
        if self.start_blitting:
            self.keys = pygame.key.get_pressed()
            self.started_mouse_rel = pygame.mouse.get_rel()
            self.start_use_mouse = self.started_mouse_rel != (0, 0)
        
            if self.multiplayer_scr:
                if self.keys[pygame.K_ESCAPE] or mods.isclicked(self.mouse_rect, self.action_button_bg, self.mouse_was_clicked):
                    self.multiplayer_scr = False
                
                mods.isclicked(self.mouse_rect, self.setting_text_rects[self.pob_up_key_opt], self.mouse_was_clicked, lambda: self._pbo_mouse_func('pob', 1))
                mods.isclicked(self.mouse_rect, self.setting_text_rects[self.pob_down_key_opt], self.mouse_was_clicked, lambda: self._pbo_mouse_func('pob', 2))
                
                self.setting_option_background_rects = []
                
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
                
                for i in self.setting_option_background_rects:
                    mods.isclicked(self.mouse_rect, i, self.mouse_was_clicked, lambda: self._setting_mouse_func(i))

                if event.type == pygame.KEYDOWN:
                    last_opt_index = (len(self.setting_rects) -3 ) // 2
                    if self.keys[pygame.K_UP] and not self.settings_disabled and self.setting_focus != 0:
                        self.widg_focused_sound.play()
                        self.pob_focus = 1
                        self.temp = self.setting_focus
                        self.setting_focus -= 1
                        if self.temp != self.setting_focus:
                            self.apply_settings_changes = True
                        
                        self._validate_text_view()
                    elif self.keys[pygame.K_DOWN] and not self.settings_disabled and self.setting_focus != last_opt_index:
                        self.widg_focused_sound.play()
                        self.pob_focus = 1
                        self.temp = self.setting_focus
                        self.setting_focus += 1
                        self.setting_focus = mods.clamp(self.setting_focus, (len(self.setting_rects)-3)//2, 0)
                        if self.temp != self.setting_focus:
                            self.apply_settings_changes = True
                        
                        self._validate_text_view()
                    
                    match self.setting_rects[self.setting_focus]:
                        case self.pob_key:
                            if not self.settings_disabled:
                                if self.keys[pygame.K_LEFT]:
                                    self.pob_focus -= 1
                                    self.widg_focused_sound.play()
                                elif self.keys[pygame.K_RIGHT]:
                                    self.pob_focus += 1
                                    self.widg_focused_sound.play()
                                self.pob_focus = mods.clamp(self.pob_focus, 2, 1)
                            
                            if self.keys[pygame.K_RETURN]:
                                self.widg_clicked_sound.play()
                        case _:
                            if not self.settings_disabled:
                                if self.keys[pygame.K_RETURN]:
                                    self._save_and_apply_settings()

            if not self.multiplayer_scr and not self.multiplayer_scr_bt and not self.multiplayer_scr_serv:
                for i in self.rects_rects:
                    if mods.isclicked(self.mouse_rect, i, self.mouse_was_clicked, lambda: self._start_mouse_func(i)):
                        self._start_actions()
            
            if self.multiplayer_scr_bt:
                if self.keys[pygame.K_ESCAPE]:
                    self._exit_button_was_pressed()
            
            if event.type == pygame.KEYDOWN:
                main_multiplayer_scr = not self.multiplayer_scr and not self.multiplayer_scr_bt and not self.multiplayer_scr_serv
                end_of_widg_index = len(self.rects_name) - 1
                if main_multiplayer_scr:
                    if self.keys[pygame.K_RETURN]:
                        self._start_actions()
                   
                    if self.keys[pygame.K_UP] and self.start_focus != 0:
                        self.widg_focused_sound.play()
                        self.start_focus -= 1
                    if self.keys[pygame.K_DOWN] and self.start_focus != end_of_widg_index:
                        self.widg_focused_sound.play()
                        self.start_focus += 1
                else:
                    if self.keys[pygame.K_RETURN]:
                        self.apply_settings_changes = True
                        self._save_and_apply_settings()

    def started_main_scr(self):
        if self.start_blitting:
            self._draw_bg()
            self.continue_drawing_button = True

            start_outline = pygame.Rect(self.start_text_rects[self.rects_name[self.start_focus]].x - EXIT_SPACE_OFFSET//2,
                                        self.start_text_rects[self.rects_name[self.start_focus]].y,
                                        self.start_texts[self.rects_name[self.start_focus]].get_width() + EXIT_SPACE_OFFSET,
                                        self.start_texts[self.rects_name[self.start_focus]].get_height())
            
            pygame.draw.rect(self.screen, self.FG_COLOR, start_outline, FOCUS_RECT_WIDTH, BORDER_RAD, BORDER_RAD, BORDER_RAD, BORDER_RAD, BORDER_RAD)
            
            temp1_size = -10
            self.ifes_pong_pos = mods.position(SCR_WIDTH//2, 'center', 'IFES PONG', temp1_size),  mods.position(SCR_HEIGHT//2, 'center', ' ', temp1_size) + temp1_size
            
            self.screen.blit(self.main_title_surf, self.main_title_rect)
            
            for i in [k for k, _ in self.start_texts.items()]:
                self.screen.blit(self.start_texts[i], self.start_text_rects[i])
        else:
            self.continue_drawing_button = False
            self._randomize_load_timer()
            self.loading_scr('Loading')
            self._load_timer(self.loading_timer)
    
    def beginning_main_loop(self):
        if self.multiplayer_scr:
            self.multiplayer()
        elif self.multiplayer_scr_bt:
            self._bt_multiplayer__blitting()
        elif self.multiplayer_scr_serv:
            self._server_multiplayer__blitting()
        else:
            self.started_main_scr()

    
    def run(self):
        while True:
            self.update()
            
            if self.started:
                for event in pygame.event.get():
                    self.game_event_loop(event)
                
                if not self.permission_error:
                    self.game_main_loop()
            
            else:
                self.beginning_update()

                for event in pygame.event.get():
                    self.beginning_event_loop(event)
                
                if not self.permission_error:
                    self.beginning_main_loop()
            
            pygame.display.update()


@pyuac.main_requires_admin
def main():
    game = Game()
    game.run()

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


