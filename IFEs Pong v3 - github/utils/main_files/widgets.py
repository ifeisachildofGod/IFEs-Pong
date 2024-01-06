from typing import Any
import pygame
from utils.code.constants.game_constants import FN3_SIZE, FOCUS_RECT_WIDTH, CURSOR_ADJUST, SPECIAL_KEYS
from utils.code.constants.ui_constants import BLINK_TIMER, X_OPTION_SPACE_OFFSET, BORDER_RAD
from utils.code.etc import mods
import time

class TextView:
    def __init__(self, tv_input, screen: pygame.Surface, max_tv_len: int, border_radius: int = BORDER_RAD, op_space_offset: int = X_OPTION_SPACE_OFFSET, f_r_width: int = FOCUS_RECT_WIDTH) -> None:
        self.tv_input = tv_input
        self.cursor = len(str(self.tv_input))
        self.screen = screen
        self.words = []
        self.op_space_offset = op_space_offset
        self.border_radius = border_radius
        self.f_r_width = f_r_width
        self.start_click_check = True
        self.start_spec_click_check = True
        self.click_timer = 0
        self.spec_click_timer = 0
        for i in str(self.tv_input):
            self.words.append(i)
        self.max_tv_len = max_tv_len

    def text_view_input(self):
        self.keys = pygame.key.get_pressed()
        
        invalid_keys = (self.keys[pygame.K_ESCAPE], self.keys[pygame.K_RETURN], self.keys[pygame.K_BACKSPACE], self.keys[pygame.K_DELETE], self.keys[pygame.K_HOME], self.keys[pygame.K_END], self.keys[pygame.K_PAGEUP], self.keys[pygame.K_PAGEDOWN], self.keys[pygame.K_LCTRL], self.keys[pygame.K_RCTRL], self.keys[pygame.K_LEFT], self.keys[pygame.K_RIGHT])
                    
        for i in range(len(self.keys)):
            if self.keys[i] not in invalid_keys:
                self.click_timer += 1
                if self.click_timer >= 150 or self.click_timer == 5:
                    if len(self.words) <= self.max_tv_len:
                        self.words.insert(self.cursor, chr(i))
                        self.cursor += 1
                        self.cursor = mods.clamp(self.cursor, len(self.words), 0)
                        self.tv_input = ''.join(self.words)
        
        a = []
        for i in range(len(self.keys)):
            a.append(self.keys[i])
        
        if True not in a or a.count(True) > 1:
            self.click_timer = 0
    
    def tv_special_keys(self):
        invalid_keys = (self.keys[pygame.K_ESCAPE], self.keys[pygame.K_RETURN], self.keys[pygame.K_BACKSPACE], self.keys[pygame.K_DELETE], self.keys[pygame.K_HOME], self.keys[pygame.K_END], self.keys[pygame.K_PAGEUP], self.keys[pygame.K_PAGEDOWN], self.keys[pygame.K_LCTRL], self.keys[pygame.K_RCTRL], self.keys[pygame.K_LEFT], self.keys[pygame.K_RIGHT])
        
        try:
            self.spec_click_timer += 1
            if self.spec_click_timer >= 110 or self.spec_click_timer == 5:
                if self.keys[pygame.K_BACKSPACE]:
                    if self.cursor != 0:
                        self.cursor -= 1
                        self.words[self.cursor] = '@'
                        self.words.remove('@')
                        self.cursor = mods.clamp(self.cursor, len(self.words), 0)
                
                if self.keys[pygame.K_DELETE]:
                    self.words[self.cursor] = '@'
                    self.words.remove('@')
                    self.cursor = mods.clamp(self.cursor, len(self.words), 0)
        
                if self.keys[pygame.K_LEFT]:
                    self.cursor -= 1
                    self.cursor = mods.clamp(self.cursor, len(self.words), 0)
                
                elif self.keys[pygame.K_RIGHT]:
                    self.cursor += 1
                    self.cursor = mods.clamp(self.cursor, len(self.words), 0)
                
                if self.keys[pygame.K_END]:
                    self.cursor = len(self.words)

                if self.keys[pygame.K_HOME]:
                    self.cursor = 0

                if (self.keys[pygame.K_LCTRL] or self.keys[pygame.K_RCTRL]) and self.keys[pygame.K_BACKSPACE]:
                    self.words.clear()

                self.tv_input = ''.join(self.words)
                
            if True not in invalid_keys or invalid_keys.count(True) > 1:
                self.spec_click_timer = 0
        except IndexError:
            pass
    
    def draw_cursor(self, text_surf: pygame.Surface, text_rect: pygame.Rect, fg_color, bg_color):
        cursor_x = text_rect.left + (FN3_SIZE) * len(str(self.tv_input)[:self.cursor])
        timer = int(str(round(time.time(), 1))[-1])
        
        if timer > BLINK_TIMER//2: col = fg_color
        else: col = bg_color
        
        for i in str(self.tv_input)[:self.cursor]:
            if CURSOR_ADJUST.get(i):
                cursor_x += CURSOR_ADJUST.get(i)
        
        outline = pygame.Rect(text_rect.x - self.op_space_offset//2,
                              text_rect.y,
                              text_surf.get_width() + self.op_space_offset,
                              text_surf.get_height()
                       )
        
        pygame.draw.line(
                        self.screen,
                        col,
                        (cursor_x, outline.bottom - self.f_r_width),
                        (cursor_x, outline.top + self.f_r_width)
                        )
    
    def draw_outline(self, text_surf: pygame.Surface, text_rect: pygame.Rect, fg_color):
        outline = pygame.Rect(text_rect.x - self.op_space_offset//2,
                              text_rect.y,
                              text_surf.get_width() + self.op_space_offset,
                              text_surf.get_height()
                       )
        
        pygame.draw.rect(self.screen, fg_color, outline, self.f_r_width, self.border_radius, self.border_radius, self.border_radius, self.border_radius, self.border_radius)
    
    def activate_text_view(self, text_surf: pygame.Surface, text_rect: pygame.Rect, fg_color, bg_color):
        self.draw_outline(text_surf, text_rect, fg_color)
        self.draw_cursor(text_surf, text_rect, fg_color, bg_color)
        self.text_view_input()
        self.tv_special_keys()
        
        return self.tv_input

