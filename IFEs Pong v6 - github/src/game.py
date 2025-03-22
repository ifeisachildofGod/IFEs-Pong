
import sys
import json
import time
import math
import socket
import random
from typing import Any, Callable, Sequence, Tuple, Union
import pygame
import asyncio
import webbrowser
import bleak as bk
import bluetooth as bt
import threading as thread

from pygame.event import Event
from src.game_objects import Ball, Player
import src.functions as mods

from src.user_interface import Button, Input, Selector, InputSeletor, ClickableText
from src.constants import *


Coordinate = Union[Tuple[float, float], Sequence[float], pygame.Vector2]


# Main game
class Game(pygame.Surface):
    def __init__(self, size: Coordinate):
        super().__init__(size, pygame.SRCALPHA)
        pygame.init()
        
        self.display = pygame.display.set_mode(size)
        
        self.game_title = 'IFEs Pong'
        pygame.display.set_caption(self.game_title)
        
        self.SCR_WIDTH, self.SCR_HEIGHT = size
        
        logo = pygame.image.load(LOGO_PNG_PATH)
        pygame.display.set_icon(logo)
        
        self.clock = pygame.time.Clock()
        
        self.id = 0
        
        self.screen: Screen
        self.screens: dict[int, Screen] = {}
        
        self.FPS = 60
        
        self.clock = pygame.time.Clock()
        self.delta_time = 0
        
        self.save = Save(self)
        
        self.game_init_processor = ProcessGame(self, SCREEN_KEYS, SCREEN_TREE)
        self.game_init_processor.start()
    
    def loop(self):
        while True:
            self.delta_time = self.clock.tick(self.FPS)
            self.fill(self.save.get(SETTINGS_DICT_BG_KEY))
            
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    self.set_screen(END_SCREEN)
                
                self.screen.update_event(event)
            
            self.screen.update()
            self.screen._draw()
            
            self.blit(self.screen, self.screen.rect)
            self.display.blit(self, self.get_rect(center=(self.display.get_width() / 2, self.display.get_height() / 2)))
            
            pygame.display.update()
    
    def get(self, _id: int):
        return self.screens[_id]
    
    def set_screen(self, _id: int):
        self.id = _id
        self.screen = self.screens[self.id]
        # print(self.id)
    
    def add(self, screen: 'Screen', _id: int):
        self.screens[_id] = screen


# Non screen related
class ProcessGame:
    def __init__(self, game: Game, screen_keys, screen_tree):
        self.game = game
        self.screen_keys = screen_keys
        self.screen_dicts: dict[int, Screen] = {}
        self.screen_tree = screen_tree
    
    def start(self):
        self._process_game(self.screen_tree)
        
        for _, obj in self.screen_dicts.items():
            obj._init_later()
        
        self.game.set_screen(START_SCREEN)
    
    def _find_branch(self, tree: dict[int, dict | str], branch: int):
        for tree_id, tree_values in tree.items():
            if isinstance(tree_values, dict):
                if branch == tree_id:
                    return tree_values
                else:
                    future_branch = self._find_branch(tree_values[OTHER_LINKS], branch)
                    if future_branch == -1:
                        continue
                    return future_branch
            else:
                if branch == tree_id:
                    if tree_values == DEFAULT:
                        continue
        
        return -1
    
    def _process_game(self, branch: dict[int, dict[str, dict[int, dict]]] | str):
        if not isinstance(branch, str):
            for tree_id, tree_dict in branch.items():
                screen_class, args = self.screen_keys[tree_id]
                
                if isinstance(tree_dict, dict):
                    action_link = tree_dict[ACTION_LINK]
                    link_args = list(tree_dict[OTHER_LINKS].keys())
                    
                    if isinstance(action_link, dict):
                        link = list(action_link.keys())[0]
                        self.screen_dicts[tree_id] = screen_class(self.game, tree_id, link, link_args, *args)
                        self._process_game(action_link)
                    else:
                        self.screen_dicts[tree_id] = screen_class(self.game, tree_id, action_link, link_args, *args)
                    
                    self._process_game(tree_dict[OTHER_LINKS])

class PyBlue:
    def __init__(self, auth_key: str, port: int, max_connect_amt: int, comm_addr: str | None = None):
        self.auth_key = auth_key
        self.port = port
        self.max_connect_amt = max_connect_amt
        self.comm_addr = comm_addr
        
        self._search_info = []
        
        self._scanned = False
        self.status = 0
        self.retry_timer = 0
        
        self.ble_scanner = bk.BleakScanner()
    
    def _scan(self, start_delay_ms: int):
        time.sleep(start_delay_ms)
        
        try:
            self.status = 0.5
            bc_address_info = bt.discover_devices(lookup_names=True)
            ble_address_info = [(bl_info.address, bl_info.name) for bl_info in asyncio.run(self.ble_scanner.discover())]
            
            self._search_info = bc_address_info + [info for info in ble_address_info if info not in bc_address_info]
            self.status = 1
        except OSError:
            self.status = -1
        finally:
            self._scanned = True
    
    def authenticate(self):
        # bt_key = 'Ifechukwu is the oga and there is nothing anyone can do about that'
        if self.comm_addr is None:
            raise Exception("No address to be authenticatated has been provided")

        with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as bt_comm:
            try:
                self.status = 1.5
                bt_comm.connect((self.comm_addr, self.port))
                
                bt_comm.send(self.auth_key.encode())
                key_recv = bt_comm.recv(1024).decode()
                if key_recv == self.auth_key:
                    self.status = 2
                    self._search_info = []
                    return True
                else:
                    self.retry_timer += 1
                
                if self.retry_timer > self.max_connect_amt:
                    self.status = -2
            except (TimeoutError, OSError):
                # if self.bt_authenticate_tries_counter < MAX_BT_RETRY:
                #     self.bt_authenticate_tries_counter += 1
                #     self.authenticate(self.comm_addr)
                # else:
                self.status = -2
    
    def communicate(self, info: dict) -> dict[str, Any]:
        if self.comm_addr is None:
            raise Exception("Bluetooth communication has been closed")
        
        self.status = 2.5
        with socket.socket(socket.AF_BLUETOOTH, socket.SOCK_STREAM, socket.BTPROTO_RFCOMM) as bt_comm:
            bt_comm.connect((self.comm_addr, self.port))
            
            bt_comm.send(json.dumps(info, indent=2).encode())
            recv = json.loads(bt_comm.recv(1024).decode())
            
            self.status = 3
        
        return recv
    
    def scan(self, start_delay_ms: int):
        if not self._scanned:
            self.start_bt_search = thread.Thread(target=lambda: self._scan(start_delay_ms))
            self.start_bt_search.daemon = True
            self.start_bt_search.start()
    
    def get(self):
        return self._search_info
    
    def select_addr(self, index: int):
        self.comm_addr = self._search_info[index][0]
    
    def close(self):
        self.comm_addr = None
        self.status = 0
        self._search_info = []

