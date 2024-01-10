
import sys
import json
import time
import math
import random
import socket
import webbrowser
import pygame
import asyncio
import bleak as bk
import bluetooth as bt
from pathlib import Path
import threading as thread
from utils.ui.ui_constants import *
import utils.helper_functions as mods
from utils.game.game_constants import *
from utils.game.game_components import Ball, Player
from utils.ui.ui_components import Button, Input, Selector, InputSeletor, ClickableText

class GameApp:
    def __init__(self):
        self._init_scr_()
        
        self._init_saved_values()
        
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
        
        self.main_menu_update()
        
        # Ever at all
        self.multiplayer_scr = False
        
        self._init_other_widgets_in_settings()
        
        self._init_serv_vars()
        
        self._init_info_scr_vars()
        
        self._init_pause_vars()
    
    def _init_scr_(self):
        pygame.init()
        
        self.screen = pygame.display.set_mode(SCR_SIZE)
        
        self.game_title = 'IFEs Pong'
        pygame.display.set_caption(self.game_title)

        logo = pygame.image.load(LOGO_PNG_PATH)
        pygame.display.set_icon(logo)
        self.clock = pygame.time.Clock()
        
        self.SCR_WIDTH = self.screen.get_width()
        self.SCR_HEIGHT = self.screen.get_height()
    
    def _init_global_bool_vars(self):
        self.apply_settings_changes = False
        self.started = False
        self.settings_disabled = False
        self.start_blitting = False
        self.changed_ctrl_state = False
        self.mouse_clicked_for_links = False
        self.paused_scr = False
        self.settings_scr = False
        self.info_scr = False
        self.multiplayer_scr = False
        self.init_once = True
    
    def _init_multiplayer_scr_vars(self):
        efsb_size = (200, 50)
        self.exit_failed_scr_button = Button(self.screen, self.FG_COLOR, ((self.SCR_WIDTH / 2) - (self.saa_size[0] / 2), (self.SCR_HEIGHT / 2) + self.saa_size[1] + 100), efsb_size, txt='Go Back', txt_color=self.BG_COLOR, sound_info=self.button_sound_info)
        
        self.multiplayer_scr_bt = False
        self.multiplayer_scr_serv = False
        self.scan_for_bt = True
        self.failed_auth = False
        self.start_bt_check = True
    
    def _init_characters(self):
        self.player1 = Player(self.screen, (P1_START_POS, self.SCR_HEIGHT / 2), PLAYER_SIZE, True)
        self.player2 = Player(self.screen, (self.SCR_WIDTH - EDGE_SPACE - PLAYER_SIZE[0], self.SCR_HEIGHT / 2), PLAYER_SIZE, False)
        self.ball = Ball(self.screen, (self.SCR_WIDTH / 2, self.SCR_HEIGHT / 2), BALL_RADIUS, (random.choice([1, -1]), random.choice([1, -1])))
    
    def _init_settings_vars(self):
        self.ai_difficulty = AI_DIFFICULTY_OPTIONS[self.ad_index]
        
        self.ptb_focus = 1
        self.pob_focus = 1
        
        self.controller_opts = CONTROL_OPTIONS.copy()
        
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
        
        self.warning_indexes_pos = (0, 0)
        self.settings_widget_height = self.settings_widget_x = 55
        self.settings_widget_width = self.SCR_WIDTH - (self.settings_widget_x * 2)
    
    def _init_skins(self):
        skin_path = [i.as_posix() for i in list(Path('SKINS').glob('*.*'))]
        
        self.ui_surf = None
        self.bg_surf = None
        self.ball_skin_surf = None
        self.player_skin_surf = None
        for i in skin_path:
            if '/player.png' in i.lower() or '/player.jpg' in i.lower():
                self.player_skin_surf = pygame.image.load(i)
            if '/background.png' in i.lower() or '/background.jpg' in i.lower():
                self.bg_surf = pygame.transform.scale(pygame.image.load(i), (self.SCR_WIDTH, self.SCR_HEIGHT))
            if '/ball.png' in i.lower() or '/ball.jpg' in i.lower():
                self.ball_skin_surf = pygame.image.load(i)
            if '/ui.png' in i.lower() or '/ui.jpg' in i.lower():
                self.ui_surf = pygame.image.load(i)
                self.back_button_img_rect = pygame.Rect(ICON_POS - (BG_OFFSET / 2), ICON_POS - (BG_OFFSET / 2), (ICON_SIZE * FN2_SIZE) + BG_OFFSET, (ICON_SIZE * FN2_SIZE) + BG_OFFSET)
                self.back_button_img_surf = pygame.transform.scale(self.ui_surf, (self.back_button_img_rect.width, self.back_button_img_rect.height))
            
    def _init_some_very_important_buttons(self):
        self.saa_size = (150, 30)
        
        self.on_focus_widg_vol = .2
        self.on_clicked_widg_vol = .2
        
        self.button_sound_info = ((ONWIDGETCLICKED_MP3_PATH, self.on_clicked_widg_vol), (ONWIDGETFOCUS_WAV_PATH, self.on_focus_widg_vol))
        
        self.back_button = Button(self.screen, self.FG_COLOR, (ICON_POS, ICON_POS), ICON_SIZE*FN3_SIZE, sound_info=self.button_sound_info)
        self.bt_mult_continue_button = Button(self.screen, self.FG_COLOR, (self.SCR_WIDTH - self.saa_size[0] - 50, self.SCR_HEIGHT - self.saa_size[1] - 30), self.saa_size, txt="   Continue  ", txt_color=self.BG_COLOR, sound_info=self.button_sound_info)
    
    def _init_serv_vars(self):
        # Next Time
        pass
    
    def _init_info_scr_vars(self):
        self.ptr_u_d_width = FN3_SIZE
        self.ptr_u_d_height = (FN3_SIZE * 1.5) - 10
        self.ptr_u_d_x = self.SCR_WIDTH - 25
        self.ptr_u_y = PTR_Y_POS + 5
        self.ptr_d_y = (self.SCR_HEIGHT - self.ptr_u_d_height - PTR_Y_POS) - 5
        
        self.cursor_counter = 1
        self.scr_focus = 0
        
        self.ptr_up = Button(self.screen, self.FG_COLOR, (self.ptr_u_d_x + 1, self.ptr_u_y), (self.ptr_u_d_width, self.ptr_u_d_height), border_radius=0)
        self.ptr_down = Button(self.screen, self.FG_COLOR, (self.ptr_u_d_x + 1, self.ptr_d_y), (self.ptr_u_d_width, self.ptr_u_d_height), border_radius=0)
        
        self.ptr_rect_up = self.ptr_up.rect.copy()
        self.ptr_rect_down = self.ptr_down.rect.copy()
        
        info_texts_size = max([rect[1].y for rect in mods.multiline_write((0, HELP_SCR_START_POS), HELP_INFO, FONT3, 'blue', 'blue')[0]]) - (self.SCR_HEIGHT / 2)
        self.info_scr_wheel_height = (self.SCR_HEIGHT / info_texts_size) * (self.ptr_rect_down.top - self.ptr_rect_up.bottom)
        
        self.scr_wheel_y = self.ptr_rect_up.bottom
        
        self.info_scroll_wheel = Button(self.screen, self.FG_COLOR, (self.ptr_u_d_x, self.scr_wheel_y), (self.ptr_u_d_width, self.info_scr_wheel_height), border_radius=0)
        
        self.cursor_img = pygame.image.load(ONHOVER_PNG_PATH)
        self.cursor_img = pygame.transform.rotozoom(self.cursor_img, 0, .5)
        
        self.max_link_hit_rect = pygame.Rect(0, 0, 0, 0)
    
    def _init_bt_vars(self):
        self.load_timer = 1
        self.load_dot_amount = 1
        self.bt_address_info = []
        self.addresses = []
        self.bt_addr_offset_val = 10
        self.searched = False
        self.opponent_addr = None
        self.authenticated = False
        self.bt_is_not_on = False
        self.customised = False
        self.retry_timer = 1
        self.bleak_scanner = bk.BleakScanner()
        self.exiting_mult_game = False
        # Next time, I will fix the use of this variable
        # self.mmu_y = 0
        self.bt_authenticate_tries_counter = 0
        self.search_for_bt_conn_again = False
        self.bt_exit_button = Button(self.screen, self.FG_COLOR, (ICON_POS, ICON_POS), ((ICON_SIZE*FN3_SIZE) * 4, ICON_SIZE*FN3_SIZE), txt='Exit', txt_color=self.BG_COLOR, sound_info=self.button_sound_info)
        self.multiplayer_b_buton = Button(self.screen, self.FG_COLOR, (self.SCR_WIDTH - (ICON_SIZE*FN3_SIZE) - ICON_POS, ICON_POS), ICON_SIZE*FN3_SIZE, sound_info=self.button_sound_info)
        self.bt_reload_button = Button(self.screen, self.FG_COLOR, (ICON_POS, ICON_POS), ((ICON_SIZE*FN3_SIZE) * 4, ICON_SIZE*FN3_SIZE), txt='Reload', txt_color=self.BG_COLOR, sound_info=self.button_sound_info)
        self.rotate_val = 0
        self.reload_surf = pygame.Surface((5, self.bt_reload_button.rect.height))
    
    def _init_text_view(self):
        self.fg_input = Input(self.screen, self.fg_txt_view_input, MAX_TV_LEN, (self.fg_t_v.centerx, self.fg_t_v.centery), FONT3, self.FG_COLOR)
        self.bg_input = Input(self.screen, self.bg_txt_view_input, MAX_TV_LEN, (self.bg_t_v.centerx, self.bg_t_v.centery), FONT3, self.FG_COLOR)
    
    def _init_other_widgets_in_settings(self):
        self.ai_difficulty_selector = Selector(self.screen, AI_DIFFICULTY_OPTIONS, self.ad_index, (self.ai_t_v.x, self.ai_t_v.y), FONT3, self.FG_COLOR, circular=True)
        self.p1_control_selector = Selector(self.screen, self.controller_opts, self.pc1_index, (self.p1c_t_v.x, self.p1c_t_v.y), FONT3, self.FG_COLOR, circular=True)
        self.p2_control_selector = Selector(self.screen, self.controller_opts, self.pc2_index, (self.p2c_t_v.x, self.p2c_t_v.y), FONT3, self.FG_COLOR, circular=True)
        self.mpo_selector = Selector(self.screen, ['Server', 'Bluetooth'], self.mpo_index, (self.mpo_s_v.x, self.mpo_s_v.y), FONT3, self.FG_COLOR, circular=True)
        self.pob_up_input = InputSeletor(self.screen, self.player1_up_txt_view_input, self.BG_COLOR, self.FG_COLOR, 'Player one binding up', (self.puko1.x, self.puko1.y), FONT3, self.FG_COLOR, mini_win_logo_path = LOGO_PNG_PATH, _prefix='Up: ')
        self.pob_down_input = InputSeletor(self.screen, self.player1_down_txt_view_input, self.BG_COLOR, self.FG_COLOR, 'Player one binding down', (self.puko2.x, self.puko2.y), FONT3, self.FG_COLOR, mini_win_logo_path = LOGO_PNG_PATH, _prefix='Down: ')
        self.ptb_up_input = InputSeletor(self.screen, self.player2_up_txt_view_input, self.BG_COLOR, self.FG_COLOR, 'Player two binding up', (self.pdko1.x, self.pdko1.y), FONT3, self.FG_COLOR, mini_win_logo_path = LOGO_PNG_PATH, _prefix='Up: ')
        self.ptb_down_input = InputSeletor(self.screen, self.player2_down_txt_view_input, self.BG_COLOR, self.FG_COLOR, 'Player two binding down', (self.pdko2.x, self.pdko2.y), FONT3, self.FG_COLOR, mini_win_logo_path = LOGO_PNG_PATH, _prefix='Down: ')
    
    def _init_pause_vars(self):
        self.mouse_move = 0
        self.pause_focus = 0
        self.setting_focus = 0
        self.start_opt_foc = self.setting_focus
        self.pause_bg_img = pygame.transform.scale(pygame.image.load(r'utils\ui\Untitled.png'), (self.SCR_WIDTH, self.SCR_HEIGHT))
    
    def _init_saved_values(self):
        with open(CONTINUE_JSON_PATH) as continue_vals:
            self.saved_continue_data = json.loads(continue_vals.read())
        
        with open(SETTINGS_JSON_PATH) as settings_vals:
            self.saved_settings_data = json.loads(settings_vals.read())
            
            self.bg_txt_view_input = self.BG_COLOR = self.saved_settings_data['bg_color'] if not isinstance(self.saved_settings_data['bg_color'], list) else tuple(self.saved_settings_data['bg_color'])
            self.fg_txt_view_input = self.FG_COLOR = self.saved_settings_data['fg_color'] if not isinstance(self.saved_settings_data['fg_color'], list) else tuple(self.saved_settings_data['fg_color'])
            self.str_bg_txt_view_input = str(self.bg_txt_view_input)
            self.str_fg_txt_view_input = str(self.fg_txt_view_input)
            
            self.ad_index = self.saved_settings_data['ad_index']
            self.pc1_index = self.saved_settings_data['pc1_index']
            self.pc2_index = self.saved_settings_data['pc2_index']
            
            self.player1_up_txt_view_input, self.player1_up = self.saved_settings_data['key1_up']
            self.player1_down_txt_view_input, self.player1_down = self.saved_settings_data['key1_down']
            self.player2_up_txt_view_input, self.player2_up = self.saved_settings_data['key2_up']
            self.player2_down_txt_view_input, self.player2_down = self.saved_settings_data['key2_down']

            self.is_a_new_game = self.saved_settings_data['is a new game']
            self.mpo = 'Bluetooth'
            self.mpo_index = 1
    
    def _init_misc_vars(self):
        self.start_focus = 0
        self.t1 = time.time()
        self.in_next_update = False
        self.pause_outline = pygame.Rect(self.SCR_WIDTH, 0, 0, 0)
        self.mlhr_width = 0
        self.start_blitting_timer = 0
        self.title_font = mods.make_font(4, 200)
        self.coming_soon_surf = mods.make_font(3, 100).render('Coming Soon', False, self.FG_COLOR)
        self.coming_soon_rect = self.coming_soon_surf.get_rect(center=(self.SCR_WIDTH / 2, self.SCR_HEIGHT / 2))
        self.widg_focused_sound = pygame.mixer.Sound(ONWIDGETFOCUS_WAV_PATH)
        self.widg_focused_sound.set_volume(self.on_focus_widg_vol)
        self.widg_clicked_sound = pygame.mixer.Sound(ONWIDGETCLICKED_MP3_PATH)
        self.widg_clicked_sound.set_volume(self.on_clicked_widg_vol)
        self.title_hover_offset = 0
    
    
    def _draw_midline(self):
        spacing = LINE_SPACE
        
        for _ in range(int(self.SCR_HEIGHT // LINE_LEN)):
            l_x_pos = self.SCR_WIDTH / 2
            if self.ui_surf is not None:
                self.screen.blit(pygame.transform.scale(self.ui_surf, (LINE_WIDTH, LINE_LEN)), (l_x_pos, spacing))
            else:
                pygame.draw.line(self.screen, self.FG_COLOR, (l_x_pos, spacing), (l_x_pos, spacing + LINE_LEN), LINE_WIDTH)
                
            spacing += LINE_LEN + LINE_SPACE
    
    def _validate_text_view(self):
        if self.apply_settings_changes:
            if len(self.str_bg_txt_view_input.split(',')) in (3, 4):
                self.bg_txt_view_input = tuple(int(i) for i in self.str_bg_txt_view_input.removeprefix('(').removesuffix(')').removeprefix('[').removesuffix(']').split(','))
            if len(self.str_fg_txt_view_input.split(',')) in (3, 4):
                self.fg_txt_view_input = tuple(int(i) for i in self.str_fg_txt_view_input.removeprefix('(').removesuffix(')').removeprefix('[').removesuffix(']').split(','))
            
            self.bg_txt_view_input = mods.check_valid_color(self.bg_txt_view_input, self.BG_COLOR)
            self.fg_txt_view_input = mods.check_valid_color(self.fg_txt_view_input, self.FG_COLOR)
            self._init_text_view()
    
    def _save_and_apply_settings(self):
        self.apply_settings_changes = True
    
    def _mult_save_and_apply(self):
        self._save_and_apply_settings()
        self.multiplayer_scr = False
        if self.mpo == 'Bluetooth':
            self.multiplayer_scr_bt = True
            self.multiplayer_scr_serv = False
            
        elif self.mpo == 'Server':
            self.multiplayer_scr_bt = False
            self.multiplayer_scr_serv = True
    
    def _restart(self, resume: bool, include_pause: bool = True):
        self.player1 = Player(self.screen, (P1_START_POS, self.SCR_HEIGHT / 2), PLAYER_SIZE, True)
        self.player2 = Player(self.screen, (self.SCR_WIDTH - EDGE_SPACE - PLAYER_SIZE[0], self.SCR_HEIGHT / 2), PLAYER_SIZE, False)
        self.ball = Ball(self.screen, (self.SCR_WIDTH / 2, self.SCR_HEIGHT / 2), BALL_RADIUS, (random.choice([1, -1]), random.choice([1, -1])))

        self.player1_score = 0
        self.player2_score = 0
        
        if include_pause:
            self.pause_focus = 0
        
        if resume:
            self.paused_scr = False
            self.info_scr = False
            self.settings_scr = False
    
    def _continue_game(self):
        player_1_score = self.saved_continue_data['player 1 score']
        player_2_score = self.saved_continue_data['player 2 score']
        p1_y = self.saved_continue_data['player 1 y position']
        p2_y = self.saved_continue_data['player 2 y position']
        b_pos = self.saved_continue_data['ball pos']
        b_dir = self.saved_continue_data['ball dir']
        
        self.player1 = Player(self.screen, (P1_START_POS, p1_y), PLAYER_SIZE, True)
        self.player2 = Player(self.screen, (self.SCR_WIDTH - EDGE_SPACE - PLAYER_SIZE[0], p2_y), PLAYER_SIZE, False)
        self.ball = Ball(self.screen, b_pos, BALL_RADIUS, b_dir, (player_1_score, player_2_score))
    
    def _exit_game(self):
        pygame.quit()
        sys.exit()
    
    def _save_and_exit(self):
        with open(CONTINUE_JSON_PATH, "w") as continue_file:
            p1_y_pos = self.player1.rect.centery
            p2_y_pos = self.player2.rect.centery
            b_dir = self.ball.x_dir, self.ball.y_dir
            b_pos = self.ball.rect.center
            
            self.saved_continue_data['player 1 score'] = self.player1_score
            self.saved_continue_data['player 2 score'] = self.player2_score
            self.saved_continue_data['player 1 y position'] = p1_y_pos
            self.saved_continue_data['player 2 y position'] = p2_y_pos
            self.saved_continue_data['ball dir'] = b_dir
            self.saved_continue_data['ball pos'] = b_pos
        
            new_var_info = json.dumps(self.saved_continue_data, indent=2)
            continue_file.write(new_var_info)
                
        self._save_and_apply_settings()
    
        if self.is_a_new_game:
            with open(SETTINGS_JSON_PATH, 'w') as settings_file:
                self.saved_settings_data['is a new game'] = False
                
                new_vals = json.dumps(self.saved_settings_data, indent=2)
                settings_file.write(new_vals)
        
        self._exit_game()
    
    def _main_menu_activated_actions(self):
        if self.rects_name[self.start_focus] == MAIN_MENU_DICT_CONTINUE:
            self.widg_clicked_sound.play()
            self._continue_game()
            self.started = True
            self.start_blitting = False
        elif self.rects_name[self.start_focus] == MAIN_MENU_DICT_NEW_GAME:
            self.widg_clicked_sound.play()
            self._restart(True)
            self.started = True
            self.start_blitting = False
        elif self.rects_name[self.start_focus] == MAIN_MENU_DICT_MULTIPLAYER:
            self.widg_clicked_sound.play()
            self.multiplayer_scr = True
            self.start_blitting = False
            self.init_once = True
        elif self.rects_name[self.start_focus] == 'Exit':
            self.widg_clicked_sound.play()
            self._exit_game()
    
    def _pause_activated_actions(self, action):
        self.widg_clicked_sound.play()
        if action == PAUSE_DICT_EXIT:
            self._save_and_exit()
        elif action == PAUSE_DICT_RESTART:
            self._restart(True)
            self.start_blitting = False
        elif action == PAUSE_DICT_MAIN_MENU:
            self.start_focus = 0
            self.started = False
            self.paused_scr = False
            self.start_blitting = False
        elif action == PAUSE_DICT_INFORMATION:
            self.info_scr = True
            self.paused_scr = False
        elif action == PAUSE_DICT_SETTINGS:
            self.settings_scr = True
            self.paused_scr = False
        elif action == PAUSE_DICT_RESUME:
            self.paused_scr = False
    
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
            self._save_and_apply_settings()
            
            self._validate_text_view()
    
    def _pause_mouse_func(self, i):
        if self.use_mouse and self.pause_focus != self.pause_dict_values.index(i):
            self.widg_focused_sound.play()
            self.pause_focus = self.pause_dict_values.index(i)
    
    def _main_menu_mouse_func(self, i):
        if self.start_use_mouse and self.rects_rects.index(i) != self.start_focus:
            self.widg_focused_sound.play()
            self.start_focus = self.rects_rects.index(i)
    
    def _on_hover_link(self, x, y):
        pygame.draw.line(self.screen, self.link_color, (x, y + FN3_SIZE*2.5), (x + self.txt_width, y + FN3_SIZE*2.5), 2)
        pygame.mouse.set_visible(False)
        self.screen.blit(self.cursor_img, (self.mouse_rect.x, self.mouse_rect.y))
        self.cursor_counter += 1
    
    def _exit_button_was_pressed(self):
        if self.started:
            if not self.paused_scr and not self.settings_scr and not self.info_scr:
                self.paused_scr = True
            else:
                if self.paused_scr:
                    self.paused_scr = False
                if self.settings_scr and not self.settings_disabled:
                    self.settings_scr = False
                    self._save_and_apply_settings()
                    self.paused_scr = True
                if self.info_scr:
                    self.paused_scr = True
                    self.info_scr = False
        else:
            if self.multiplayer_scr:
                self.multiplayer_scr = False
                self.start_blitting = False
            elif self.multiplayer_scr_serv:
                self.multiplayer_scr_serv = False
                self.multiplayer_scr = True
            elif self.multiplayer_scr_bt:
                self.scan_for_bt = False
                self.multiplayer_scr_bt = False
                self.multiplayer_scr = True
                self.searched = False
                self.scan_for_bt = True
    
    def _activate_mult_scr(self, pos):
        self.multiplayer_scr = False
        if pos == 1:
            self.multiplayer_scr_bt = True
            self.multiplayer_scr_serv = False
        elif pos == 2:
            self.multiplayer_scr_serv = True
            self.multiplayer_scr_bt = False
    
    def _draw_bg(self):
        self.screen.fill(self.BG_COLOR)
        if self.bg_surf is not None:
            self.screen.blit(self.bg_surf, (0, 0))

        if self.paused_scr:
            self.player1.draw(self.FG_COLOR)
            self.player2.draw(self.FG_COLOR)
            self.ball.draw(self.FG_COLOR)
            self._draw_midline()
            mods.draw_nums(self.screen, self.player1_score, 0, FONT_CELL_SIZE, True, self.FG_COLOR, self.ui_surf)
            mods.draw_nums(self.screen, self.player2_score, 0, FONT_CELL_SIZE, False, self.FG_COLOR, self.ui_surf)
            self.screen.blit(FONT2.render(self.controller_opts[self.pc1_index], False, self.FG_COLOR), (len(self.controller_opts[self.pc1_index]), self.SCR_HEIGHT-FN2_SIZE*2))
            self.screen.blit(FONT2.render(self.controller_opts[self.pc2_index], False, self.FG_COLOR), (self.SCR_WIDTH-(FN2_SIZE*len(self.controller_opts[self.pc2_index])+FN2_SIZE+3), self.SCR_HEIGHT-FN2_SIZE*2))
            
            self.screen.blit(self.pause_bg_img, (0, 0))
    
    def _scroll_up_down(self, up: bool):
        if up:
            self.scr_wheel_y -= SCROLL_SPEED * self.delta_time
        else:
            self.scr_wheel_y += SCROLL_SPEED * self.delta_time
    
    def _scroll(self):
        self.scr_wheel_y -= self.mouse_move
        if self.keys[pygame.K_UP]:
            if self.ptr_rect_up.bottom < self.scr_wheel_rect.top:
                self._scroll_up_down(True)
        if self.keys[pygame.K_DOWN]:
            if self.ptr_rect_down.top > self.scr_wheel_rect.bottom:
                self._scroll_up_down(False)
        
        self.mouse_move = mods.special_calcualation(self.mouse_move, 0, .000000001)
        
        if self.keys[pygame.K_HOME]:
            self.scr_wheel_y = self.ptr_rect_up.bottom
        elif self.keys[pygame.K_END]:
            self.scr_wheel_y = self.ptr_rect_down.top - self.info_scr_wheel_height
    
    def _load_timer(self, timer: int):
        if self.start_blitting_timer >= timer:
            self.start_blitting_timer = 0
            self.start_blitting = True
        else:
            self.start_blitting_timer += 1
    
    def _randomize_load_timer(self):
        self.loading_timer = random.randint(100, 700)
    
    def _activate_back_button(self):
        self.back_button.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_clicked, on_click=self._exit_button_was_pressed, color=self.FG_COLOR)
        if self.ui_surf is not None:
            self.screen.blit(self.back_button_img_surf, self.back_button_img_rect)
    
    
    def _server_multiplayer__blitting(self):
        # Next Time
        pass
    
    
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
        self.exiting_mult_game = True
        self._save_and_apply_settings()
    
    def _search_for_bt(self):
        if self.scan_for_bt:
            def bt_search():
                try:
                    b_address_info = bt.discover_devices(lookup_names=True)
                    ble_address_info = [(i.address, i.name) for i in asyncio.run(self.bleak_scanner.discover())]
                    
                    self.bt_address_info = mods.list_intersect(b_address_info, ble_address_info)
                except OSError:
                    self.bt_is_not_on = True
                
                if self.bt_is_not_on:
                    self.searched = True
                    self.scan_for_bt = False
                    return
                
                bt_lists_title_surf = mods.make_font(3, 40).render('Bluetooth Lobby', False, self.FG_COLOR)
                bt_lists_title_rect = bt_lists_title_surf.get_rect(center=(self.SCR_WIDTH / 2, bt_lists_title_surf.get_height()))

                self.addresses = [(bt_lists_title_surf, bt_lists_title_rect)]
                
                for clickable_index, clickable_texts in enumerate(self.bt_address_info):
                    font = mods.make_font(2, 20)
                    y = (font.render(f'{clickable_texts[1]} : {clickable_texts[0]}', False, self.FG_COLOR).get_height() + self.bt_addr_offset_val) * clickable_index + self.bt_addr_y_pos
                    ct = ClickableText(
                                    self.screen,
                                    f'{clickable_texts[1] if clickable_texts[1] else '_'} : {clickable_texts[0]}',
                                    font,
                                    self.FG_COLOR,
                                    self.BG_COLOR,
                                    (
                                        130,
                                        y
                                    ),
                                    sound_info=self.button_sound_info,
                                    )
                    sn = font.render(f'{clickable_index + 1}.', False, self.FG_COLOR)
                    sn_rect = sn.get_rect(midright=(ct.hover_rect.left - 30 , ct.hover_rect.centery))
                    
                    if ct not in self.addresses:
                        self.addresses.append(ct)
                    if (sn, sn_rect) not in self.addresses:
                        self.addresses.append((sn, sn_rect))
                
                self.searched = True

            self.start_bt_search = thread.Thread(target=bt_search)
            self.start_bt_search.daemon = True
            self.start_bt_search.start()
            
            self.scan_for_bt = False
        
        if self.bt_is_not_on:
            return
    
    def _find_and_assign_bt_opponent__blitting(self):
        self.bt_info_font = mods.make_font(2, 30)
        self.bt_addr_y_pos = 130
        
        if not self.searched:
            self._search_for_bt()
        
        if not self.start_bt_search.is_alive() and self.search_for_bt_conn_again:
            self.scan_for_bt = True
            self._search_for_bt()
            self.search_for_bt_conn_again = False
        
        if self.searched:
            if not self.bt_is_not_on:
                if self.start_blitting:
                    self.multiplayer_b_buton.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_clicked, on_click=self._exit_button_was_pressed, color=self.FG_COLOR)

                if self.start_bt_search.is_alive() and self.start_blitting:
                    self.rotate_val += 1
                    color = math.fabs(math.sin(math.radians(self.rotate_val)) * 255)
                    self.reload_surf.fill(mods.set_color(self.FG_COLOR, color))
                    self.rotate_val = self.rotate_val % 360
                    reload_surf = pygame.transform.rotate(self.reload_surf.convert_alpha(), self.rotate_val)
                    reload_rect = reload_surf.get_rect(center=((self.bt_reload_button.rect.midright[0] + 10) + (reload_surf.get_width() / 2), self.bt_reload_button.rect.midright[1]))
                    self.screen.blit(reload_surf, reload_rect)
                
                # ct_coord = list(set([objs[1].bottom if isinstance(objs, tuple) else None for objs in self.addresses]))
                # if None in ct_coord:
                #     ct_coord.remove(None)
                # last_ct_sn = max(ct_coord)
                
                # if last_ct_sn > self.SCR_HEIGHT:
                #     if self.keys[pygame.K_UP]:
                #         self.mmu_y += 7
                #     elif self.keys[pygame.K_DOWN]:
                #         self.mmu_y -= 7
                #     self.mmu_y = min(self.mmu_y, 0)
                #     self.mmu_y = max(self.mmu_y, last_ct_sn)
                
                def reload_button():
                    self.search_for_bt_conn_again = True
                
                def assign_bt_opponent(ct: ClickableText):
                    self.opponent_addr = ct.text.split(' : ')[1]
                
                self.bt_reload_button.activate_button(self.mouse_rect, self.mouse_clicked, on_click=reload_button)
                
                # Instead of putting self.mmu_y I put 0 because the mods.multiplayer_multiline_update function it needs some tuning and fixes
                # And the offset would sometimes be too high due too a large amount of addresses
                mods.multiplayer_multiline_update(self.screen, self.addresses, 0, assign_bt_opponent, (self.mouse_rect, self.mouse_clicked))
            else:
                self._bt_multiplayer_bt_is_not_on__blitting()
                self.exit_failed_scr_button.activate_button(self.mouse_rect, self.mouse_clicked, on_click=self._stop_bt_mult_game, color=(self.FG_COLOR, self.BG_COLOR))
        else:
            self._loading_scr('Loading')
    
    def _bt_authenticate(self, opponent_addr: str):
        bt_key = 'Ifechukwu is the oga and there is nothing anyone can do about that'
        
        with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as bt_comm:
            try:
                bt_comm.connect((opponent_addr, 1234))
                
                bt_comm.send(bt_key.encode())
                key_recv = bt_comm.recv(1024).decode()
                if key_recv == bt_key:
                    self.authenticated = True
                    self.load_scr = True
                    self.failed_auth = False
                    self.exiting_mult_game = False
                    return
                else:
                    self.retry_timer += 1
                
                if self.retry_timer > MAX_BT_RETRY:
                    self.authenticated = False
                    self.failed_auth = True
                    return
            
            except (TimeoutError, OSError):
                if self.bt_authenticate_tries_counter < MAX_BT_RETRY:
                    self.bt_authenticate_tries_counter += 1
                    self._bt_authenticate(self.opponent_addr)
                else:
                    self.authenticated = False
                    self.failed_auth = True
                    self.bt_authenticate_tries_counter = 0
    
    def _bt_get_send_game(self, opponent_addr: str):
        game_info_send = json.dumps(dict(movement=(self.keys[self.player1_up], self.keys[self.player1_down]), color=self.FG_COLOR, mouse_pos=(self.mouse_rect.x, self.mouse_rect.y), exitting=self.exiting_mult_game), indent=2)
        
        if self.authenticated:
            with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as bt_comm:
                bt_comm.connect((opponent_addr, 1234))
        
                bt_comm.send(game_info_send)
                self.game_info_recv = json.loads(bt_comm.recv(1024).decode())
                
                if self.game_info_recv['exitting']:
                    self._stop_bt_mult_game()
                    return
    
    def _bt_multiplayer_failed__blitting(self):
        failed_surf1 = mods.make_font(2, 30).render('Failed to Authenticate', False, self.FG_COLOR)
        failed_surf2 = mods.make_font(2, 30).render('The problem might come from choosing the wrong bluetooth address', False, self.FG_COLOR)
        
        failed_rect1 = failed_surf1.get_rect(center=(self.SCR_WIDTH / 2, (self.SCR_HEIGHT / 2) - (failed_surf1.get_height() / 2)))
        failed_rect2 = failed_surf2.get_rect(center=(self.SCR_WIDTH / 2, (self.SCR_HEIGHT / 2) + (failed_surf2.get_height() / 2)))
        
        self.screen.blit(failed_surf1, failed_rect1)
        self.screen.blit(failed_surf2, failed_rect2)
    
    def _bt_multiplayer__blitting(self):
        if self.opponent_addr is None:
            self._find_and_assign_bt_opponent__blitting()
        else:
            if not self.failed_auth:
                if not self.authenticated:
                    if self.start_bt_check:
                        bt_auth_info = thread.Thread(target=lambda: self._bt_authenticate(self.opponent_addr))
                        bt_auth_info.daemon = True
                        bt_auth_info.start()
                        
                        self.start_bt_check = False
                    
                    self._loading_scr('Authenticating')
                else:
                    self._bt_get_send_game(self.opponent_addr)
                    self.started = True
                    self.multiplayer_scr = False
                    self.load_scr = False
                    self.multiplayer_scr_serv = False
                    self.multiplayer_scr_bt = False
                    self.start_blitting = False
            else:
                self._bt_multiplayer_failed__blitting()
                self.exit_failed_scr_button.activate_button(self.mouse_rect, self.mouse_clicked, on_click=lambda: self._stop_bt_mult_game(False), color=(self.FG_COLOR, self.BG_COLOR))
    
    def _bt_multiplayer_bt_is_not_on__blitting(self):
        bt_not_on_info1 = self.bt_info_font.render('Bluetooth address scan failed', False, self.FG_COLOR)
        bt_not_on_info2 = self.bt_info_font.render('Either blutooth is not turned on or there was an error during the scan', False, self.FG_COLOR)
        
        bt_not_on_info_rect1 = bt_not_on_info1.get_rect(center=(self.SCR_WIDTH / 2, (self.SCR_HEIGHT / 2) - bt_not_on_info1.get_height()))
        bt_not_on_info_rect2 = bt_not_on_info2.get_rect(center=(self.SCR_WIDTH / 2, (self.SCR_HEIGHT / 2) + bt_not_on_info2.get_height()))
        
        self.screen.blit(bt_not_on_info1, bt_not_on_info_rect1)
        self.screen.blit(bt_not_on_info2, bt_not_on_info_rect2)
    
    def _loading_scr(self, info: str):
        self.load_timer += 1
        if self.load_timer % 50 == 0:
            self.load_dot_amount += 1
            self.load_timer = 1
        if self.load_dot_amount > 5:
            self.load_dot_amount = 1
        
        load_surf = mods.make_font(2, 30).render(f'{info}{'.' * self.load_dot_amount}', False, self.FG_COLOR)
        load_rect = load_surf.get_rect(center=(self.SCR_WIDTH / 2, self.SCR_HEIGHT / 2))

        self.screen.blit(load_surf, load_rect)
    

    def multiplayer(self):
        if self.start_blitting:
            self.settings(True)
        else:
            self.loading_timer = 100
            self._loading_scr('Please wait')
            self._load_timer(self.loading_timer)
    
    def pause(self):
        self.pause_outline = pygame.Rect(self.pause_text_rects[self.pause_dict_keys[self.pause_focus]].x - X_WIDG_SPACE_OFFSET / 2,
                                        self.pause_text_rects[self.pause_dict_keys[self.pause_focus]].y,
                                        self.pause_texts[self.pause_dict_keys[self.pause_focus]].get_width() + X_WIDG_SPACE_OFFSET,
                                        self.pause_texts[self.pause_dict_keys[self.pause_focus]].get_height())
        
        pygame.draw.rect(self.screen, self.FG_COLOR, self.pause_outline, FOCUS_RECT_WIDTH, BORDER_RAD, BORDER_RAD, BORDER_RAD, BORDER_RAD, BORDER_RAD)
        
        gp_text_surf = FONT1.render('Game Paused', False, self.FG_COLOR)
        gp_text_rect = gp_text_surf.get_rect(midtop=(self.SCR_WIDTH / 2, 40))
        self.screen.blit(gp_text_surf, gp_text_rect)
        
        for i in list(self.pause_texts.keys()):
            self.screen.blit(self.pause_texts[i], self.pause_text_rects[i])
    
    def information(self):
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                self.mouse_move = event.dict['precise_y']
        
        help_info_surf_list, list_val = mods.multiline_write((40, HELP_SCR_START_POS), HELP_INFO, FONT3, self.link_color, self.FG_COLOR)
        
        self.scr_wheel_y = pygame.math.clamp(self.scr_wheel_y, self.ptr_rect_up.bottom, self.ptr_rect_down.top - self.info_scr_wheel_height)
        self.scr_wheel_rect = pygame.Rect(self.ptr_u_d_x, self.scr_wheel_y, self.ptr_u_d_width, self.info_scr_wheel_height)
        
        def _info_scr_mouse_movement():
            self.scr_wheel_y += self.mouse_rel[1]
        
        self.info_scr_text_height = (self.SCR_HEIGHT * (self.ptr_rect_down.top - self.ptr_rect_up.bottom)) / self.info_scr_wheel_height
        self.scr_focus = self.info_scr_text_height * ((self.scr_wheel_y - self.ptr_rect_up.bottom) / (self.ptr_rect_down.top - self.info_scr_wheel_height))
        
        self.info_scroll_wheel.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_clicked, on_click=_info_scr_mouse_movement, pos=self.scr_wheel_rect.topleft, color=self.FG_COLOR, bounce_delay=0)
        
        help_scr_title_surf = FONT1.render(PAUSE_DICT_INFORMATION, False, self.FG_COLOR)
        help_scr_title_rect = help_scr_title_surf.get_rect(midtop=(self.SCR_WIDTH / 2, min(HELP_SCR_START_POS - self.scr_focus, self.info_scr_text_height) - 50))
        self.screen.blit(help_scr_title_surf, help_scr_title_rect)
        
        list_of_linkrects_x = []
        list_of_linkrects_width = []
        list_of_linkrects = []
        for blit_index, blit_info in enumerate(help_info_surf_list):
            rect = blit_info[1]
            y = rect.y - self.scr_focus
            self.txt_width, t_height = rect.size
            self.screen.blit(blit_info[0], (rect.x, y))
            
            if list_val[blit_index] in LINK_KEYS:
                text_rects = pygame.Rect(rect.x, y, self.txt_width, t_height)
                list_of_linkrects_x.append(text_rects.x)
                list_of_linkrects_width.append(text_rects.width)

                link_rect = pygame.Rect(rect.x, y, self.txt_width, t_height)
                
                if len(list_of_linkrects) <= len(LINK_KEYS):
                    list_of_linkrects.append(link_rect)
                
                if self.txt_width > self.mlhr_width:
                    self.mlhr_width = self.txt_width
                
                self.max_link_hit_rect.left = min(list_of_linkrects_x)
                
                if list_val[blit_index] == LINK_KEYS[0]:
                    self.max_link_hit_rect.y = link_rect.top
                    self.max_link_hit_rect.width = self.mlhr_width
                
                if list_val[blit_index] == LINK_KEYS[-1]:
                    self.max_link_hit_rect.height =  link_rect.bottom - self.max_link_hit_rect.y
                
                dead_zone_list = []
                for linkrect_index, linkrect in enumerate(list_of_linkrects):
                    if linkrect_index != len(list_of_linkrects) - 1:
                        cords = linkrect.x, linkrect.bottom, self.mlhr_width, list_of_linkrects[linkrect_index + 1].top - linkrect.bottom
                    else:
                        cords = linkrect.x, linkrect.bottom, self.mlhr_width, 0
                    dead_zone_list.append(cords)
                
                if not self.mouse_rect.colliderect(self.max_link_hit_rect):
                    pygame.mouse.set_visible(True)
                else:
                    for i in dead_zone_list:
                        if self.mouse_rect.colliderect(i):
                            pygame.mouse.set_visible(True)
                
                if self.mouse_rect.colliderect(link_rect):
                    self._on_hover_link(rect.x, y)
                    if self.mouse_clicked:
                        if self.mouse_clicked_for_links:
                            link = LINKS.get(list_val[blit_index])
                            link_starter = thread.Thread(target=lambda: webbrowser.open(link))
                            link_starter.daemon = True
                            link_starter.start()
                            self.mouse_clicked_for_links = False

            if list_val[blit_index] in HELP_SCR_HEADERS:
                line_height = y + (FN3_SIZE * 2.5)
                pygame.draw.line(self.screen, self.FG_COLOR, (rect.x, line_height), (rect.x + self.txt_width, line_height), 1)        
        
        self.ptr_up.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_clicked, on_click=lambda: self._scroll_up_down(True), bounce_delay=0, color=self.FG_COLOR)
        self.ptr_down.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_clicked, on_click=lambda: self._scroll_up_down(False), bounce_delay=0, color=self.FG_COLOR)
        
        self._scroll()

        if self.ui_surf is not None:
            self.screen.blit(pygame.transform.scale(self.ui_surf, (self.scr_wheel_rect.width, self.scr_wheel_rect.height)), self.scr_wheel_rect)
            self.screen.blit(pygame.transform.scale(self.ui_surf, (self.ptr_rect_up.width, self.ptr_rect_up.height)), self.ptr_rect_up)
            self.screen.blit(pygame.transform.scale(self.ui_surf, (self.ptr_rect_down.width, self.ptr_rect_down.height)), self.ptr_rect_down)
    
    def settings(self, multiplayer=False):
        self.settings_disabled = self.ptb_up_input.mini_win.isactive() or self.ptb_down_input.mini_win.isactive() or self.pob_up_input.mini_win.isactive() or self.pob_down_input.mini_win.isactive()
        
        setting_name = self.settings_dict_keys[self.setting_focus]
        
        if multiplayer:
            self.bt_mult_continue_button.disabled = self.settings_disabled
            if self.start_blitting:
                self.multiplayer_b_buton.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_clicked, on_click=self._exit_button_was_pressed, color=self.FG_COLOR)
            
            self.controller_opts = CONTROL_OPTIONS[0], CONTROL_OPTIONS[2]
            self.pc1_index = pygame.math.clamp(self.pc1_index, 0, 1)
            
            is_index_changed = True
            self.tv_bg_color = self.FG_COLOR
            self.tv_fg_color = self.FG_COLOR
            self.p1_color = self.FG_COLOR
            self.pob_color = self.FG_COLOR
            self.mpo_color = self.FG_COLOR
            
            continue_prompt_surf = FONT2.render('You can also click Enter to continue', False, self.FG_COLOR)
            continue_prompt_rect = continue_prompt_surf.get_rect(bottomleft=(0, self.SCR_HEIGHT))
            self.screen.blit(continue_prompt_surf, continue_prompt_rect)
            self.bt_mult_continue_button.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_clicked, on_click=self._mult_save_and_apply, color=(self.FG_COLOR, self.BG_COLOR))
        else:
            warning_surf = mods.make_font(2, 10).render('Changes made will reset the game', False, self.BG_COLOR)
        
            if self.init_once:
                self._init_text_view()
                self._init_other_widgets_in_settings()
                self.init_once = False
            is_index_changed = (((self.saved_settings_data['ad_index'] != self.ad_index) and (f'{setting_name} opt' == SETTINGS_DICT_AI_OPT_KEY)) or
                                ((self.saved_settings_data['pc1_index'] != self.pc1_index) and (f'{setting_name} opt' == SETTINGS_DICT_P1C_OPT_KEY))or
                                ((self.saved_settings_data['pc2_index'] != self.pc2_index) and (f'{setting_name} opt' == SETTINGS_DICT_P2C_OPT_KEY)))
            
            self.tv_bg_color = self.FG_COLOR
            self.tv_fg_color = self.FG_COLOR
            self.aid_color = self.FG_COLOR
            self.p1_color = self.FG_COLOR
            self.p2_color = self.FG_COLOR
            self.pob_color = self.FG_COLOR
            self.ptb_color = self.FG_COLOR
        
        settings_widg_background = pygame.Rect(
                                        self.settings_widget_x,
                                        self.setting_text_rects[setting_name].y - Y_SETTINGS_SPACE_OFFSET/2,
                                        self.settings_widget_width,
                                        self.settings_widget_height
                                        )
        mini_win_bg_color = mods.set_color(self.BG_COLOR, 200) if self.BG_COLOR not in ('black', [0, 0, 0], [0, 0, 0, 0], (0, 0, 0), (0, 0, 0, 0)) else 'grey20'
        
        if self.ui_surf is not None:
            self.screen.blit(pygame.transform.scale(self.back_button_img_surf, (settings_widg_background.width, settings_widg_background.height)), (settings_widg_background.x, settings_widg_background.y))
        
        pygame.draw.rect(self.screen, self.FG_COLOR, settings_widg_background)
        
        for i in self.setting_texts.keys():
            if f'{setting_name} opt' not in i:
                self.screen.blit(self.setting_texts[i], self.setting_text_rects[i])
        
        if setting_name == SETTINGS_DICT_BG_KEY:
            self.tv_bg_color = self.BG_COLOR
            self.bg_input.text_rect.centerx = self.setting_text_rects[setting_name].centerx
            self.bg_txt_view_input = self.bg_input.partial_activate_text_view(mouse_rect=self.mouse_rect, fg_color=self.tv_bg_color)
            
        elif setting_name == SETTINGS_DICT_FG_KEY:
            self.tv_fg_color = self.BG_COLOR
            self.fg_input.text_rect.centerx = self.setting_text_rects[setting_name].centerx
            self.fg_txt_view_input = self.fg_input.partial_activate_text_view(mouse_rect=self.mouse_rect, fg_color=self.tv_fg_color)
            
        elif setting_name == SETTINGS_DICT_P1C_KEY:
            self.p1_color = self.BG_COLOR
            if multiplayer:
                self.p1_control, self.pc1_index = self.p1_control_selector.activate_selector(self.mouse_rect, self.mouse_clicked, pos=self.setting_text_rects[SETTINGS_DICT_P1C_OPT_KEY].topleft, color=self.p1_color, options=(CONTROL_OPTIONS[0], CONTROL_OPTIONS[2]))
            else:
                self.p1_control, self.pc1_index = self.p1_control_selector.activate_selector(self.mouse_rect, self.mouse_clicked, color=self.p1_color)
                self.warning_indexes_pos = (
                        self.p1_control_selector.text_rect.centerx,
                        settings_widg_background.bottom - warning_surf.get_height()
                    )
        
        elif setting_name == SETTINGS_DICT_P2C_KEY:
            if not multiplayer:
                self.p2_color = self.BG_COLOR
                self.p2_control, self.pc2_index = self.p2_control_selector.activate_selector(self.mouse_rect, self.mouse_clicked, color=self.p2_color)
                self.warning_indexes_pos = (
                    self.p2_control_selector.text_rect.centerx,
                    settings_widg_background.bottom - warning_surf.get_height()
                    )
        
        elif setting_name == SETTINGS_DICT_AI_KEY:
            if not multiplayer:
                self.aid_color = self.BG_COLOR
                self.ai_difficulty, self.ad_index = self.ai_difficulty_selector.activate_selector(self.mouse_rect, self.mouse_clicked, color=self.aid_color)
                self.warning_indexes_pos = (
                        self.ai_difficulty_selector.text_rect.centerx,
                        settings_widg_background.bottom - warning_surf.get_height()
                        )
            
        elif setting_name == SETTINGS_DICT_POB_KEY:
            self.pob_color = self.BG_COLOR
            if self.pob_focus == 1:
                self.screen.blit(self.setting_texts[SETTINGS_DICT_POB_DOWN_OPT_KEY], self.setting_text_rects[SETTINGS_DICT_POB_DOWN_OPT_KEY])
                self.player1_up_txt_view_input, self.player1_up = self.pob_up_input.activate_input_selector(self.mouse_rect,
                                                                                                            self.mouse_clicked,
                                                                                                            self.mouse_rel,
                                                                                                            self.pob_color,
                                                                                                            mini_win_bg_color,
                                                                                                            self.FG_COLOR)
            
            elif self.pob_focus == 2:
                self.screen.blit(self.setting_texts[SETTINGS_DICT_POB_UP_OPT_KEY], self.setting_text_rects[SETTINGS_DICT_POB_UP_OPT_KEY])
                self.player1_down_txt_view_input, self.player1_down = self.pob_down_input.activate_input_selector(self.mouse_rect,
                                                                                                                    self.mouse_clicked,
                                                                                                                    self.mouse_rel,
                                                                                                                    self.pob_color,
                                                                                                                    mini_win_bg_color,
                                                                                                                    self.FG_COLOR)

        elif setting_name == SETTINGS_DICT_PTB_KEY:
            if not multiplayer:
                self.ptb_color = self.BG_COLOR
                if self.ptb_focus == 1:
                    self.screen.blit(self.setting_texts[SETTINGS_DICT_PTB_DOWN_OPT_KEY], self.setting_text_rects[SETTINGS_DICT_PTB_DOWN_OPT_KEY])
                    self.player2_up_txt_view_input, self.player2_up = self.ptb_up_input.activate_input_selector(self.mouse_rect,
                                                                                                                self.mouse_clicked,
                                                                                                                self.mouse_rel,
                                                                                                                self.ptb_color,
                                                                                                                mini_win_bg_color,
                                                                                                                self.FG_COLOR,)
                
                elif self.ptb_focus == 2:
                    self.screen.blit(self.setting_texts[SETTINGS_DICT_PTB_UP_OPT_KEY], self.setting_text_rects[SETTINGS_DICT_PTB_UP_OPT_KEY])
                    self.player2_down_txt_view_input, self.player2_down = self.ptb_down_input.activate_input_selector(self.mouse_rect,
                                                                                                                    self.mouse_clicked,
                                                                                                                    self.mouse_rel,
                                                                                                                    self.ptb_color,
                                                                                                                    mini_win_bg_color,
                                                                                                                    self.FG_COLOR)

        elif setting_name == SETTINGS_DICT_MPO_KEY:
            self.mpo_color = self.BG_COLOR
            self.mpo, _ = self.mpo_selector.activate_selector(self.mouse_rect, self.mouse_clicked, color=self.mpo_color)

        if not multiplayer:
            if is_index_changed:
                self.screen.blit(warning_surf, warning_surf.get_rect(midtop=(self.warning_indexes_pos)))
    
    
    def update(self):
        self.str_bg_txt_view_input = str(self.bg_txt_view_input)
        self.str_fg_txt_view_input = str(self.fg_txt_view_input)
        
        self.SCR_WIDTH = self.screen.get_width()
        self.SCR_HEIGHT = self.screen.get_height()

        self._draw_bg()
        
        self.mouse_pos = pygame.mouse.get_pos()
        m_x, m_y = self.mouse_pos
        self.mouse_rect = pygame.Rect(m_x, m_y, 1, 1)
        self.mouse_clicked = pygame.mouse.get_pressed()[0]
        self.in_stats_or_help = not self.info_scr
        
        if self.authenticated:
            self._bt_get_send_game(self.opponent_addr)
            self.bt_exit_button.activate_button(mouse_rect=self.mouse_rect, mouse_clicked=self.mouse_clicked, on_click=self._stop_bt_mult_game, color=self.FG_COLOR)
        else:
            if not self.multiplayer_scr and not self.multiplayer_scr_bt and not self.multiplayer_scr_serv:
                self.controller_opts = CONTROL_OPTIONS
                self.back_button.disabled = self.settings_disabled
        
        if self.apply_settings_changes:
            indexes_changed = (self.ad_index != self.saved_settings_data['ad_index']) or (self.pc1_index != self.saved_settings_data['pc1_index']) or (self.pc2_index != self.saved_settings_data['pc2_index'])
            
            self._validate_text_view()
            
            self.BG_COLOR = mods.check_valid_color(self.bg_txt_view_input, self.BG_COLOR)
            self.FG_COLOR = mods.check_valid_color(self.fg_txt_view_input, self.FG_COLOR)
            
            if indexes_changed:
                self._restart(False, False)
            
            with open(SETTINGS_JSON_PATH, "w") as settings_file:
                self.saved_settings_data['bg_color'] = self.BG_COLOR
                self.saved_settings_data['fg_color'] = self.FG_COLOR
                self.saved_settings_data['key1_up'] = (self.player1_up_txt_view_input, self.player1_up)
                self.saved_settings_data['key1_down'] = (self.player1_down_txt_view_input, self.player1_down)
                self.saved_settings_data['key2_up'] = (self.player2_up_txt_view_input, self.player2_up)
                self.saved_settings_data['key2_down'] = (self.player2_down_txt_view_input, self.player2_down)
                self.saved_settings_data['ad_index'] = self.ad_index
                self.saved_settings_data['pc1_index'] = self.pc1_index
                self.saved_settings_data['pc2_index'] = self.pc2_index
                
                new_info = json.dumps(self.saved_settings_data, indent=2)
                settings_file.write(new_info)
            self.apply_settings_changes = False
        
        self.delta_time = self.clock.tick(FPS)
        
        self.option_txt_colors = mods.set_color(self.FG_COLOR, 180)
        
        self.link_color = mods.set_color(self.FG_COLOR, 105)
        
        self.pause_texts = {
            PAUSE_DICT_RESUME: mods.font_renderer(PAUSE_DICT_RESUME, FONT3, self.option_txt_colors),
            PAUSE_DICT_INFORMATION: mods.font_renderer(PAUSE_DICT_INFORMATION, FONT3, self.option_txt_colors),
            PAUSE_DICT_SETTINGS: mods.font_renderer(PAUSE_DICT_SETTINGS, FONT3, self.option_txt_colors),
            PAUSE_DICT_MAIN_MENU: mods.font_renderer(PAUSE_DICT_MAIN_MENU, FONT3, self.option_txt_colors),
            PAUSE_DICT_RESTART: mods.font_renderer(PAUSE_DICT_RESTART, FONT3, self.option_txt_colors), 
            PAUSE_DICT_EXIT: mods.font_renderer(PAUSE_DICT_EXIT, FONT3, self.option_txt_colors),
        }
        self.pause_text_rects = {
            PAUSE_DICT_RESUME: mods.font_rect_renderer(self.screen, PAUSE_DICT_RESUME, FONT3.render(PAUSE_DICT_RESUME, False, self.FG_COLOR), y=PAUSE_TEXT_START_POS, x_offset=X_PAUSE_WIDG_POS_OFFSET),
            PAUSE_DICT_SETTINGS: mods.font_rect_renderer(self.screen, PAUSE_DICT_SETTINGS, FONT3.render(PAUSE_DICT_SETTINGS, False, self.FG_COLOR), y=PAUSE_TEXT_START_POS + PAUSE_TEXT_SPACING, x_offset=-X_PAUSE_WIDG_POS_OFFSET),
            PAUSE_DICT_INFORMATION: mods.font_rect_renderer(self.screen, PAUSE_DICT_INFORMATION, FONT3.render(PAUSE_DICT_INFORMATION, False, self.FG_COLOR), y=PAUSE_TEXT_START_POS + PAUSE_TEXT_SPACING*2, x_offset=X_PAUSE_WIDG_POS_OFFSET),
            PAUSE_DICT_MAIN_MENU: mods.font_rect_renderer(self.screen, PAUSE_DICT_MAIN_MENU, FONT3.render(PAUSE_DICT_MAIN_MENU, False, self.FG_COLOR), y=PAUSE_TEXT_START_POS + PAUSE_TEXT_SPACING*3, x_offset=-X_PAUSE_WIDG_POS_OFFSET),
            PAUSE_DICT_RESTART: mods.font_rect_renderer(self.screen, PAUSE_DICT_RESTART, FONT3.render(PAUSE_DICT_RESTART, False, self.FG_COLOR), y=PAUSE_TEXT_START_POS + (PAUSE_TEXT_SPACING*4), x_offset=X_PAUSE_WIDG_POS_OFFSET),
            PAUSE_DICT_EXIT: mods.font_rect_renderer(self.screen, 'Exit', FONT3.render('Exit', False, self.FG_COLOR), y=PAUSE_TEXT_START_POS + (PAUSE_TEXT_SPACING*5))
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
            SETTINGS_DICT_BG_KEY: mods.font_renderer(SETTINGS_DICT_BG_KEY, FONT3, self.tv_bg_color),
            SETTINGS_DICT_FG_KEY: mods.font_renderer(SETTINGS_DICT_FG_KEY, FONT3, self.tv_fg_color),
            SETTINGS_DICT_POB_KEY: mods.font_renderer(SETTINGS_DICT_POB_KEY, FONT3, self.pob_color),
            SETTINGS_DICT_PTB_KEY: mods.font_renderer(SETTINGS_DICT_PTB_KEY, FONT3, self.ptb_color),
            SETTINGS_DICT_AI_KEY: mods.font_renderer(SETTINGS_DICT_AI_KEY, FONT3, self.aid_color),
            SETTINGS_DICT_P1C_KEY: mods.font_renderer(SETTINGS_DICT_P1C_KEY, FONT3, self.p1_color),
            SETTINGS_DICT_P2C_KEY: mods.font_renderer(SETTINGS_DICT_P2C_KEY, FONT3, self.p2_color),
            
            SETTINGS_DICT_BG_OPT_KEY: mods.font_renderer(self.str_bg_txt_view_input, FONT3, self.tv_bg_color),
            SETTINGS_DICT_FG_OPT_KEY: mods.font_renderer(self.str_fg_txt_view_input, FONT3, self.tv_fg_color),
            
            SETTINGS_DICT_POB_UP_OPT_KEY: mods.font_renderer(f'Up: {self.player1_up_txt_view_input}', FONT3, self.pob_color),
            SETTINGS_DICT_PTB_UP_OPT_KEY: mods.font_renderer(f'Up: {self.player2_up_txt_view_input}', FONT3, self.ptb_color),
            SETTINGS_DICT_POB_DOWN_OPT_KEY: mods.font_renderer(f'Down: {self.player1_down_txt_view_input}', FONT3, self.pob_color),
            SETTINGS_DICT_PTB_DOWN_OPT_KEY: mods.font_renderer(f'Down: {self.player2_down_txt_view_input}', FONT3, self.ptb_color),
            
            SETTINGS_DICT_AI_OPT_KEY: mods.font_renderer(self.ai_difficulty, FONT3, self.aid_color),
            SETTINGS_DICT_P1C_OPT_KEY: mods.font_renderer(self.p1_control, FONT3, self.p1_color),
            SETTINGS_DICT_P2C_OPT_KEY: mods.font_renderer(self.p2_control, FONT3, self.p2_color),
        }
        
        self.setting_text_rects = {
            SETTINGS_DICT_BG_KEY: mods.font_rect_renderer(self.screen, SETTINGS_DICT_BG_KEY, FONT3.render(SETTINGS_DICT_BG_KEY, False, self.FG_COLOR),y=SETTINGS_TEXT_START_POS, x_offset= -X_SETTINGS_TEXT_OFFSET),
            SETTINGS_DICT_FG_KEY: mods.font_rect_renderer(self.screen, SETTINGS_DICT_FG_KEY, FONT3.render(SETTINGS_DICT_FG_KEY, False, self.FG_COLOR),y=SETTINGS_TEXT_START_POS + SETTINGS_TEXT_SPACING, x_offset= -X_SETTINGS_TEXT_OFFSET),
            SETTINGS_DICT_POB_KEY: mods.font_rect_renderer(self.screen, SETTINGS_DICT_POB_UP_OPT_KEY, FONT3.render(SETTINGS_DICT_POB_UP_OPT_KEY, False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*2), x_offset= -X_SETTINGS_TEXT_OFFSET),
            SETTINGS_DICT_PTB_KEY: mods.font_rect_renderer(self.screen, SETTINGS_DICT_PTB_UP_OPT_KEY, FONT3.render(SETTINGS_DICT_PTB_UP_OPT_KEY, False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*3), x_offset= -X_SETTINGS_TEXT_OFFSET),
            SETTINGS_DICT_AI_KEY: mods.font_rect_renderer(self.screen, SETTINGS_DICT_AI_KEY, FONT3.render(SETTINGS_DICT_AI_KEY, False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*4), x_offset= -X_SETTINGS_TEXT_OFFSET),
            SETTINGS_DICT_P1C_KEY: mods.font_rect_renderer(self.screen, SETTINGS_DICT_P1C_KEY, FONT3.render(SETTINGS_DICT_P1C_KEY, False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*5), x_offset= -X_SETTINGS_TEXT_OFFSET),
            SETTINGS_DICT_P2C_KEY: mods.font_rect_renderer(self.screen, SETTINGS_DICT_P2C_KEY, FONT3.render(SETTINGS_DICT_P2C_KEY, False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*6), x_offset= -X_SETTINGS_TEXT_OFFSET),
            
            SETTINGS_DICT_BG_OPT_KEY: mods.font_rect_renderer(self.screen, self.str_bg_txt_view_input, FONT3.render(self.str_bg_txt_view_input, False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS, x_offset= X_SETTINGS_TEXT_OFFSET),
            SETTINGS_DICT_FG_OPT_KEY: mods.font_rect_renderer(self.screen, self.str_fg_txt_view_input, FONT3.render(self.str_fg_txt_view_input, False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + SETTINGS_TEXT_SPACING, x_offset= X_SETTINGS_TEXT_OFFSET),
            SETTINGS_DICT_AI_OPT_KEY: mods.font_rect_renderer(self.screen, self.ai_difficulty, FONT3.render(self.ai_difficulty, False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*4), x_offset= X_SETTINGS_TEXT_OFFSET),
            
            SETTINGS_DICT_P1C_OPT_KEY: mods.font_rect_renderer(self.screen, self.p1_control, FONT3.render(self.p1_control, False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*5), x_offset= X_SETTINGS_TEXT_OFFSET),
            SETTINGS_DICT_P2C_OPT_KEY: mods.font_rect_renderer(self.screen, self.p2_control, FONT3.render(self.p2_control, False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*6), x_offset= X_SETTINGS_TEXT_OFFSET),

            SETTINGS_DICT_POB_UP_OPT_KEY: mods.font_rect_renderer(self.screen, f'Up: {self.player1_up_txt_view_input}', FONT3.render(f'Up: {self.player1_up_txt_view_input}', False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*2), x_offset= X_SETTINGS_TEXT_OFFSET - FN3_SIZE*6),#*len('UP: ')),
            SETTINGS_DICT_PTB_UP_OPT_KEY: mods.font_rect_renderer(self.screen, f'Up: {self.player2_up_txt_view_input}', FONT3.render(f'Up: {self.player2_up_txt_view_input}', False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*3), x_offset= X_SETTINGS_TEXT_OFFSET - FN3_SIZE*6),#*len(f'UP: ')),
            SETTINGS_DICT_POB_DOWN_OPT_KEY: mods.font_rect_renderer(self.screen, f'Down: {self.player1_down_txt_view_input}', FONT3.render(f'Down: {self.player1_down_txt_view_input}', False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*2), x_offset= X_SETTINGS_TEXT_OFFSET + FN3_SIZE*8.5),
            SETTINGS_DICT_PTB_DOWN_OPT_KEY: mods.font_rect_renderer(self.screen, f'Down: {self.player2_down_txt_view_input}', FONT3.render(f'Down: {self.player2_down_txt_view_input}', False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*3), x_offset= X_SETTINGS_TEXT_OFFSET + FN3_SIZE*8.5),
        }
        
        self.bg_t_v = self.setting_text_rects[SETTINGS_DICT_BG_OPT_KEY]
        self.fg_t_v = self.setting_text_rects[SETTINGS_DICT_FG_OPT_KEY]
        self.ai_t_v = self.setting_text_rects[SETTINGS_DICT_AI_OPT_KEY]
        self.p1c_t_v = self.setting_text_rects[SETTINGS_DICT_P1C_OPT_KEY]
        self.p2c_t_v = self.setting_text_rects[SETTINGS_DICT_P2C_OPT_KEY]
        self.puko1 = self.setting_text_rects[SETTINGS_DICT_POB_UP_OPT_KEY]
        self.pdko1 = self.setting_text_rects[SETTINGS_DICT_PTB_UP_OPT_KEY]
        self.puko2 = self.setting_text_rects[SETTINGS_DICT_POB_DOWN_OPT_KEY]
        self.pdko2 = self.setting_text_rects[SETTINGS_DICT_PTB_DOWN_OPT_KEY]
        self.pause_dict_keys = list(self.pause_text_rects.keys())
        self.settings_dict_keys = list(self.setting_text_rects.keys())
        self.pause_dict_values = list(self.pause_text_rects.values())

        self.mouse_rel = pygame.mouse.get_rel()
        self.use_mouse = self.mouse_rel != (0, 0)
    
    
    def game_event_loop(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self._save_and_exit()
        
        if self.start_blitting:
            if self.mouse_clicked:
                self.mouse_clicked_for_links = True
            
            self.keys = pygame.key.get_pressed()

            if event.type == pygame.KEYDOWN:
                if self.keys[pygame.K_ESCAPE]:
                    self._exit_button_was_pressed()
            
            if True in (self.paused_scr, self.settings_scr):
                if self.paused_scr:
                    self.scr_wheel_y = self.ptr_rect_up.bottom
                    for pause_widg_rect in self.pause_dict_values:
                        click_area = pygame.Rect(
                                                    pause_widg_rect.x - (X_WIDG_SPACE_OFFSET / 2),
                                                    pause_widg_rect.y,
                                                    pause_widg_rect.width + X_WIDG_SPACE_OFFSET,
                                                    pause_widg_rect.height,
                                                )
                        
                        if mods.isclicked(self.mouse_rect, click_area, self.mouse_clicked, lambda: self._pause_mouse_func(pause_widg_rect)):
                            self._pause_activated_actions(self.pause_dict_keys[self.pause_focus])
                elif self.settings_scr:
                    height = 55
                    x = height
                    width = self.SCR_WIDTH - (x * 2)
                    settings_bg_rect_info = [rect if ' opt' not in i else 'skip' for i, rect in self.setting_text_rects.items()]
                    self.setting_option_background_rects = [pygame.Rect(x, pos_info.y - (Y_SETTINGS_SPACE_OFFSET / 2), width, height) if pos_info != 'skip' else 'skip' for pos_info in settings_bg_rect_info]
                    if 'skip' in self.setting_option_background_rects:
                        for _ in range(self.setting_option_background_rects.count('skip')):
                            self.setting_option_background_rects.remove('skip')
                    
                    for i in self.setting_option_background_rects:
                        mods.isclicked(self.mouse_rect, i, self.mouse_clicked, lambda: self._setting_mouse_func(i))
                    
                    mods.isclicked(self.mouse_rect, self.setting_text_rects[SETTINGS_DICT_POB_UP_OPT_KEY], self.mouse_clicked, lambda: self._pbo_mouse_func('pob', 1))
                    mods.isclicked(self.mouse_rect, self.setting_text_rects[SETTINGS_DICT_POB_DOWN_OPT_KEY], self.mouse_clicked, lambda: self._pbo_mouse_func('pob', 2))
                    mods.isclicked(self.mouse_rect, self.setting_text_rects[SETTINGS_DICT_PTB_UP_OPT_KEY], self.mouse_clicked, lambda: self._pbo_mouse_func('ptb', 1))
                    mods.isclicked(self.mouse_rect, self.setting_text_rects[SETTINGS_DICT_PTB_DOWN_OPT_KEY], self.mouse_clicked, lambda: self._pbo_mouse_func('ptb', 2))
                
                if event.type == pygame.KEYDOWN:
                        if self.paused_scr:
                            last_widg_index = len(self.pause_dict_keys) - 1
                            if self.keys[pygame.K_UP] and self.pause_focus != 0:
                                self.widg_focused_sound.play()
                                self.pause_focus -= 1
                                self.use_mouse = False
                            elif self.keys[pygame.K_DOWN] and self.pause_focus != last_widg_index:
                                self.widg_focused_sound.play()
                                self.pause_focus += 1
                                self.use_mouse = False
                                
                            if self.keys[pygame.K_RETURN]:
                                self._pause_activated_actions(self.pause_dict_keys[self.pause_focus])
                        elif self.settings_scr:
                            last_opt_index = (len(self.settings_dict_keys) -3 ) // 2
                            
                            def key_up_or_down_pressed_for_settings(direction_moved: int):
                                self.widg_focused_sound.play()
                                self.pob_focus = 1
                                self.ptb_focus = 1
                                prev_setting_focus = self.setting_focus
                                self.setting_focus += direction_moved
                                self.setting_focus = pygame.math.clamp(self.setting_focus, 0, last_opt_index)
                                if prev_setting_focus != self.setting_focus:
                                    self._save_and_apply_settings()
                                
                                self._validate_text_view()
                            
                            if self.keys[pygame.K_UP] and not self.settings_disabled and self.setting_focus != 0:
                                key_up_or_down_pressed_for_settings(-1)
                            
                            elif self.keys[pygame.K_DOWN] and not self.settings_disabled and self.setting_focus != last_opt_index:
                                key_up_or_down_pressed_for_settings(1)
                            
                            if self.settings_dict_keys[self.setting_focus] == SETTINGS_DICT_POB_KEY:
                                if not self.settings_disabled:
                                    if self.keys[pygame.K_LEFT]:
                                        self.pob_focus -= 1
                                        self.widg_focused_sound.play()
                                    elif self.keys[pygame.K_RIGHT]:
                                        self.pob_focus += 1
                                        self.widg_focused_sound.play()
                                    self.pob_focus = pygame.math.clamp(self.pob_focus, 1, 2)
                                
                                if self.keys[pygame.K_RETURN]:
                                    self.widg_clicked_sound.play()
                            elif self.settings_dict_keys[self.setting_focus] == SETTINGS_DICT_PTB_KEY:
                                if not self.settings_disabled:
                                    if self.keys[pygame.K_LEFT]:
                                        self.ptb_focus -= 1
                                        self.widg_focused_sound.play()
                                    elif self.keys[pygame.K_RIGHT]:
                                        self.ptb_focus += 1
                                        self.widg_focused_sound.play()
                                    self.ptb_focus = pygame.math.clamp(self.ptb_focus, 1, 2)
                                
                                if self.keys[pygame.K_RETURN]:
                                    self.widg_clicked_sound.play()
                            else:
                                if not self.settings_disabled:
                                    if self.keys[pygame.K_RETURN]:
                                        self._save_and_apply_settings()

                self.setting_focus = 0 if not self.settings_scr else self.setting_focus
    
    def game_scr(self):
        if self.authenticated:
            move_info = self.game_info_recv['movement']
            mouse = self.game_info_recv['mouse']
            color = self.game_info_recv['color']
        
        ball_rect_info = self.ball.get_rect_info()
        player1_rect_info = self.player1.get_rect_info()
        player2_rect_info = self.player2.get_rect_info()
        self.player1_score, self.player2_score = self.ball.get_score()
        
        mods.draw_nums(self.screen, self.player1_score, 0, FONT_CELL_SIZE, True, self.FG_COLOR, self.ui_surf)
        mods.draw_nums(self.screen, self.player2_score, 0, FONT_CELL_SIZE, False, self.FG_COLOR, self.ui_surf)
        
        self.ball.update(BALL_SPEED * self.delta_time, (player1_rect_info, player2_rect_info), self.FG_COLOR, self.ball_skin_surf)
        
        self.player1.update(self.p1_control, ball_rect_info, self.mouse_pos, PLAYER_SPEED * self.delta_time, (self.player1_up, self.player1_down), self.ai_difficulty, self.FG_COLOR, self.player_skin_surf)
        self.player2.update(self.p2_control, ball_rect_info, mouse if self.authenticated else self.mouse_pos, PLAYER_SPEED * self.delta_time, move_info if self.authenticated else (self.player2_up, self.player2_down), self.ai_difficulty, color if self.authenticated else self.FG_COLOR, None if self.authenticated else self.player_skin_surf)
        
        self._draw_midline()
        
        self.screen.blit(FONT2.render(self.controller_opts[self.pc1_index], False, self.FG_COLOR), (len(self.controller_opts[self.pc1_index]), self.SCR_HEIGHT-FN2_SIZE*2))
        self.screen.blit(FONT2.render(self.controller_opts[self.pc2_index], False, self.FG_COLOR), (self.SCR_WIDTH-(FN2_SIZE*len(self.controller_opts[self.pc2_index])+FN2_SIZE+3), self.SCR_HEIGHT-FN2_SIZE*2))
    
    def game_main_loop(self):
        if self.start_blitting:
            if not self.authenticated:
                self._activate_back_button()
            
            if self.info_scr:
                self.information()
            elif self.settings_scr:
                self.settings()
            elif self.paused_scr:
                self.pause()
            else:
                self.game_scr()
        else:
            if not self.authenticated:
                self._randomize_load_timer()
            else:
                self.loading_timer = 200
            self._loading_scr('Loading')
            self._load_timer(self.loading_timer)
    
    
    def main_menu_update(self):
        self.main_title_surf = self.title_font.render(self.game_title, False, self.FG_COLOR)
        self.title_hover_offset += 2
        self.title_hover_offset = self.title_hover_offset % 360
        y_floating_offset = math.sin(math.radians(self.title_hover_offset)) * 10
        
        self.main_title_rect = self.main_title_surf.get_rect(center=(self.SCR_WIDTH / 2, (self.main_title_surf.get_height() - (self.main_title_surf.get_height() / 4)) + y_floating_offset))
        
        if self.is_a_new_game:
            self.start_texts = {
                MAIN_MENU_DICT_NEW_GAME: mods.font_renderer(MAIN_MENU_DICT_NEW_GAME, FONT3, self.option_txt_colors),
                MAIN_MENU_DICT_MULTIPLAYER: mods.font_renderer(MAIN_MENU_DICT_MULTIPLAYER, FONT3, self.option_txt_colors),
                MAIN_MENU_DICT_EXIT: mods.font_renderer(MAIN_MENU_DICT_EXIT, FONT3, self.option_txt_colors),
            }
            self.start_text_rects = {
                MAIN_MENU_DICT_NEW_GAME: mods.font_rect_renderer(self.screen, MAIN_MENU_DICT_NEW_GAME, FONT3.render(MAIN_MENU_DICT_NEW_GAME, False, self.FG_COLOR), y=MAIN_MENU_TEXT_START_POS + MAIN_MENU_TEXT_Y_SPACE_OFFSET, x_offset=MAIN_MENU_X_SPACING_OFFSET),
                MAIN_MENU_DICT_MULTIPLAYER: mods.font_rect_renderer(self.screen, MAIN_MENU_DICT_MULTIPLAYER, FONT3.render(MAIN_MENU_DICT_MULTIPLAYER, False, self.FG_COLOR), y=MAIN_MENU_TEXT_START_POS + MAIN_MENU_TEXT_SPACING + MAIN_MENU_TEXT_Y_SPACE_OFFSET, x_offset=-MAIN_MENU_X_SPACING_OFFSET),
                MAIN_MENU_DICT_EXIT: mods.font_rect_renderer(self.screen, MAIN_MENU_DICT_EXIT, FONT3.render(MAIN_MENU_DICT_MULTIPLAYER, False, self.FG_COLOR), y=MAIN_MENU_TEXT_START_POS + MAIN_MENU_TEXT_SPACING*2 + MAIN_MENU_TEXT_Y_SPACE_OFFSET, x_offset=MAIN_MENU_X_SPACING_OFFSET),
            }
        else:
            self.start_texts = {
                MAIN_MENU_DICT_CONTINUE: mods.font_renderer(MAIN_MENU_DICT_CONTINUE, FONT3, self.option_txt_colors),
                MAIN_MENU_DICT_NEW_GAME: mods.font_renderer(MAIN_MENU_DICT_NEW_GAME, FONT3, self.option_txt_colors),
                MAIN_MENU_DICT_MULTIPLAYER: mods.font_renderer(MAIN_MENU_DICT_MULTIPLAYER, FONT3, self.option_txt_colors),
                MAIN_MENU_DICT_EXIT: mods.font_renderer(MAIN_MENU_DICT_EXIT, FONT3, self.option_txt_colors),
                }
            self.start_text_rects = {
                MAIN_MENU_DICT_CONTINUE: mods.font_rect_renderer(self.screen, MAIN_MENU_DICT_CONTINUE, FONT3.render(MAIN_MENU_DICT_CONTINUE, False, self.FG_COLOR), y=MAIN_MENU_TEXT_START_POS + MAIN_MENU_TEXT_Y_SPACE_OFFSET, x_offset=MAIN_MENU_X_SPACING_OFFSET),
                MAIN_MENU_DICT_NEW_GAME: mods.font_rect_renderer(self.screen, MAIN_MENU_DICT_NEW_GAME, FONT3.render(MAIN_MENU_DICT_NEW_GAME, False, self.FG_COLOR), y=MAIN_MENU_TEXT_START_POS + MAIN_MENU_TEXT_SPACING + MAIN_MENU_TEXT_Y_SPACE_OFFSET, x_offset=-MAIN_MENU_X_SPACING_OFFSET),
                MAIN_MENU_DICT_MULTIPLAYER: mods.font_rect_renderer(self.screen, MAIN_MENU_DICT_MULTIPLAYER, FONT3.render(MAIN_MENU_DICT_MULTIPLAYER, False, self.FG_COLOR), y=MAIN_MENU_TEXT_START_POS + MAIN_MENU_TEXT_SPACING*2 + MAIN_MENU_TEXT_Y_SPACE_OFFSET, x_offset=MAIN_MENU_X_SPACING_OFFSET),
                MAIN_MENU_DICT_EXIT: mods.font_rect_renderer(self.screen, MAIN_MENU_DICT_EXIT, FONT3.render(MAIN_MENU_DICT_EXIT, False, self.FG_COLOR),y=MAIN_MENU_TEXT_START_POS + MAIN_MENU_TEXT_SPACING*3 + MAIN_MENU_TEXT_Y_SPACE_OFFSET, x_offset=-MAIN_MENU_X_SPACING_OFFSET),
            }

        self.rects_name = [k for k, _ in self.start_text_rects.items()]
        self.rects_rects = [k for _, k in self.start_text_rects.items()]
        
        if self.multiplayer_scr:
            self.setting_texts = {
                SETTINGS_DICT_BG_KEY: mods.font_renderer(SETTINGS_DICT_BG_KEY, FONT3, self.tv_bg_color),
                SETTINGS_DICT_FG_KEY: mods.font_renderer(SETTINGS_DICT_FG_KEY, FONT3, self.tv_fg_color),
                SETTINGS_DICT_POB_KEY: mods.font_renderer(SETTINGS_DICT_POB_KEY, FONT3, self.pob_color),
                SETTINGS_DICT_P1C_KEY: mods.font_renderer(SETTINGS_DICT_P1C_KEY, FONT3, self.p1_color),
                SETTINGS_DICT_MPO_KEY: mods.font_renderer(SETTINGS_DICT_MPO_KEY, FONT3, self.mpo_color),
                
                SETTINGS_DICT_BG_OPT_KEY: mods.font_renderer(self.str_bg_txt_view_input, FONT3, self.tv_bg_color),
                SETTINGS_DICT_FG_OPT_KEY: mods.font_renderer(self.str_fg_txt_view_input, FONT3, self.tv_fg_color),
                SETTINGS_DICT_POB_UP_OPT_KEY: mods.font_renderer(f'Up: {self.player1_up_txt_view_input}', FONT3, self.pob_color),
                SETTINGS_DICT_POB_DOWN_OPT_KEY: mods.font_renderer(f'Down: {self.player1_down_txt_view_input}', FONT3, self.pob_color),
                SETTINGS_DICT_P1C_OPT_KEY: mods.font_renderer(self.p1_control, FONT3, self.p1_color),
                SETTINGS_DICT_MPO_OPT_KEY: mods.font_renderer(self.mpo, FONT3, self.mpo_color)
                }
            self.setting_text_rects = {
                SETTINGS_DICT_BG_KEY: mods.font_rect_renderer(self.screen, SETTINGS_DICT_BG_KEY, FONT3.render(SETTINGS_DICT_BG_KEY, False, self.FG_COLOR),y=SETTINGS_TEXT_START_POS, x_offset= -X_SETTINGS_TEXT_OFFSET),
                SETTINGS_DICT_FG_KEY: mods.font_rect_renderer(self.screen, SETTINGS_DICT_FG_KEY, FONT3.render(SETTINGS_DICT_FG_KEY, False, self.FG_COLOR),y=SETTINGS_TEXT_START_POS + SETTINGS_TEXT_SPACING, x_offset= -X_SETTINGS_TEXT_OFFSET),
                SETTINGS_DICT_POB_KEY: mods.font_rect_renderer(self.screen, SETTINGS_DICT_POB_UP_OPT_KEY, FONT3.render(SETTINGS_DICT_POB_UP_OPT_KEY, False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*2), x_offset= -X_SETTINGS_TEXT_OFFSET),
                SETTINGS_DICT_P1C_KEY: mods.font_rect_renderer(self.screen, SETTINGS_DICT_P1C_KEY, FONT3.render(SETTINGS_DICT_P1C_KEY, False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*3), x_offset= -X_SETTINGS_TEXT_OFFSET),
                SETTINGS_DICT_MPO_KEY: mods.font_rect_renderer(self.screen, SETTINGS_DICT_MPO_KEY, FONT3.render(SETTINGS_DICT_MPO_KEY, False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*4), x_offset= -X_SETTINGS_TEXT_OFFSET),
                
                SETTINGS_DICT_BG_OPT_KEY: mods.font_rect_renderer(self.screen, self.str_bg_txt_view_input, FONT3.render(self.str_bg_txt_view_input, False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS, x_offset= X_SETTINGS_TEXT_OFFSET),
                SETTINGS_DICT_FG_OPT_KEY: mods.font_rect_renderer(self.screen, self.str_fg_txt_view_input, FONT3.render(self.str_fg_txt_view_input, False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + SETTINGS_TEXT_SPACING, x_offset= X_SETTINGS_TEXT_OFFSET),
                SETTINGS_DICT_POB_UP_OPT_KEY: mods.font_rect_renderer(self.screen, f'Up: {self.player1_up_txt_view_input}', FONT3.render(f'Up: {self.player1_up_txt_view_input}', False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*2), x_offset= X_SETTINGS_TEXT_OFFSET - FN3_SIZE*6),
                SETTINGS_DICT_POB_DOWN_OPT_KEY: mods.font_rect_renderer(self.screen, f'Down: {self.player1_down_txt_view_input}', FONT3.render(f'Down: {self.player1_down_txt_view_input}', False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*2), x_offset= X_SETTINGS_TEXT_OFFSET + FN3_SIZE*8.5),
                SETTINGS_DICT_P1C_OPT_KEY: mods.font_rect_renderer(self.screen, self.p1_control, FONT3.render(self.p1_control, False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*3), x_offset= X_SETTINGS_TEXT_OFFSET),
                SETTINGS_DICT_MPO_OPT_KEY: mods.font_rect_renderer(self.screen, self.mpo, FONT3.render(self.mpo, False, self.FG_COLOR), y=SETTINGS_TEXT_START_POS + (SETTINGS_TEXT_SPACING*4), x_offset= X_SETTINGS_TEXT_OFFSET)
            }
            
            self.bg_t_v = self.setting_text_rects[SETTINGS_DICT_BG_OPT_KEY]
            self.fg_t_v = self.setting_text_rects[SETTINGS_DICT_FG_OPT_KEY]
            self.p1c_t_v = self.setting_text_rects[SETTINGS_DICT_P1C_OPT_KEY]
            self.puko1 = self.setting_text_rects[SETTINGS_DICT_POB_UP_OPT_KEY]
            self.pdko1 = self.setting_text_rects[SETTINGS_DICT_POB_DOWN_OPT_KEY]
            self.mpo_s_v = self.setting_text_rects[SETTINGS_DICT_MPO_OPT_KEY]
            
            self.settings_dict_keys = [k for k, _ in self.setting_text_rects.items()]
    
    def main_menu_event_loop(self, event: pygame.event.Event):
        if event.type == pygame.QUIT:
            self._exit_game()
        
        if self.start_blitting:
            self.keys = pygame.key.get_pressed()
            self.started_mouse_rel = pygame.mouse.get_rel()
            self.start_use_mouse = self.started_mouse_rel != (0, 0)
            
            if self.multiplayer_scr:
                if self.keys[pygame.K_ESCAPE]:
                    self.multiplayer_scr = False
                
                mods.isclicked(self.mouse_rect, self.setting_text_rects[SETTINGS_DICT_POB_UP_OPT_KEY], self.mouse_clicked, lambda: self._pbo_mouse_func('pob', 1))
                mods.isclicked(self.mouse_rect, self.setting_text_rects[SETTINGS_DICT_POB_DOWN_OPT_KEY], self.mouse_clicked, lambda: self._pbo_mouse_func('pob', 2))
                
                self.setting_option_background_rects = []
                
                for i in [(i, k) if ' opt' not in i else 'skip' for i, k in self.setting_text_rects.items()]:
                    if i != 'skip':
                        height = 55
                        x = height
                        width = self.SCR_WIDTH - (x * 2)
                        
                        background_rect = pygame.Rect(x,
                                                    i[1].y - Y_SETTINGS_SPACE_OFFSET/2,
                                                    width,
                                                    height
                                                    )
                        self.setting_option_background_rects.append(background_rect)
                
                for i in self.setting_option_background_rects:
                    mods.isclicked(self.mouse_rect, i, self.mouse_clicked, lambda: self._setting_mouse_func(i))

                if event.type == pygame.KEYDOWN:
                    last_opt_index = (len(self.settings_dict_keys) - 3) // 2
                    
                    def key_up_or_down_pressed_for_settings(direction_moved: int):
                        self.widg_focused_sound.play()
                        self.pob_focus = 1
                        prev_setting_focus = self.setting_focus
                        self.setting_focus += direction_moved
                        self.setting_focus = pygame.math.clamp(self.setting_focus, 0, last_opt_index)
                        if prev_setting_focus != self.setting_focus:
                            self._save_and_apply_settings()
                    
                    if self.keys[pygame.K_UP] and not self.settings_disabled and self.setting_focus != 0:
                        key_up_or_down_pressed_for_settings(-1)
                    
                    elif self.keys[pygame.K_DOWN] and not self.settings_disabled and self.setting_focus != last_opt_index:
                        key_up_or_down_pressed_for_settings(1)
                    
                    if self.settings_dict_keys[self.setting_focus] == SETTINGS_DICT_POB_KEY:
                        if not self.settings_disabled:
                            if self.keys[pygame.K_LEFT]:
                                self.pob_focus -= 1
                                self.widg_focused_sound.play()
                            elif self.keys[pygame.K_RIGHT]:
                                self.pob_focus += 1
                                self.widg_focused_sound.play()
                            self.pob_focus = pygame.math.clamp(self.pob_focus, 1, 2)
                        
                        if self.keys[pygame.K_RETURN]:
                            self.widg_clicked_sound.play()
                    else:
                        if not self.settings_disabled:
                            if self.keys[pygame.K_RETURN]:
                                self._save_and_apply_settings()

            if not self.multiplayer_scr and not self.multiplayer_scr_bt and not self.multiplayer_scr_serv:
                for i in self.rects_rects:
                    if mods.isclicked(self.mouse_rect, i, self.mouse_clicked, lambda: self._main_menu_mouse_func(i)):
                        self._main_menu_activated_actions()
            
            if self.multiplayer_scr_bt:
                if self.keys[pygame.K_ESCAPE]:
                    self._exit_button_was_pressed()
            
            if event.type == pygame.KEYDOWN:
                main_multiplayer_scr = not self.multiplayer_scr and not self.multiplayer_scr_bt and not self.multiplayer_scr_serv
                end_of_widg_index = len(self.rects_name) - 1
                if main_multiplayer_scr:
                    if self.keys[pygame.K_RETURN]:
                        self._main_menu_activated_actions()
                   
                    if self.keys[pygame.K_UP] and self.start_focus != 0:
                        self.widg_focused_sound.play()
                        self.start_focus -= 1
                    if self.keys[pygame.K_DOWN] and self.start_focus != end_of_widg_index:
                        self.widg_focused_sound.play()
                        self.start_focus += 1
                else:
                    if self.keys[pygame.K_RETURN]:
                        self._mult_save_and_apply()
                        self.widg_clicked_sound.play()
    
    def main_menu_scr(self):
        if self.start_blitting:
            start_outline = pygame.Rect(self.start_text_rects[self.rects_name[self.start_focus]].x - X_WIDG_SPACE_OFFSET//2,
                                        self.start_text_rects[self.rects_name[self.start_focus]].y,
                                        self.start_texts[self.rects_name[self.start_focus]].get_width() + X_WIDG_SPACE_OFFSET,
                                        self.start_texts[self.rects_name[self.start_focus]].get_height())
            
            pygame.draw.rect(self.screen, self.FG_COLOR, start_outline, FOCUS_RECT_WIDTH, BORDER_RAD, BORDER_RAD, BORDER_RAD, BORDER_RAD, BORDER_RAD)
            
            self.screen.blit(self.main_title_surf, self.main_title_rect)
            
            for i in [k for k, _ in self.start_texts.items()]:
                self.screen.blit(self.start_texts[i], self.start_text_rects[i])
        else:
            self._randomize_load_timer()
            self._loading_scr('Loading')
            self._load_timer(self.loading_timer)
    
    def main_menu_loop(self):
        if self.multiplayer_scr:
            self.multiplayer()
        elif self.multiplayer_scr_bt:
            self._bt_multiplayer__blitting()
        elif self.multiplayer_scr_serv:
            self._server_multiplayer__blitting()
        else:
            self.main_menu_scr()
    
    
    def run(self):
        while True:
            self.update()
            
            if self.started:
                for event in pygame.event.get():
                    self.game_event_loop(event)
                
                self.game_main_loop()
            
            else:
                self.main_menu_update()

                for event in pygame.event.get():
                    self.main_menu_event_loop(event)
                
                self.main_menu_loop()
            
            pygame.display.update()