class Button:
    def __init__(self, screen: pygame.Surface, background_color, border_radius: int, positon: tuple, size: int | tuple, txt=None, txt_color=None, sound_path: tuple = None) -> None:
        self.button_opacity = 255
        self.border_radius = border_radius
        self.screen = screen
        self.click_timer = 0
        self.start_click_check = True
        self.txt = txt
        self.disabled = False
        self.do_someting = False
        self.cicked_outside = True
        self.bg_offset = 2
        self.on_hover_opacity = 200
        self.on_click_opacity = 150
        self.background_color = background_color
        self.txt_color = txt_color
        self.size = size
        self.mouse_was_clicked = pygame.mouse.get_pressed()[0]
        self.sound_path = sound_path
        
        if self.sound_path is not None:
            self.clicked_sound = pygame.mixer.Sound(self.sound_path[0])
            self.clicked_sound.set_volume(self.sound_path[1])
            
        if (txt is not None and txt_color is None) or (txt is None and txt_color is not None) or (txt is None and txt_color is None):
            self.txt_color = background_color
        
        if self.txt is not None:
            self.txt_surf = pygame.transform.scale(pygame.font.Font(size=int(self.size) if isinstance(self.size, int) or isinstance(self.size, float) else self.size[1]).render(self.txt, False, self.txt_color), (self.size, self.size) if isinstance(self.size, int) or isinstance(self.size, float) else self.size)
            self.rect_div = self.txt_surf.get_rect(topleft=(positon[0], positon[1]))
        else:
            if isinstance(size, int) or isinstance(size, float):
                the_size = (size, size)
            else:
                the_size = size
                
            self.rect_div = pygame.Rect(positon[0], positon[1], *the_size)
        
        self.button_rect = pygame.Rect(self.rect_div.x - (self.bg_offset/2), self.rect_div.y - (self.bg_offset/2), self.rect_div.width + self.bg_offset, self.rect_div.height + self.bg_offset)
        self.button = self.button_rect
        
        self.button_rect = pygame.Rect(self.rect_div.x - (self.bg_offset/2), self.rect_div.y - (self.bg_offset/2), self.rect_div.width + self.bg_offset, self.rect_div.height + self.bg_offset)
    
    def on_hover(self, action_performed):
        self.button_opacity = self.on_hover_opacity
        if action_performed is not None:
            action_performed()
        
    def isclicked(self, mouse_rect: pygame.Rect, target: pygame.Rect, clicked: bool, func):
        if self.mouse_was_clicked and (not self.mouse_rect.colliderect(self.button_rect)):
            self.cicked_outside = True
        elif not self.mouse_was_clicked:
            self.cicked_outside = False
        
        if mouse_rect.colliderect(target) and not self.cicked_outside:
            func()
            return clicked
        return False
    
    def get_rect(self):
        return self.button_rect
    
    def on_activate(self, action_performed, action_on_hover, no_bounce: bool, sound_path: tuple):
        if self.txt is not None:
            self.txt_surf = pygame.transform.scale(pygame.font.Font(size=int(self.size) if isinstance(self.size, int) or isinstance(self.size, float) else self.size[1]).render(self.txt, False, self.txt_color), (self.size, self.size) if isinstance(self.size, int) or isinstance(self.size, float) else self.size)
        
        if sound_path is not None:
            self.clicked_sound = pygame.mixer.Sound(self.sound_path[0])
            self.clicked_sound.set_volume(self.sound_path[1])
        
        mouse = pygame.mouse.get_pos()
        m_x, m_y = mouse
        self.mouse_rect = pygame.Rect(m_x, m_y, 1, 1)
        self.mouse_was_clicked = pygame.mouse.get_pressed()[0]
        
        was_clicked = self.isclicked(self.mouse_rect, self.button_rect, self.mouse_was_clicked, lambda: self.on_hover(action_on_hover))
        
        self.start_click_check = True if no_bounce else self.start_click_check
        
        if self.mouse_rect.colliderect(self.button_rect):
            if was_clicked:
                if self.start_click_check:
                    if self.sound_path is not None or sound_path is not None:
                        self.clicked_sound.play()
                    if action_performed is not None:
                        action_performed()
                    self.start_click_check = False
                self.button_opacity = self.on_click_opacity
        else:
            self.button_opacity = 255
        
        if not self.start_click_check:
            self.click_timer += 1
            if self.click_timer >= 20:
                self.start_click_check = True
                self.click_timer = 0
    
    def draw(self, pos=None, color: tuple | Any = None, disabled = None):
        background_color = self.background_color
        
        if pos is not None:
            self.button_rect.x = pos[0]
            self.button_rect.y = pos[1]
        if color is not None:
            if isinstance(color, tuple) or isinstance(color, list):
                if len(color) == 2:
                    background_color, self.txt_color = color
                else:
                    background_color = color
            else:
                background_color = color
        
        background_color = mods.set_color(background_color, self.button_opacity) if not disabled else background_color
        self.button = pygame.draw.rect(self.screen, background_color, self.button_rect, 0, self.border_radius, self.border_radius, self.border_radius, self.border_radius)
        
        if self.txt is not None:
            if pos is not None:
                self.rect_div.x = pos[0]
                self.rect_div.y = pos[1]
        
            self.screen.blit(self.txt_surf, self.rect_div)

    def activate_button(self, on_click=None, on_hover=None, pos=None, color: tuple | Any = None, no_bounce=False, sound_path: tuple = None):
        if not self.disabled:
            self.on_activate(on_click, on_hover, no_bounce, sound_path)
        self.draw(pos, color, disabled=self.disabled)