class OptionSelector:
    def __init__(self, game: Game, centerx: float, y: float, font: pygame.font.Font, color: ColorType, options: list[Tuple[str, int, Callable[[], None] | None]]):
        self.game = game
        self.game = game
        
        self.options = options
        self.color = color
        self.font = font
        
        self.focus = -0
        
        self.option_spacing = 10
        self.option_outline_padding_x = 20
        self.option_outline_border_width = 2
        self.option_outline_border_radius = 10
        
        self.options_processed = {
            name: (self.font.render(name, False, self.color), (centerx - ((((index%2) * (2 if index + 1 != len(self.options) else 0)) - 1) * ((len(name) * self.font.get_height()) + 50)), y + index * (self.option_spacing + self.font.get_height())), screen_id, func)
            for index, (name, screen_id, func) in enumerate(self.options)
        }
        self.option_rects_processed = {
            (name, screen_id): (surf.get_rect(midtop=pos), func) for name, (surf, pos, screen_id, func) in self.options_processed.items()
        }
        self.option_outline_rects_processed = {
            key: (pygame.Rect(rect.x - self.option_outline_padding_x//2, rect.y, rect.width + self.option_outline_padding_x, rect.height), func)
            for key, (rect, func) in self.option_rects_processed.items()
        }
    
    def _m_mouse_hover_func(self, index):
        def func():
            self.focus = index
        
        return func
    
    def update(self):
        mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        for index, ((_, _id), (rect, func)) in enumerate(self.option_outline_rects_processed.items()):
            if mods.isclicked(mouse_rect, rect, mouse_clicked, self._m_mouse_hover_func(index)):
                if isinstance(func, Callable):
                    func()
                self.game.set_screen(_id)
    
    def draw(self):
        for name, (surf, _, _id, _) in self.options_processed.items():
            self.game.screen.blit(surf, self.option_rects_processed[(name, _id)][0])
        
        outline_rect, _ = list(self.option_outline_rects_processed.values())[self.focus]
        
        pygame.draw.rect(self.game.screen, self.color, outline_rect, self.option_outline_border_width, self.option_outline_border_radius, self.option_outline_border_radius, self.option_outline_border_radius, self.option_outline_border_radius, self.option_outline_border_radius)

class Save:
    def __init__(self, game: Game, path: str = DATA_PATH) -> None:
        self.game = game
        self.path = path
        self.save_func_dict = {}
        
        self.load()
    
    def add_saveables(self, save_func_dict: dict[str, Callable[[], Any]]):
        self.save_func_dict.update(save_func_dict)
    
    def remove_saveables(self, saveable_names: list[str]):
        for name in saveable_names:
            if name in self.save_func_dict:
                self.save_func_dict.pop(name)
    
    def load(self):
        try:
            with open(self.path) as file:
                self.reset()
                data = json.load(file)
                
                if list(data.keys()) == list(self.data.keys()):
                    self.data = data
        except Exception as e:
            print(e)
        finally:
            self.reset
    
    def get(self, key: str):
        return self.data[key]
    
    def save(self):
        for name, func in self.save_func_dict.items():
            self.data[name] = func()
        
        for _, screen in self.game.game_init_processor.screen_dicts.items():
            screen._on_save()
        
        with open(self.path, 'w') as file:
            json.dump(self.data, file, indent=2)

    def reset(self):
        self.data = {
            SETTINGS_DICT_BG_KEY: "black",
            SETTINGS_DICT_FG_KEY: "white",
            SETTINGS_DICT_POB_KEY + "0": [
                "w",
                119
            ],
            SETTINGS_DICT_POB_KEY + "1": [
                "s",
                115
            ],
            SETTINGS_DICT_PTB_KEY + "0": [
                "UP",
                1073741906
            ],
            SETTINGS_DICT_PTB_KEY + "1": [
                "DOWN",
                1073741905
            ],
            SETTINGS_DICT_P1C_KEY: 1,
            SETTINGS_DICT_P2C_KEY: 2,
            SETTINGS_DICT_AI_KEY: 1,
            
            
            SCORE_SAVE_KEY: [
                1,
                4
            ],
            P1_Y_POS_SAVE_KEY: 246,
            P2_Y_POS_SAVE_KEY: 277,
            BALL_POS_SAVE_KEY: [
                604,
                225
            ],
            BALL_DIR_SAVE_KEY: [
                1.2,
                -0.1
            ],
            
            MPO_BG_COLOR_KEY: "black",
            MPO_FG_COLOR_KEY: "white",
            MPO_DATA_KEY: 0,
            MPO_PC_KEY: 1,
            MPO_PB_KEY + "0": [
                "w",
                119
            ],
            MPO_PB_KEY + "1": [
                "s",
                115
            ]
        }
    



# Base screen class
class Screen(pygame.Surface):
    def __init__(self, game: Game, _id: int, action_id: int | None, link_id_args: list[int]):
        super().__init__((game.SCR_WIDTH, game.SCR_HEIGHT), pygame.SRCALPHA)
        
        self.game = game
        self._id = _id
        self.action_id = action_id
        self.link_id_args = link_id_args
        
        self.fps_font = mods.make_font(1, 15)
        
        on_focus_widg_vol = .2
        on_clicked_widg_vol = .2
        self.button_sound_info = ((ONWIDGETCLICKED_MP3_PATH, on_clicked_widg_vol), (ONWIDGETFOCUS_WAV_PATH, on_focus_widg_vol))
        
        self.action_button = Button(self, self.game.save.get(SETTINGS_DICT_FG_KEY), (10, 10), 20, sound_info=self.button_sound_info)
        
        self._draw_buffer = []
        
        self.rect = self.get_rect(center=self.game.get_rect().center)
        self.game.add(self, self._id)
        
        self._updated = False
    
    def update(self):
        self._update_action_button()
        
        fps_surf = self.fps_font.render(f"FPS: {int(self.game.clock.get_fps())}", True, self.game.save.get(SETTINGS_DICT_FG_KEY))
        fps_rect = fps_surf.get_rect(topright=(self.game.SCR_WIDTH, 5))
        
        self._draw_buffer.append(("blit", (fps_surf, fps_rect), None))
        
        if isinstance(self.action_id, int):
            self._draw_buffer.append((self.action_button.draw, None, None))
        
        self._updated = True
    
    def update_event(self, event: pygame.event.Event):
        pass
    
    def copy(self):
        return Screen(self.game, self._id, self.action_id, self.link_id_args)
    
    def _on_save(self):
        pass
    
    def _init_later(self):
        pass
    
    def _update_action_button(self):
        if isinstance(self.action_id, int):
            self.action_button.update(pygame.Rect(pygame.mouse.get_pos(), (1, 1)), pygame.mouse.get_pressed()[0], self._activate_button_clicked)
    
    def _activate_button_clicked(self):
        if isinstance(self.action_id, int):
            self.game.set_screen(self.action_id)
    
    def _draw(self):
        self.fill(self.game.save.get(SETTINGS_DICT_BG_KEY))
        
        for draw_type, draw_args, draw_kwargs in self._draw_buffer:
            draw_args = draw_args if draw_args is not None else []
            draw_kwargs = draw_kwargs if draw_kwargs is not None else {}
            
            if "rect" == draw_type:
                pygame.draw.rect(self, *draw_args, **draw_kwargs)
            elif "circle" == draw_type:
                pygame.draw.circle(self, *draw_args, **draw_kwargs)
            elif "line" == draw_type:
                pygame.draw.line(self, *draw_args, **draw_kwargs)
            elif "blit" == draw_type:
                self.blit(*draw_args, **draw_kwargs)
            elif callable(draw_type):
                draw_type(*draw_args, **draw_kwargs)
        
        if self._updated:
            self._draw_buffer.clear()
            self._updated = False


# Utility Screens
class InfoDisplayScreen(Screen):
    def __init__(self, game: Game, _id: int, action_id: int | None, link_id_args: list[int], info: str, delay_s: int):
        super().__init__(game, _id, action_id, link_id_args)
        self.info = info
        self.delay_s = delay_s
        self.next_screen_id, = self.link_id_args
        
        self.start_time = 0
        self.curr_time = 0
        self.started_timer = False
        
        self.load_timer = 0
        self.font = mods.make_font(2, 30)
        self.load_dot_amount = 0
    
    def update(self):
        super().update()
        
        if not self.started_timer:
            self.start_time = time.time()
            self.started_timer = True
        self.curr_time = time.time()
        
        self.load_timer += 1
        if self.load_timer % 50 == 0:
            self.load_dot_amount += 1
            self.load_timer = 1
        if self.load_dot_amount > 5:
            self.load_dot_amount = 1
        
        load_surf = self.font.render(self.info + ('.' * self.load_dot_amount), False, self.game.save.get(SETTINGS_DICT_FG_KEY))
        load_rect = load_surf.get_rect(center=(self.game.SCR_WIDTH / 2, self.game.SCR_HEIGHT / 2))
        
        self._draw_buffer = [["blit", (load_surf, load_rect), None]]
        
        if self.curr_time - self.start_time >= self.delay_s:
            self.game.set_screen(self.next_screen_id)

# Display Screens
class BlueLobbyScreen(Screen):
    def __init__(self, game: Game, _id: int, action_id: int | None, link_id_args: list[int], blue: PyBlue):
        super().__init__(game, _id, action_id, link_id_args)
        self.y = 130
        self.title_text_offset = 10
        
        self.auth_load_screen_id, = link_id_args
        self.blue = blue
        
        title_font = mods.make_font(3, 40)
        self.info_font = mods.make_font(2, 20)
        
        self.title_surf = title_font.render('Bluetooth Lobby', False, self.game.save.get(SETTINGS_DICT_FG_KEY))
        self.title_rect = self.title_surf.get_rect(center=(self.game.SCR_WIDTH / 2, self.title_surf.get_height()))
        
        self.clickable_texts: list[ClickableText] = []
    
    def _m_addr_select_func(self, index):
        def func():
            self.blue.select_addr(index)
            self.game.set_screen(self.auth_load_screen_id)
        
        return func
    
    def _draw(self):
        super()._draw()
        
        for ct in self.clickable_texts:
            ct.draw(None)
    
    def update(self):
        super().update()
        mouse_rect= pygame.Rect(pygame.mouse.get_pos(), (1, 1))
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        self.blue.scan(1000)
        
        if self.blue.status == 1:
            self.clickable_texts = []
            for index, clickable_info in enumerate(self.blue.get()):
                text = f'{clickable_info[1] if clickable_info[1] else '_'} : {clickable_info[0]}'
                y = (self.info_font.render(text, False, self.game.save.get(SETTINGS_DICT_FG_KEY)).get_height() + self.title_text_offset) * index + self.y
                ct = ClickableText(self, text, self.info_font, self.game.save.get(SETTINGS_DICT_FG_KEY), self.game.save.get(SETTINGS_DICT_BG_KEY), (130, y), sound_info=self.button_sound_info)
                
                sn = self.info_font.render(f'{index + 1}.', False, self.game.save.get(SETTINGS_DICT_FG_KEY))
                sn_rect = sn.get_rect(midright=(ct.hover_rect.left - 30 , ct.hover_rect.centery))
                
                self.clickable_texts.append(ct)
                
                self._draw_buffer.append(["blit", (sn, sn_rect), None])
            
            self.blue.status = 1.1
        
        for index, ct in enumerate(self.clickable_texts):
            ct.update(mouse_rect, mouse_clicked, self._m_addr_select_func(index))

class WelcomeScreen(Screen):
    def __init__(self, game: Game, _id: int, action_id: int | None, link_id_args: list[int]):
        super().__init__(game, _id, action_id, link_id_args)
        self.title_hover_bounce = 0
        
        self.title_font = mods.make_font(4, 200)
        
        self.title_surf = self.title_font.render("IFEs Pong", False, self.game.save.get(SETTINGS_DICT_FG_KEY))
        self.title_rect = self.title_surf.get_rect(center=(self.game.SCR_WIDTH / 2, self.title_surf.get_height() - (self.title_surf.get_height() / 4)))
    
    def _init_later(self):
        continue_id, new_game_id, multiplayer_id, exit_id = self.link_id_args
        self.option_selector = OptionSelector(self.game, self.game.SCR_WIDTH / 2, self.title_rect.bottom + 40, mods.make_font(1, 20), self.game.save.get(SETTINGS_DICT_FG_KEY), [("Continue", continue_id, None), ("New Game", new_game_id, self.game.save.reset), ("Multiplayer", multiplayer_id, None), ("Exit", exit_id, None)])
    
    def _draw(self):
        super()._draw()
        
        self.option_selector.draw()
    
    def update(self):
        super().update()
        
        self.title_hover_bounce += 2
        self.title_hover_bounce = self.title_hover_bounce % 360
        
        y_floating_offset = int(math.sin(math.radians(self.title_hover_bounce)) * 3)
        self.title_rect.y += y_floating_offset
        
        self._draw_buffer.append(["blit", (self.title_surf, self.title_rect), None])
        self.option_selector.update()

class PauseScreen(Screen):
    def __init__(self, game: Game, _id: int, action_id: int | None, link_id_args: list[int]):
        super().__init__(game, _id, action_id, link_id_args)
        self.title_font = mods.make_font(4, 100)
        
        self.title_surf = self.title_font.render("Game Paused", False, self.game.save.get(SETTINGS_DICT_FG_KEY))
        self.title_rect = self.title_surf.get_rect(center=(self.game.SCR_WIDTH / 2, self.title_surf.get_height() - (self.title_surf.get_height() / 4)))
    
    def _init_later(self):
        resume_id, settings_id, info_id, main_menu_id, restart_id, exit_id = self.link_id_args
        self.option_selector = OptionSelector(self.game, self.game.SCR_WIDTH / 2, self.title_rect.bottom + 40, mods.make_font(1, 20), self.game.save.get(SETTINGS_DICT_FG_KEY), [("Resume", resume_id, None), ("Settings", settings_id, None), ("Information", info_id, None), ("Main Menu", main_menu_id, None), ("Restart", restart_id, None), ("Exit", exit_id, None)])
    
    def _draw(self):
        super()._draw()
        
        self.option_selector.draw()
    
    def update(self):
        super().update()
        self._draw_buffer.append(("blit", (self.title_surf, self.title_rect), None))
        self.option_selector.update()

class GameScreen(Screen):
    def __init__(self, game: Game, _id: int, action_id: int | None, link_id_args: list[int], blue: PyBlue):
        super().__init__(game, _id, action_id, link_id_args)
        self.blue = blue
        
        self.control_info_font = mods.make_font(1, 10)
        
        self._bt_exit_status = 0
        
        self.get_save_func: dict[str, Callable[[], Any]] = {}
        
        self.score_cell_size = 15
        
        self.player_speed = 0.7
        self.player_size = 20, 70
        self.player_x_offset = 40
        
        self.ball_speed = 0.4
        self.ball_radius = 10
        
        self.mid_line_width = 3
        self.mid_line_length = 20
        self.mid_line_spacing = 5
        
        self.player1_score = self.player2_score = 0
    
    def _init_later(self):
        setting_id, = self.link_id_args
        settings = self.game.get(setting_id)
        
        if isinstance(settings, SettingsScreen):
            self.settings = settings
        
        self.p1_control_info_surf = self.control_info_font.render(CONTROL_OPTIONS[self.settings.get(SETTINGS_DICT_P1C_KEY)], False, self.game.save.get(SETTINGS_DICT_FG_KEY))
        self.p2_control_info_surf = self.control_info_font.render(CONTROL_OPTIONS[self.settings.get(SETTINGS_DICT_P2C_KEY)], False, self.game.save.get(SETTINGS_DICT_FG_KEY))
        
        self.player1 = Player(self, (self.player_x_offset, self.game.save.get(P1_Y_POS_SAVE_KEY)), self.player_size, True)
        self.player2 = Player(self, (self.game.SCR_WIDTH - self.player_x_offset - self.player_size[0], self.game.save.get(P2_Y_POS_SAVE_KEY)), self.player_size, False)
        self.ball = Ball(self, self.game.save.get(BALL_POS_SAVE_KEY), self.ball_radius, self.game.save.get(BALL_DIR_SAVE_KEY), self.game.save.get(SCORE_SAVE_KEY))
        
        self.get_save_func[P1_Y_POS_SAVE_KEY] = lambda: self.player1.get_rect_info()[0].centery
        self.get_save_func[P2_Y_POS_SAVE_KEY] = lambda: self.player2.get_rect_info()[0].centery
        self.get_save_func[BALL_DIR_SAVE_KEY] = lambda: self.ball.get_rect_info()[1]
        self.get_save_func[BALL_POS_SAVE_KEY] = lambda: self.ball.get_rect_info()[0].center
        self.get_save_func[SCORE_SAVE_KEY] = lambda: self.ball.get_score()
        
        self.game.save.add_saveables(self.get_save_func)
    
    def _get(self):
        keys = pygame.key.get_pressed()
        
        return dict(control_type=self.settings.get("p1_control_type"), movement=(keys[self.settings.get("p1_key_control_up")], keys[self.settings.get("p1_key_control_down")]), color=self.game.save.get(SETTINGS_DICT_FG_KEY), mouse_pos=pygame.mouse.get_pos(), exit_status=self._bt_exit_status)
    
    def _exit_bt_game(self):
        self._bt_exit_status = 1
        self.blue.communicate(self._get())
    
    def _update_bluetooth_game(self):
        mouse_pos = pygame.mouse.get_pos()
        
        blue_info = self.blue.communicate(self._get())
        
        ball_rect_info = self.ball.get_rect_info()
        player1_rect_info = self.player1.get_rect_info()
        player2_rect_info = self.player2.get_rect_info()
        self.player1_score, self.player2_score = self.ball.get_score()
        
        self._bt_exit_status = blue_info["exit_status"]
        
        self.ball.update(1 / self.game.FPS, (player1_rect_info, player2_rect_info), self.game.save.get(SETTINGS_DICT_FG_KEY))
        
        self.player1.update(MPO_CONTROL_OPTIONS[self.settings.get(MPO_PC_KEY)], ball_rect_info, mouse_pos, self.player_speed / self.game.FPS, (self.settings.get(MPO_PB_KEY + "0"), self.settings.get(MPO_PB_KEY + "1")), AI_DIFFICULTY_OPTIONS[self.settings.get(SETTINGS_DICT_AI_KEY)], self.game.save.get(SETTINGS_DICT_FG_KEY))
        self.player2.update(blue_info["control_type"], ball_rect_info, blue_info["mouse"], self.player_speed / self.game.FPS, blue_info["movement"], self.settings.get("ai_difficulty"), blue_info["color"])
        
        if self._bt_exit_status:
            self.blue.close()
            self.game.set_screen(3)
    
    def _update_normal_game(self):
        mouse_pos = pygame.mouse.get_pos()
        
        ball_rect_info = self.ball.get_rect_info()
        player1_rect_info = self.player1.get_rect_info()
        player2_rect_info = self.player2.get_rect_info()
        self.player1_score, self.player2_score = self.ball.get_score()
        
        self.ball.update(self.game.delta_time, (player1_rect_info, player2_rect_info), self.game.save.get(SETTINGS_DICT_FG_KEY))
        
        self.player1.update(CONTROL_OPTIONS[self.settings.get(SETTINGS_DICT_P1C_KEY)], ball_rect_info, mouse_pos, self.player_speed * self.game.delta_time, (self.settings.get(SETTINGS_DICT_POB_KEY + "0"), self.settings.get(SETTINGS_DICT_POB_KEY + "1")), AI_DIFFICULTY_OPTIONS[self.settings.get(SETTINGS_DICT_AI_KEY)], self.game.save.get(SETTINGS_DICT_FG_KEY))
        self.player2.update(CONTROL_OPTIONS[self.settings.get(SETTINGS_DICT_P2C_KEY)], ball_rect_info, mouse_pos, self.player_speed * self.game.delta_time, (self.settings.get(SETTINGS_DICT_PTB_KEY + "0"), self.settings.get(SETTINGS_DICT_PTB_KEY + "1")), AI_DIFFICULTY_OPTIONS[self.settings.get(SETTINGS_DICT_AI_KEY)], self.game.save.get(SETTINGS_DICT_FG_KEY))
    
    def _draw_midline(self):
        for i in range(int(self.game.SCR_HEIGHT // self.mid_line_length)):
            spacing = self.mid_line_spacing + (i * self.mid_line_length)
            
            l_x_pos = self.game.SCR_WIDTH / 2
            self._draw_buffer.append(["line", (self.game.save.get(SETTINGS_DICT_FG_KEY), (l_x_pos, spacing), (l_x_pos, spacing + self.mid_line_length), self.mid_line_width), None])
    
    def _on_save(self):
        self.p1_control_info_surf = self.control_info_font.render(CONTROL_OPTIONS[self.settings.get(SETTINGS_DICT_P1C_KEY)], False, self.game.save.get(SETTINGS_DICT_FG_KEY))
        self.p2_control_info_surf = self.control_info_font.render(CONTROL_OPTIONS[self.settings.get(SETTINGS_DICT_P2C_KEY)], False, self.game.save.get(SETTINGS_DICT_FG_KEY))
    
    def reset(self):
        self.player1.rect.centery = int(self.game.SCR_HEIGHT / 2)
        self.player2.rect.centery = int(self.game.SCR_HEIGHT / 2)
        self.ball.rect.center = (int(self.game.SCR_WIDTH // 2), int(self.game.SCR_HEIGHT // 2))
        self.ball.x_dir = random.randint(-1, 1)
        self.ball.y_dir = random.randint(-1, 1)
        if not self.ball.x_dir:
            self.ball.x_dir = random.choice([-1, 1])
        self.ball.p1_score = 0
        self.ball.p2_score = 0
        
    def update(self):
        super().update()
        
        if self.blue.status == 2:
            self._update_bluetooth_game()
        elif self.blue.status == 0:
            self._update_normal_game()
        
        self._draw_buffer.append((mods.draw_nums, (self, self.player1_score, 0, self.score_cell_size, False, self.game.save.get(SETTINGS_DICT_FG_KEY)), None))
        self._draw_buffer.append((mods.draw_nums, (self, self.player2_score, 0, self.score_cell_size, True, self.game.save.get(SETTINGS_DICT_FG_KEY)), None))
        self._draw_buffer.append((self._draw_midline, None, None))
        self._draw_buffer.append((self.ball.draw, None, None))
        self._draw_buffer.append((self.player1.draw, None, None))
        self._draw_buffer.append((self.player2.draw, None, None))
        self._draw_buffer.append(("blit", (self.p1_control_info_surf, self.p1_control_info_surf.get_rect(bottomleft=(0, self.game.SCR_HEIGHT))), None))
        self._draw_buffer.append(("blit", (self.p2_control_info_surf, self.p2_control_info_surf.get_rect(bottomright=(self.game.SCR_WIDTH, self.game.SCR_HEIGHT))), None))

class InfoScreen(Screen):
    def __init__(self, game: Game, _id: int, action_id: int | None, link_id_args: list[int]):
        super().__init__(game, _id, action_id, link_id_args)
        self.y = 70
        
        self.mouse_scroll_y = 0
        self.title_font = mods.make_font(2, 26)
        self.text_font = mods.make_font(2, 15)
        self.link_color = mods.set_color(self.game.save.get(SETTINGS_DICT_FG_KEY), 125)
        
        self.title_surf = self.title_font.render("Information", False, self.game.save.get(SETTINGS_DICT_FG_KEY))
        
        self.ptr_u_d_width = 12
        self.ptr_u_d_height = 8
        self.ptr_u_d_x = self.game.SCR_WIDTH - self.ptr_u_d_width - 12
        self.ptr_u_y = 10
        self.ptr_d_y = self.game.SCR_HEIGHT - self.ptr_u_d_height - self.ptr_u_y
        
        self.scr_focus = 0
        
        self.ptr_up = Button(self, self.game.save.get(SETTINGS_DICT_FG_KEY), (self.ptr_u_d_x + 1, self.ptr_u_y), (self.ptr_u_d_width, self.ptr_u_d_height), border_radius=0)
        self.ptr_down = Button(self, self.game.save.get(SETTINGS_DICT_FG_KEY), (self.ptr_u_d_x + 1, self.ptr_d_y), (self.ptr_u_d_width, self.ptr_u_d_height), border_radius=0)
        
        self.ptr_rect_up = self.ptr_up.rect.copy()
        self.ptr_rect_down = self.ptr_down.rect.copy()
        
        info_texts_size = max([rect[1].y for rect in mods.multiline_write((0, self.y), HELP_INFO, self.text_font, 'blue', 'blue')[0]]) - (self.game.SCR_HEIGHT / 2)
        self.info_scr_wheel_height = (self.game.SCR_HEIGHT / info_texts_size) * (self.ptr_rect_down.top - self.ptr_rect_up.bottom)
        
        self.scr_wheel_y = self.ptr_rect_up.bottom
        
        self.info_scroll_wheel = Button(self, self.game.save.get(SETTINGS_DICT_FG_KEY), (self.ptr_u_d_x, self.scr_wheel_y), (self.ptr_u_d_width, self.info_scr_wheel_height), border_radius=0)
        
        self.cursor_img = pygame.image.load(ONHOVER_PNG_PATH)
        self.cursor_img = pygame.transform.rotozoom(self.cursor_img, 0, .5)
        
        self.max_link_hit_rect = pygame.Rect(0, 0, 0, 0)
        self.mlhr_width = 0
        self.mouse_move = 0
        
        self.scroll_speed = 0.15
    
    def update_event(self, event):
        super().update_event(event)
        
        for event in pygame.event.get():
            if event.type == pygame.MOUSEWHEEL:
                self.mouse_scroll_y = event.dict['precise_y']
    
    def _on_hover_link(self, x, y):
        line_height = 30
        self._draw_buffer.append(["line", (self.link_color, (x, y + line_height), (x + self.txt_width, y + line_height), 2), None])
        pygame.mouse.set_visible(False)
        self._draw_buffer.append(["blit", (self.cursor_img, pygame.mouse.get_pos()), None])
    
    def _mouse_drag_movement(self):
        self.scr_wheel_y += pygame.mouse.get_rel()[1]
    
    def _scroll(self, up: bool):
        if up:
            self.scr_wheel_y -= self.scroll_speed * self.game.delta_time
        else:
            self.scr_wheel_y += self.scroll_speed * self.game.delta_time
    
    def _update_scroll(self):
        keys = pygame.key.get_pressed()
        
        self.scr_wheel_y -= self.mouse_move
        if keys[pygame.K_UP]:
            if self.ptr_rect_up.bottom < self.scr_wheel_rect.top:
                self._scroll(True)
        if keys[pygame.K_DOWN]:
            if self.ptr_rect_down.top > self.scr_wheel_rect.bottom:
                self._scroll(False)
        
        self.mouse_move = mods.special_calcualation(self.mouse_move, 0, .000000001)
        
        if keys[pygame.K_HOME]:
            self.scr_wheel_y = self.ptr_rect_up.bottom
        elif keys[pygame.K_END]:
            self.scr_wheel_y = self.ptr_rect_down.top - self.info_scr_wheel_height
    
    def update(self):
        super().update()
        
        mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
        mouse_clicked = pygame.mouse.get_pressed()[0]
        
        help_info_surf_list, list_val = mods.multiline_write((40, self.y), HELP_INFO, self.text_font, self.link_color, self.game.save.get(SETTINGS_DICT_FG_KEY))
        
        self.scr_wheel_y = pygame.math.clamp(self.scr_wheel_y, self.ptr_rect_up.bottom, self.ptr_rect_down.top - self.info_scr_wheel_height)
        self.scr_wheel_rect = pygame.Rect(self.ptr_u_d_x, self.scr_wheel_y, self.ptr_u_d_width, self.info_scr_wheel_height)
        
        self.info_scr_text_height = (self.game.SCR_HEIGHT * (self.ptr_rect_down.top - self.ptr_rect_up.bottom)) / self.info_scr_wheel_height
        scr_focus = self.info_scr_text_height * ((self.scr_wheel_y - self.ptr_rect_up.bottom) / (self.ptr_rect_down.top - self.info_scr_wheel_height))
        
        self.info_scroll_wheel.update(mouse_rect=mouse_rect, mouse_clicked=mouse_clicked, on_click=self._mouse_drag_movement, color=self.game.save.get(SETTINGS_DICT_FG_KEY), bounce_delay=0)
        self.info_scroll_wheel.rect.topleft = self.scr_wheel_rect.topleft
        
        help_scr_title_rect = self.title_surf.get_rect(midtop=(self.game.SCR_WIDTH / 2, min(self.y - scr_focus, self.info_scr_text_height) - 50))
        self._draw_buffer.append(["blit", (self.title_surf, help_scr_title_rect), None])
        
        list_of_linkrects_x = []
        list_of_linkrects_width = []
        list_of_linkrects = []
        for blit_index, blit_info in enumerate(help_info_surf_list):
            rect = blit_info[1]
            y = rect.y - scr_focus
            self.txt_width, t_height = rect.size
            self._draw_buffer.append(["blit", (blit_info[0], (rect.x, y)), None])
            
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
                
                if not mouse_rect.colliderect(self.max_link_hit_rect):
                    pygame.mouse.set_visible(True)
                else:
                    for i in dead_zone_list:
                        if mouse_rect.colliderect(i):
                            pygame.mouse.set_visible(True)
                
                if mouse_rect.colliderect(link_rect):
                    self._on_hover_link(rect.x, y)
                    if mouse_clicked:
                        if self.mouse_clicked_for_links:
                            link = LINKS[list_val[blit_index]]
                            link_starter = thread.Thread(target=lambda: webbrowser.open(link))
                            link_starter.daemon = True
                            link_starter.start()
                            self.mouse_clicked_for_links = False

            if list_val[blit_index] in HELP_SCR_HEADERS:
                line_height = y + 12
                self._draw_buffer.append(["line", (self.game.save.get(SETTINGS_DICT_FG_KEY), (rect.x, line_height), (rect.x + self.txt_width, line_height), 1), None])
        
        self.ptr_up.update(mouse_rect=mouse_rect, mouse_clicked=mouse_clicked, on_click=lambda: self._scroll(True), bounce_delay=0, color=self.game.save.get(SETTINGS_DICT_FG_KEY))
        self.ptr_down.update(mouse_rect=mouse_rect, mouse_clicked=mouse_clicked, on_click=lambda: self._scroll(False), bounce_delay=0, color=self.game.save.get(SETTINGS_DICT_FG_KEY))
        
        self._draw_buffer.append((self.info_scroll_wheel.draw, None, None))
        self._draw_buffer.append((self.ptr_up.draw, None, None))
        self._draw_buffer.append((self.ptr_down.draw, None, None))
        self._update_scroll()

class SettingsScreen(Screen):
    def __init__(self, game: Game, _id: int, action_id: int | None, link_id_args: list[int], *, _y: int | None = None, _options: list[Tuple[str, str, list]] | None = None):
        super().__init__(game, _id, action_id, link_id_args)
        
        self.focus = 0
        
        self.get_save_func: dict[str, Callable[[], Any]] = {}
        
        self.option_font = mods.make_font(3, 15)
        
        self.options_type_funcs = {
            "input": self._make_input,
            "selector": self._make_selector,
            "input_selector": self._make_input_selector,
        }
        
        options = _options if _options is not None else [
            (SETTINGS_DICT_BG_KEY, "input", [self.game.save.get(SETTINGS_DICT_BG_KEY)]),
            (SETTINGS_DICT_FG_KEY, "input", [self.game.save.get(SETTINGS_DICT_FG_KEY)]),
            (SETTINGS_DICT_AI_KEY, "selector", [AI_DIFFICULTY_OPTIONS, self.game.save.get(SETTINGS_DICT_AI_KEY)]),
            (SETTINGS_DICT_P1C_KEY, "selector", [CONTROL_OPTIONS, self.game.save.get(SETTINGS_DICT_P1C_KEY)]),
            (SETTINGS_DICT_P2C_KEY, "selector", [CONTROL_OPTIONS, self.game.save.get(SETTINGS_DICT_P2C_KEY)]),
            (SETTINGS_DICT_POB_KEY, "input_selector", [[("Player one up key binding", "Up: ", self.game.save.get(SETTINGS_DICT_POB_KEY + "0")), ("Player one down key binding", "Down: ", self.game.save.get(SETTINGS_DICT_POB_KEY + "1"))], ]),
            (SETTINGS_DICT_PTB_KEY, "input_selector", [[("Player one up key binding", "Up: ", self.game.save.get(SETTINGS_DICT_PTB_KEY + "0")), ("Player one down key binding", "Down: ", self.game.save.get(SETTINGS_DICT_PTB_KEY + "1"))], ]),
        ]
        
        option_padding = 25
        option_width = self.game.SCR_WIDTH / 1.5
        option_height = self.option_font.get_height() + (option_padding * 2)
        option_internal_gap = 20
        option_spacing = 20
        
        option_y = _y if _y is not None else (self.game.SCR_HEIGHT - ((option_height + option_spacing) * len(options))) / 2
        
        self.options_bg_processed = {
            name: [self.option_font.render(name, False, self.game.save.get(SETTINGS_DICT_BG_KEY)), self.option_font.render(name, False, self.game.save.get(SETTINGS_DICT_FG_KEY)), pygame.Rect((self.game.SCR_WIDTH - option_width) / 2, option_y + (index * (option_height + option_spacing)), option_width, option_height), option_type, args] for index, (name, option_type, args) in enumerate(options)
        }
        
        self.options_processed = {
            name: [(surf_fg, surf_bg), surf_fg.get_rect(midright=(bg_rect.centerx - option_internal_gap, bg_rect.centery)), self.options_type_funcs[option_type](name, bg_rect.centerx + option_internal_gap, bg_rect.centery, *args), bg_rect, option_type] for name, (surf_bg, surf_fg, bg_rect, option_type, args) in self.options_bg_processed.items()
        }
        
        self.game.save.add_saveables(self.get_save_func)
    
    def _make_opt_display_func(self, text: str, pos: Tuple[float, float]):
        surf_fg = self.option_font.render(text, False, self.game.save.get(SETTINGS_DICT_FG_KEY))
        surf_bg = self.option_font.render(text, False, self.game.save.get(SETTINGS_DICT_BG_KEY))
        
        return (surf_fg, surf_bg), surf_bg.get_rect(midleft=pos)
    
    def _make_input_selector_func(self, text: str, key_code: int):
        def func():
            return text, key_code
        
        return func
    
    def _make_input(self, name: str, x: float, centery: float, text: str):
        text_input = Input(self.game, text, 20, (x, centery), self.option_font, self.game.save.get(SETTINGS_DICT_FG_KEY))
        self.get_save_func[name] = lambda: text_input.tv_input
        
        return text_input, lambda: self._make_opt_display_func(text, (x, centery))
    
    def _make_selector(self, name: str, x: float, centery: float, options: list[str], index: int):
        selector = Selector(self, options, index, (x, centery), self.option_font, self.game.save.get(SETTINGS_DICT_FG_KEY), circular=True)
        self.get_save_func[name] = lambda: selector.index
        
        return selector, lambda: self._make_opt_display_func(options[index], (x, centery))
    
    def _make_input_selector(self, name: str, x: float, centery: float, options: list[Tuple[str, str, tuple[str, int]]]):
        input_selectors = []
        for index, (mini_win_name, prefix, character) in enumerate(options):
            input_selector = InputSeletor(self, character, self.game.save.get(SETTINGS_DICT_BG_KEY), self.game.save.get(SETTINGS_DICT_FG_KEY), mini_win_name, (x, centery), self.option_font, self.game.save.get(SETTINGS_DICT_FG_KEY), mini_win_logo_path = LOGO_PNG_PATH, _prefix=prefix)
            self.get_save_func[name + str(index)] = self._make_input_selector_func(input_selector.display_char, input_selector.display_ord)
            
            input_selectors.append((input_selector, lambda: self._make_opt_display_func(prefix + name, (x, centery))))
        
        return input_selectors
    
    def update_event(self, event: Event):
        keys = pygame.key.get_pressed()
        
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_UP]:
                self.focus -= 1
            elif keys[pygame.K_DOWN]:
                self.focus += 1
            
            self.focus = int(pygame.math.clamp(self.focus, 0, len(self.options_processed) - 1))
    
    def update(self):
        super().update()
        
        mini_win_bg_color = mods.set_color(self.game.save.get(SETTINGS_DICT_BG_KEY), 200) if self.game.save.get(SETTINGS_DICT_BG_KEY) not in ('black', [0, 0, 0], [0, 0, 0, 0], (0, 0, 0), (0, 0, 0, 0)) else 'grey20'
        mouse_clicked = pygame.mouse.get_pressed()[0]
        mouse_rect = pygame.Rect(pygame.mouse.get_pos(), (1, 1))
        
        for index, (_, (surfs, surfs_rect, ui_object_info, rect, option_type)) in enumerate(self.options_processed.items()):
            if index == self.focus:
                color = self.game.save.get(SETTINGS_DICT_BG_KEY)
                bg_color = self.game.save.get(SETTINGS_DICT_FG_KEY)
                
                self._draw_buffer.append(["rect", (bg_color, rect), None])
            else:
                color = self.game.save.get(SETTINGS_DICT_FG_KEY)
                bg_color = self.game.save.get(SETTINGS_DICT_BG_KEY)
            
            self._draw_buffer.append(["blit", (surfs[1] if index == self.focus else surfs[0], surfs_rect), None])
            
            if option_type == "input":
                text_input, display_func = ui_object_info
                (surf_fg, surf_bg), rect = display_func()
                if index != self.focus:
                    self._draw_buffer.append(["blit", (surf_fg, rect), None])
                else:
                    self._draw_buffer.append(["blit", (surf_bg, rect), None])
                text_input.partial_activate_text_view(mouse_rect=mouse_rect, fg_color=color)
            elif option_type == "selector":
                selector, display_func = ui_object_info
                (surf_fg, surf_bg), rect = display_func()
                if index != self.focus:
                    self._draw_buffer.append(["blit", (surf_fg, rect), None])
                else:
                    self._draw_buffer.append(["blit", (surf_bg, rect), None])
                selector.activate_selector(mouse_rect, mouse_clicked, color=color)
            elif option_type == "input_selector":
                for object_info in ui_object_info:
                    input_selector, display_func = object_info
                    (surf_fg, surf_bg), rect = display_func()
                    if index != self.focus:
                        self._draw_buffer.append(["blit", (surf_fg, rect), None])
                    else:
                        self._draw_buffer.append(["blit", (surf_bg, rect), None])
                    input_selector.activate_input_selector(mouse_rect, mouse_clicked, pygame.mouse.get_rel(), color, mini_win_bg_color, self.game.save.get(SETTINGS_DICT_FG_KEY))
    
    def get(self, name: str) -> Any:
        return self.get_save_func[name]()

class MultiplayerSettingsScreen(SettingsScreen):
    def __init__(self, game: Game, _id: int, action_id: int | None, link_id_args: list[int], blue: PyBlue):
        options = [
            (MPO_BG_COLOR_KEY, "input", [game.save.get(MPO_BG_COLOR_KEY)]),
            (MPO_FG_COLOR_KEY, "input", [game.save.get(MPO_FG_COLOR_KEY)]),
            (MPO_DATA_KEY, "selector", [MPO_OPTIONS, game.save.get(MPO_DATA_KEY)]),
            (MPO_PC_KEY, "selector", [MPO_CONTROL_OPTIONS, game.save.get(MPO_PC_KEY)]),
            (MPO_PB_KEY, "input_selector", [[("Player one up key binding", "Up: ", game.save.get(MPO_PB_KEY + "0")), ("Player one down key binding", "Down: ", game.save.get(MPO_PB_KEY + "1"))]]),
        ]
        
        super().__init__(game, _id, action_id, link_id_args, _options=options)
        
        font = mods.make_font(3, 100)
        
        self.title_surf = font.render("Multiplayer Settings", False, self.game.save.get(SETTINGS_DICT_FG_KEY))
        self.title_rect = self.title_surf.get_rect(midtop=(self.game.SCR_WIDTH / 2, 30))
        
        self.confirm_button = self.action_button.copy()
        self.confirm_button.rect.right = int(self.game.SCR_WIDTH - self.confirm_button.rect.x)
    
    def _confirm_button_clicked(self):
        self.game.set_screen(2002)
    
    def _update_action_button(self):
        super()._update_action_button()
        self.confirm_button.update(pygame.Rect(pygame.mouse.get_pos(), (1, 1)), pygame.mouse.get_pressed()[0], self._confirm_button_clicked)
    
    def update(self):
        super().update()
        
        self._draw_buffer.append(("blit", (self.title_surf, self.title_rect), None))
        self._draw_buffer.append((self.confirm_button.draw, None, None))

# Non - display technical screens
class ExitScreen(Screen):
    def __init__(self, game: Game, _id: int, action_id: int | None, link_id_args: list[int]):
        super().__init__(game, _id, action_id, link_id_args)
    
    def update(self):
        super().update()
        
        try:
            self.game.save.save()
        except Exception as e:
            print(e)
        finally:
            pygame.quit()
            sys.exit()

class RestartScreen(Screen):
    def __init__(self, game: Game, _id: int, action_id: int | None, link_id_args: list[int]):
        super().__init__(game, _id, action_id, link_id_args)
        self.game_screen_id, = link_id_args
    
    def update(self):
        super().update()
        
        game_scr = self.game.get(self.game_screen_id)
        if isinstance(game_scr, GameScreen):
            game_scr.reset()
            self.game.set_screen(self.game_screen_id)
        else:
            raise Exception(f"ID {self.game_screen_id} is not the main game screen id")


START_SCREEN = 0
END_SCREEN = 14

AUTH_KEY = "h9qruyq9hya98yh9291m2knA+A_ADS)AS_A231SD_Qeiiqcoioqnjaksknos_++@13100/d/aoskajaewáa"

DEFAULT = "defined"
ACTION_LINK = "action link"
OTHER_LINKS = "other links"

BLUETOOTH = PyBlue(AUTH_KEY, 1234, 5)

SCREEN_TREE: dict[int, dict | str] = {
    START_SCREEN: {
        ACTION_LINK: None,
        OTHER_LINKS: {
            1: {
                ACTION_LINK: None,
                OTHER_LINKS: {
                    # Continue Game
                    11: {
                        ACTION_LINK: {
                            # Pause screen
                            111: {
                                # Go back
                                ACTION_LINK: 11,
                                OTHER_LINKS: {
                                    # Resume
                                    11: DEFAULT,
                                    # Settings
                                    1112: {
                                        ACTION_LINK: 111,
                                        OTHER_LINKS: {}
                                        },
                                    # Information
                                    1113: {
                                        ACTION_LINK: 111,
                                        OTHER_LINKS: {}
                                        },
                                    # Main menu
                                    1: DEFAULT,
                                    # Restart
                                    1114: {
                                        ACTION_LINK: None,
                                        OTHER_LINKS: {11: DEFAULT}
                                        },
                                    # Quit
                                    END_SCREEN: DEFAULT
                                    }
                                }
                            },
                        OTHER_LINKS: {
                            # Non display
                            # Get settings
                            1112: DEFAULT
                        }
                        },
                    
                    # New Game
                    12: {
                        ACTION_LINK: None,
                        OTHER_LINKS: {11: DEFAULT}
                        },
                    
                    # Multiplayer
                    13: {
                        ACTION_LINK: 1,
                        OTHER_LINKS: {
                            131: {
                                ACTION_LINK: None,
                                OTHER_LINKS: {
                                    # Bluetooth Lobby Screen
                                    1311: {
                                        ACTION_LINK: 13,
                                        OTHER_LINKS: {
                                            13111: {
                                                ACTION_LINK: None,
                                                OTHER_LINKS: {11: DEFAULT}
                                                }
                                            }
                                        }
                                    }
                                }
                            }
                        },
                    
                    # Exit
                    END_SCREEN: {
                        ACTION_LINK: None,
                        OTHER_LINKS:{}
                        }
                    }
            }
        }
    }
}

SCREEN_KEYS = {
    START_SCREEN: (InfoDisplayScreen, ["Loading",5]),
    1: (WelcomeScreen, []),
    11: (GameScreen, [BLUETOOTH]),
    111: (PauseScreen, []),
    1112: (SettingsScreen, []),
    1113: (InfoScreen, []),
    1114: (RestartScreen, []),
    12: (RestartScreen, []),
    13: (MultiplayerSettingsScreen, [BLUETOOTH]),
    131: (InfoDisplayScreen, ["Loading", 3]),
    1311: (BlueLobbyScreen, [BLUETOOTH]),
    13111: (InfoDisplayScreen, ["Authenticating", 3]),
    END_SCREEN: (ExitScreen, [])
}