class Selector:
    def __init__(self, screen, options: list, index: int, border_radius: int = BORDER_RAD, f_r_width: int = FOCUS_RECT_WIDTH, width: int = None):
        self.screen = screen
        self.options = options
        self.index = index
        self.value = self.options[self.index]
        self.start_click_check = True
        self.click_timer = 0
        self.ptr_size = 10
        self.f_r_width = f_r_width
        self.border_radius = border_radius
        self.assigned = True
        self.width = width
        
    def _inc_dec(self, inc: bool):
        if inc:
            self.index += 1
        else:
            self.index -= 1
        self.index = mods.clamp(self.index, len(self.options) - 1, 0)
        self.value = self.options[self.index]
        
    def text_and_selector(self, text_surf: pygame.Surface, text_rect: pygame.Rect, color):
        self.keys = pygame.key.get_pressed()
        
        self.outline = pygame.Rect(text_rect.x - X_OPTION_SPACE_OFFSET//2,
                                   text_rect.y,
                                   (text_surf.get_width() + X_OPTION_SPACE_OFFSET) if self.width is None else self.width,
                                   text_surf.get_height()
                                    )
        
        self.ptr_y = self.outline.top + ((self.outline.height - self.ptr_size) / 2)
        
        if self.assigned:
            self.ptr_left = Button(self.screen, color, BORDER_RAD, ((self.outline.left - self.ptr_size) - 10, self.ptr_y), self.ptr_size)
            self.ptr_right = Button(self.screen, color, BORDER_RAD, (self.outline.right + 10, self.ptr_y), self.ptr_size)
            self.assigned = False
        
        if self.index != len(self.options) - 1:
            self.ptr_right.activate_button(lambda: self._inc_dec(True), pos=((self.outline.left - self.ptr_size) - 10, self.ptr_y), color=color)
        if self.index != 0:
            self.ptr_left.activate_button(lambda: self._inc_dec(False), pos=(self.outline.right + 10, self.ptr_y), color=color)

        if self.start_click_check and (self.keys[pygame.K_LEFT] or self.keys[pygame.K_RIGHT]):
            if self.keys[pygame.K_LEFT]:
                self._inc_dec(True)
            elif self.keys[pygame.K_RIGHT]:
                self._inc_dec(False)
            
            self.start_click_check = False
        
        if not self.start_click_check:
            self.click_timer += 1
            if self.click_timer >= 20:
                self.start_click_check = True
                self.click_timer = 0
    
    def get_value(self):
        return self.value
    
    def display_outline(self, color):
        pygame.draw.rect(self.screen, color, self.outline, self.f_r_width, self.border_radius, self.border_radius, self.border_radius, self.border_radius, self.border_radius)
    
    def activate_selector(self, text_surf: pygame.Surface, text_rect: pygame.Rect, color):
        self.text_and_selector(text_surf, text_rect, color)
        self.display_outline(color)

        return self.value, self.index

class InputSeletor:
    def __init__(self, character: str, screen: pygame.Surface, bg_color, fg_color, mini_win_title: str, mini_win_logo_path, border_radius: int = BORDER_RAD, mini_outline_width: int = 700, mini_outline_height: int = 120, main_outline_width: int = X_OPTION_SPACE_OFFSET, f_r_width: int = FOCUS_RECT_WIDTH) -> None:
        self.character = self.display_char = character
        self.display_ord = SPECIAL_KEYS.get(self.character) if SPECIAL_KEYS.get(self.character) is not None else ord(self.character)
        self.outline_opacity = 255
        self.screen = screen
        self.mini_outline_width = mini_outline_width
        self.mini_outline_height = mini_outline_height
        self.main_outline_width = main_outline_width
        self.border_radius = border_radius
        self.f_r_width = f_r_width
        self.bg_color = bg_color
        self.fg_color = fg_color

        self.mini_win_size = 300
        self.txt_size = self.mini_win_size // 2

        self.keys = pygame.key.get_pressed()
        self.click_timer = 0

        self.mini_win_active = False
        self.mini_win = MiniWindow(self.screen, self.mini_win_size, [(self.screen.get_width() / 2) - (self.mini_win_size / 2), (self.screen.get_height() / 2) - (self.mini_win_size / 2)], mini_win_title, self.fg_color, self.bg_color, mods.set_color(self.bg_color, 120), window_activated=self.mini_win_active, logo=mini_win_logo_path)

        self.start_click_check = True
        self.start_click_check = True
        self.cicked_outside = True
        self.start_the_check = False
        self.check_it_now = False
    
    def _set_outline_color(self, opac: int):
        self.outline_opacity = opac
    
    def char_input(self):
        for i in range(len(self.keys)):
            invalids_not_clciked = not self.keys[pygame.K_ESCAPE] and not self.keys[pygame.K_RETURN] and not self.keys[pygame.K_BACKSPACE]
            if self.keys[i] and i not in [k for _, k in SPECIAL_KEYS.items()] and invalids_not_clciked:
                self.character = chr(i)
                self.display_ord = i
        
    def get_special_keys(self):
        for k, v in list(zip([k for k, _ in SPECIAL_KEYS.items()], [v for _, v in SPECIAL_KEYS.items()])):
            if self.keys[v]:
                self.character = k
                self.display_ord = v
    
    def isclicked(self, mouse_rect: pygame.Rect, target: pygame.Rect, clicked: bool, func = None):
        if clicked and (not mouse_rect.colliderect(target)):
            self.cicked_outside = True
        elif not clicked:
            self.cicked_outside = False
        
        if mouse_rect.colliderect(target) and not self.cicked_outside:
            if func is not None:
                func()
            return clicked
        return False
    
    def open_mini_window(self, mouse_rect: pygame.Rect, target: pygame.Rect, clicked: bool):
        self.outline_opacity = 255
        if self.isclicked(mouse_rect, target, clicked):
            self.mini_win_active = True
            self.mini_win.set_active(True)    
        
        if self.start_click_check and self.keys[pygame.K_RETURN]:
            self.mini_win_active = not self.mini_win_active
            self.mini_win.set_active(self.mini_win_active)

            self.start_click_check = False
        self.mini_win_active = self.mini_win.isactive()
    
        if not self.start_click_check:
            self.click_timer += 1
            if self.click_timer >= 15:
                self.start_click_check = True
                self.click_timer = 0
    
    def mini_prompt_window(self, mouse_rect: pygame.Rect, clicked: bool, rel, fg_color=None, bg_color=None):
        self.prompt_bottom_offset = 150
        if fg_color is not None:
            self.fg_color = fg_color
        if bg_color is not None:
            self.bg_color = bg_color
        
        char_outline = pygame.Rect((self.screen.get_width() / 2) - (self.mini_outline_width / 2),
                                   (self.screen.get_height() / 2) - (self.mini_outline_height / 2) - (self.prompt_bottom_offset / 2),
                                   self.mini_outline_width,
                                   self.mini_outline_height)
        
        self.character_surf = pygame.font.Font(size=self.txt_size).render(str(self.character), False, self.fg_color)
        self.character_rect = pygame.Rect(char_outline.centerx - (self.character_surf.get_width() / 2),
                                          char_outline.centery - (self.character_surf.get_height() / 2),
                                          self.character_surf.get_width(),
                                          self.character_surf.get_height())
        
        self.prompt = pygame.font.Font(size=self.txt_size // 2).render('Click any key', False, self.fg_color)
        prompt_rect = pygame.Rect((self.screen.get_width() / 2) - (self.prompt.get_width()) / 2,
                                  self.screen.get_height() - self.prompt_bottom_offset,
                                  self.prompt.get_width(),
                                  self.prompt.get_height())

        mini_widgets = (('rect', self.fg_color, char_outline, (self.f_r_width, self.border_radius, self.border_radius, self.border_radius, self.border_radius, self.border_radius), 'self'),
                        ('surf', self.character_surf, self.character_rect, None, 'self'),
                        ('surf', self.prompt, prompt_rect, None, 'self'))
        
        colors = {'background': bg_color,
                  'title': fg_color,
                  'title bar': (mods.set_color(self.bg_color, 120))}
        
        self.mini_win.update(mouse_rect, clicked, mini_widgets, colors=colors, rel=rel)
        
        if not self.mini_win.isactive():
            self.display_char = self.character
        else:
            self.char_input()
            self.get_special_keys()
    
    def display_outline(self, text_surf: pygame.Surface, text_rect: pygame.Rect, fg_color):
        self.keys = pygame.key.get_pressed()
        self.main_outline = pygame.Rect(text_rect.x - (self.main_outline_width/4),
                              text_rect.y,
                              text_surf.get_width() + (self.main_outline_width/2),
                              text_surf.get_height()
                       )
        
        pygame.draw.rect(self.screen, fg_color, self.main_outline, self.f_r_width, self.border_radius, self.border_radius, self.border_radius, self.border_radius, self.border_radius)
    
    def activate_input_selector(self, text_surf: pygame.Surface, text_rect: pygame.Rect, mouse_rect: pygame.Rect, clicked: bool, outline_color, rel, min_win_bg_color=None, mini_win_fg_color=None):
        self.display_outline(text_surf, text_rect, outline_color)
        self.mini_prompt_window(mouse_rect, clicked, rel, mini_win_fg_color, min_win_bg_color)
        self.open_mini_window(mouse_rect, self.main_outline, clicked)
        
        return str(self.display_char), self.display_ord

class MiniWindow:
    def __init__(self, main_window: pygame.Surface, win_size: int, window_pos: list, title, title_color, bg_color, title_bar_color, grabable=True, window_activated=True, logo=None) -> None:
        self.window_pos = window_pos
        self.win_size = win_size
        self.main_window = main_window
        self.grabable = grabable
        self.window = pygame.Surface((self.win_size, self.win_size))
        self.title_bar_color = title_bar_color
        self.bg_color = bg_color
        self.window_activated = window_activated
        self.btn_size = (self.win_size//10) / 1.5
        self.title_bar_rect = pygame.Rect(self.window_pos[0], self.window_pos[1] - self.win_size//10, self.window.get_width(), self.win_size//10)
        self.title_name = title
        self.title_color = title_color
        self.print_warning = True
        
        self.logo_surf = pygame.Surface((self.btn_size, self.btn_size)) if logo is None else pygame.transform.scale(pygame.image.load(logo), (self.btn_size, self.btn_size))
        if logo is None:
            self.logo_surf.fill(title_color)
        
        self.btn_size = self.title_bar_rect.height / 1.5
        self.offset = self.btn_size / 4
        
        self.start_moving = False
        self.exit_button = Button(self.main_window, 'red', 0, (self.title_bar_rect.right - self.btn_size - self.offset, self.title_bar_rect.top + self.offset), self.btn_size, 'x', 'black')

    def set_window_state(self, close_window):
        self.window_activated = not close_window
    
    def isclicked(self, mouse_rect: pygame.Rect, target: pygame.Rect, clicked: bool, func = None):
        if clicked and (not mouse_rect.colliderect(target)):
            self.cicked_outside = True
        elif not clicked:
            self.cicked_outside = False
        
        if mouse_rect.colliderect(target) and not self.cicked_outside:
            if func is not None:
                func()
            return clicked
        return False
    
    def check_win_moved(self, mouse_rect, clicked):
        if self.window_activated:
            self.start_moving = self.isclicked(mouse_rect, self.title_bar_rect, clicked)
    
    def get_pos(self):
        return tuple(self.window_pos)
    
    def get_size(self):
        return (self.win_size, self.win_size)
    
    def isactive(self):
        return self.window_activated
    
    def set_logo_path(self, logo_path):
        self.logo_surf = pygame.transform.scale(pygame.image.load(logo_path), (self.btn_size, self.btn_size))
    
    def set_active(self, isactive: bool):
        self.window_activated = isactive
    
    def draw_window(self, mouse_rect: pygame.Rect, colors: dict = None, rel = None):
        if self.window_activated:
            self.btn_move = [0, 0]
            if colors is not None:
                self.bg_color = colors.get('background') if colors.get('background') is not None else self.bg_color
                self.title_bar_color = colors.get('title bar') if colors.get('title bar') is not None else self.title_bar_color
                self.title_color = colors.get('title') if colors.get('title') is not None else self.title_color
            
            warning1 = 'Warning: rel is None or was not passed and grabable is true you might have made an error in passing the arguments'
            warning2 = 'Warning: rel was passed and grabable is false you might have made an error in passing the arguments'
            
            if self.start_moving and self.grabable:
                if rel is not None and mouse_rect.colliderect(pygame.Rect(0, 0, self.main_window.get_width(), self.main_window.get_height())):
                    self.window_pos[0] += rel[0]
                    self.window_pos[1] += rel[1]
                    self.btn_move = rel
                else:
                    if self.print_warning:
                        print(warning1)
                        self.print_warning = False
            
            if not self.grabable and rel is not None and self.print_warning:
                print(warning2)
                self.print_warning = False
            
            self.main_window.blit(self.window, self.window_pos)

            self.window.fill(self.bg_color)
            
            self.title_bar_rect = pygame.Rect(self.window_pos[0], self.window_pos[1] - self.win_size//10, self.window.get_width(), self.win_size//10)
            pygame.draw.rect(self.main_window, self.title_bar_color, self.title_bar_rect)
            
            self.btn_size = self.title_bar_rect.height / 1.5
            self.title = pygame.font.Font(size=int(self.btn_size)).render(self.title_name, False, self.title_color)
            self.offset = self.btn_size / 4
            
            self.title_offset = 10
            self.main_window.blit(self.title, (self.title_bar_rect.left + self.title_offset + (self.btn_size + (self.btn_size/8)), (self.title_bar_rect.bottom - self.title.get_height() - (self.title.get_height()/2) )))
            self.main_window.blit(self.logo_surf, (self.title_bar_rect.left + (self.title_offset/2), self.exit_button.button_rect.y + self.btn_move[1]))
            
            self.exit_button.activate_button(lambda: self.set_window_state(True), pos=(self.exit_button.button_rect.x + self.btn_move[0], self.exit_button.button_rect.y + self.btn_move[1]))

    def draw_widgets(self, widgets: tuple[tuple[str, pygame.Surface | pygame.Color, pygame.Rect, Any, str]] = None):
        if self.window_activated:
            if widgets is not None:
                for widget_info in widgets:
                    id_, to_be_drawn, widget_rect, others, dest = widget_info
                    
                    x = (widget_rect.x/self.main_window.get_width()) * self.win_size
                    y = (widget_rect.y/self.main_window.get_height()) * self.win_size
                    width = ((widget_rect.width/self.main_window.get_width()) * self.win_size)  if id_ == 'rect' else (to_be_drawn.get_width()/self.main_window.get_width()) * self.win_size
                    height = ((widget_rect.height/self.main_window.get_height()) * self.win_size) if id_ == 'rect' else (to_be_drawn.get_height()/self.main_window.get_height()) * self.win_size
                    
                    if dest == 'self':
                        widget_rect = pygame.Rect(x, y, width, height)
                    elif dest == 'body':
                        pass
                    else:
                        raise Exception('Invalid destination arg')
                    
                    if id_ == 'surf':
                        to_be_drawn = pygame.transform.scale(to_be_drawn, (width, height))
                        self.window.blit(to_be_drawn, widget_rect, *(others if others is not None else ()))
                    elif 'rect' in id_:
                        draw_args = self.window, to_be_drawn, widget_rect, *(others if others is not None else ())
                        
                        if id_ == 'rect':
                            pygame.draw.rect(*draw_args)
                        elif '(circle)' in id_:
                            pygame.draw.ellipse(*draw_args)
                            
                    else:
                        raise Exception('Invalid class arg')
    
    def update(self, mouse_rect, clicked, widgets: tuple[tuple[str, pygame.Surface | pygame.Color, pygame.Rect, Any, str]] = None, colors: dict = None, rel=None):
        '''
        :param rel:                   pygame.mouse.get_rel()
        :type rel:                    (tuple)
        :param mouse_rect:            pygame.Rect(*pygame.mouse.get_pos, 1, 1)
        :type mouse_rect:             (pygame.Rect)
        :param clciked:               pygame.mouse.get_pressed()[0]
        :type clciked:                (bool)
        :param widgets:               order goes like this ('surf' or 'rect', screen or color, rect, other arguments, 'self' or 'body')
        :type widgets:                (tuple[tuple[str, pygame.Surface | pygame.Color, pygame.Rect, Any, str]])
        :param colors:                {'background': val1, 'title bar': val2, 'title': val3}
        :type colors:                 (dict)
        '''
        self.draw_window(mouse_rect, colors, rel)
        self.draw_widgets(widgets)
        self.check_win_moved(mouse_rect, clicked)

