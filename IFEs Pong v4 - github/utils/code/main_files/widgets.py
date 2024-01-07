import math
from typing import Any
import pygame
import time
from utils.code.constants.game_constants import FN3_SIZE, FOCUS_RECT_WIDTH, CURSOR_ADJUST, SPECIAL_KEYS
from utils.code.constants.ui_constants import X_OPTION_SPACE_OFFSET, BORDER_RAD, TV_INPUT_DELAY_TIMER, TV_INPUT_MAX_WAIT_DELAY_TIMER, BORDER_RAD_BUTTON, BLINK_TIMER
from utils.code.etc import mods
import json
from threading import Thread


class Input:
    def __init__(self, screen: pygame.Surface, init_input: str, max_tv_len: int, pos: tuple, font: pygame.font.Font, fg_color, border_radius: int = BORDER_RAD, op_space_offset: int = X_OPTION_SPACE_OFFSET, f_r_width: int = FOCUS_RECT_WIDTH, width: int = None) -> None:
        self.tv_input = init_input
        self.cursor = len(self.tv_input)
        self.screen = screen
        self.width = width
        self.words_list = []
        self.op_space_offset = op_space_offset
        self.border_radius = border_radius
        self.f_r_width = f_r_width
        self.start_click_check = True
        self.start_spec_click_check = True
        self.enabled = True
        self.click_timer = 0
        self.spec_click_timer = 0
        self.pos = pos
        self.fg_color = fg_color
        self.font = font
        self.keys = pygame.key.get_pressed()
        self.outline = pygame.Rect(0, 0, 0, 0)
        self.mouse_was_clicked = False
        self.clicked_outside = False
        self.within_click_area = False
        self.max_tv_len = max_tv_len
        self.bool_op = False
        *self.words_list, = str(self.tv_input)
        self.text_surf = self.font.render(self.tv_input, False, self.fg_color)
        self.text_rect = self.text_surf.get_rect(topleft=self.pos)
    
    def _get_correct_click_instance(self, mouse_rect: pygame.Rect, target: pygame.Rect, clicked: bool, not_clicked: bool):
        self.clicked_outside = False
        self.within_click_area = mouse_rect.colliderect(target)
        
        if not self.within_click_area:
            if not self.mouse_was_clicked and clicked:
                self.outside_of_bounds = True
            elif not clicked:
                self.outside_of_bounds = False
        
        if self.clicked_outside and self.within_click_area:
            self.clicked_outside = False
        
        if not clicked and not self.within_click_area:
            self.mouse_was_clicked = False
        
        if clicked and self.within_click_area:
            self.mouse_was_clicked = True
        
        self.mouse_was_clicked = (not self.within_click_area and clicked) if not_clicked else self.mouse_was_clicked
        self.outside_of_bounds = (not self.outside_of_bounds) if not_clicked else self.outside_of_bounds
        
        return self.mouse_was_clicked and not self.outside_of_bounds
    
    def _set_invalids(self):
        self.invalid_keys = [
            self.keys[pygame.K_ESCAPE],
            self.keys[pygame.K_RETURN],
            self.keys[pygame.K_BACKSPACE],
            self.keys[pygame.K_DELETE],
            self.keys[pygame.K_HOME], self.keys[pygame.K_END],
            self.keys[pygame.K_PAGEUP], self.keys[pygame.K_PAGEDOWN],
            self.keys[pygame.K_LCTRL], self.keys[pygame.K_RCTRL],
            self.keys[pygame.K_LEFT], self.keys[pygame.K_RIGHT],
            self.keys[pygame.K_TAB]
            ]
        self.invalid_chrs = [
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            "",
                            ]

    def _set_state(self, state):
        self.enabled = state
    
    def _init_draw(self, fg_color, text_surf: pygame.Surface, text_rect: pygame.Rect, func):
        self.text_surf = self.font.render(self.tv_input, False, self.fg_color)
        self.text_rect = self.text_surf.get_rect(topleft=self.pos)
        
        if func is not None:
            func()
        
        if text_surf is not None:
            self.text_surf = text_surf
        if text_rect is not None:
            self.text_rect = text_rect
        
        if fg_color is not None:
            self.fg_color = fg_color
    
    def _constant_update(self, mouse_rect: pygame.Rect, target: pygame.Rect, draw_words: bool, clicked: bool, text_surf: pygame.Surface = None, text_rect: pygame.Rect = None, fg_color = None, width: int = None, partial: bool = False, func = None):
        if not partial:
            self._init_draw(fg_color, text_surf, text_rect, func)
            self.draw_outline(self.text_surf, self.text_rect, self.fg_color, width)
            if draw_words:
                self.draw_words(self.text_surf, self.text_rect)
            self.set_state(mouse_rect, target, clicked)
        else:
            self.text_view_input()
            self.draw(fg_color, draw_words, text_surf, text_rect, width, func)
            self.tv_special_keys()
    
    def isclicked(self, mouse_rect: pygame.Rect, target: pygame.Rect, clicked: bool, on_click_func = None, on_hover_func = None, not_clicked = False):
        is_clicked_correctly = self._get_correct_click_instance(mouse_rect, target, clicked, not_clicked)
        
        if is_clicked_correctly:
            if on_hover_func is not None:
                on_hover_func()
            if on_click_func is not None:
                if clicked:
                    on_click_func()
            return clicked
        return False
    
    def tv_special_keys(self):
        self._set_invalids()
        try:
            self.spec_click_timer += 1
            if self.spec_click_timer >= TV_INPUT_MAX_WAIT_DELAY_TIMER or self.spec_click_timer == TV_INPUT_DELAY_TIMER:
                if self.keys[pygame.K_BACKSPACE]:
                    if self.cursor != 0:
                        self.cursor -= 1
                        self.words_list[self.cursor] = '@'
                        self.words_list.remove('@')
                        self.cursor = pygame.math.clamp(self.cursor, 0, len(self.words_list))
                
                if self.keys[pygame.K_DELETE]:
                    self.words_list[self.cursor] = '@'
                    self.words_list.remove('@')
                    self.cursor = pygame.math.clamp(self.cursor, 0, len(self.words_list))

                if self.keys[pygame.K_LEFT]:
                    self.cursor -= 1
                    self.cursor = pygame.math.clamp(self.cursor, 0, len(self.words_list))
                
                elif self.keys[pygame.K_RIGHT]:
                    self.cursor += 1
                    self.cursor = pygame.math.clamp(self.cursor, 0, len(self.words_list))
                
                if self.keys[pygame.K_END]:
                    self.cursor = len(self.words_list)

                if self.keys[pygame.K_HOME]:
                    self.cursor = 0

                self.tv_input = ''.join(self.words_list)
                
            if True not in self.invalid_keys or self.invalid_keys.count(True) > 1:
                self.spec_click_timer = 0
        except IndexError:
            pass
    
    def text_view_input(self):
        self._set_invalids()
        self.keys = pygame.key.get_pressed()
        
        self.caps_on = (pygame.key.get_mods() & pygame.KMOD_CAPS) == 81
        
        uppercase = (self.keys[pygame.K_RSHIFT] or self.keys[pygame.K_LSHIFT]) or self.caps_on
        if (self.keys[pygame.K_RSHIFT] or self.keys[pygame.K_LSHIFT]) and self.caps_on:
            uppercase = False
        
        if len(self.words_list) <= self.max_tv_len:
            for i in range(len(self.keys)):
                if uppercase:
                    if chr(i).isalpha():
                        self.chr_addition = ord('A') - ord('a')
                    else:
                        self.chr_addition = 0
                else:
                    self.chr_addition = 0
                
                if self.keys[pygame.K_RCTRL] or self.keys[pygame.K_LCTRL]:
                    if self.keys[pygame.K_BACKSPACE]:
                        self.words_list[:self.cursor]  = '@'
                        self.words_list.remove('@')
                        self.cursor = 0
                        self.tv_input = ''.join(self.words_list)
                    
                    if self.keys[pygame.K_DELETE]:
                        self.words_list[self.cursor:]  = '@'
                        self.words_list.remove('@')
                        self.cursor = len(self.words_list)
                        self.tv_input = ''.join(self.words_list)
                    
                    # if self.keys[pygame.K_LEFT]:
                    #     if self.words_list[self.cursor - 1] != ' ':
                    #         target_words = self.words_list[:self.cursor]
                    #         target_words.reverse()
                    #         left_space = ''.join(target_words).find(' ') + 1
                    #         self.cursor -= left_space
                    #         if left_space < 0:
                    #             self.cursor = 0
                    #     else:
                    #         self.cursor -= 1
                    # try:
                    #     if self.keys[pygame.K_RIGHT]:
                    #         if self.words_list[self.cursor] != ' ':
                    #             right_space = ''.join(self.words_list[self.cursor:]).find(' ')
                    #             self.cursor += right_space
                    #             if right_space < 0:
                    #                 self.cursor = len(self.words_list)
                    #         else:
                    #             self.cursor += 1
                    # except IndexError:
                    #     pass
                
                if self.keys[i] not in self.invalid_keys:
                    if chr(i) not in self.invalid_chrs:
                        self.click_timer += 1
                        if self.click_timer >= TV_INPUT_MAX_WAIT_DELAY_TIMER or self.click_timer == TV_INPUT_DELAY_TIMER:
                            self.words_list.insert(self.cursor, chr(i + self.chr_addition))
                            self.cursor += 1
                            self.cursor = pygame.math.clamp(self.cursor, 0, len(self.words_list))
                            self.tv_input = ''.join(self.words_list)
        
        key_states = []
        for i in range(len(self.keys)):
            key_states.append(self.keys[i])
        
        if True not in key_states or key_states.count(True) > 1:
            self.click_timer = 0
    
    def set_state(self, mouse_rect: pygame.Rect, target: pygame.Rect, clicked: bool):
        if not self.within_click_area:
            self.isclicked(mouse_rect, target, clicked, on_click_func=lambda: self._set_state(False), not_clicked=True)
        else:
            self.isclicked(mouse_rect, target, clicked, on_click_func=lambda: self._set_state(True))
            
    def draw_cursor(self, text_surf: pygame.Surface, text_rect: pygame.Rect, fg_color):
        cursor_x = text_rect.left + (FN3_SIZE) * len(str(self.tv_input)[:self.cursor])
        timer = time.time() % BLINK_TIMER
        
        CONSTANT_SURF_WIDTH = pygame.font.Font('utils/fonts/font(2).ttf', 25).render(str(self.tv_input)[:self.cursor], False, self.fg_color).get_width()
        surf_width = self.font.render(str(self.tv_input)[:self.cursor], False, self.fg_color).get_width()
        
        for i in str(self.tv_input)[:self.cursor]:
            if CURSOR_ADJUST.get(i):
                cursor_x += CURSOR_ADJUST.get(i)
        
        outline = pygame.Rect(text_rect.x - self.op_space_offset//2,
                            text_rect.y,
                            text_surf.get_width() + self.op_space_offset,
                            text_surf.get_height()
                    )
        
        key_states = []
        for i in range(len(self.keys)):
            key_states.append(self.keys[i])
        
        self.key_presseed = True in key_states
        
        if timer >= BLINK_TIMER/2 or self.key_presseed:
            if self.key_presseed:
                timer = 0
            
            pygame.draw.line(
                                self.screen,
                                fg_color,
                                (cursor_x + (surf_width - CONSTANT_SURF_WIDTH), outline.bottom - self.f_r_width),
                                (cursor_x + (surf_width - CONSTANT_SURF_WIDTH), outline.top + self.f_r_width)
                                )
    
    def draw_outline(self, text_surf: pygame.Surface, text_rect: pygame.Rect, fg_color, width: int | float):
        if width is not None:
            self.width = width
        
        self.outline = pygame.Rect(text_rect.x - self.op_space_offset//2,
                                   text_rect.y,
                                   (text_surf.get_width() if self.width is None else self.width) + self.op_space_offset,
                                   text_surf.get_height()
                       )
        
        pygame.draw.rect(self.screen, fg_color, self.outline, self.f_r_width, self.border_radius, self.border_radius, self.border_radius, self.border_radius, self.border_radius)
    
    def draw_words(self, text_surf: pygame.Surface, text_rect: pygame.Rect):
        self.screen.blit(text_surf, text_rect)
    
    def draw(self, fg_color, draw_words, text_surf: pygame.Surface, text_rect: pygame.Rect, width: int, func):
        self._init_draw(fg_color, text_surf, text_rect, func)
        self.draw_outline(self.text_surf, self.text_rect, self.fg_color, width)
        self.draw_cursor(self.text_surf, self.text_rect, self.fg_color)
        if draw_words:
            self.draw_words(self.text_surf, self.text_rect)
    
    def activate_text_view(self, mouse_rect: pygame.Rect, clicked: bool, draw_words = True, text_surf: pygame.Surface = None, text_rect: pygame.Rect = None, fg_color = None, bg_color = None, width: int = None):
        self._constant_update(mouse_rect, self.outline, draw_words, clicked, text_surf, text_rect, fg_color, bg_color, width)
        if self.enabled:
            self.tv_special_keys()
            self.text_view_input()
            self.draw_cursor(self.text_surf, self.text_rect, self.fg_color)
        return self.tv_input
    
    def partial_activate_text_view(self, mouse_rect, draw_words = True, text_surf: pygame.Surface = None, text_rect: pygame.Rect = None, fg_color = None, width: int = None):
        self._constant_update(mouse_rect, self.outline, draw_words, False, text_surf, text_rect, fg_color, width, True)
        return self.tv_input

class Button:
    def __init__(self, screen: pygame.Surface, background_color, position: tuple, size: int | tuple, border_radius: int = BORDER_RAD_BUTTON, txt=None, txt_color=None, sound_info: tuple = None) -> None:
        self.button_opacity = 255
        self.border_radius = border_radius
        self.screen = screen
        self.position = (tuple(position)) if isinstance(position, tuple) or isinstance(position, list) else (position, position)
        self.clicked = False
        self.start_playing_hover_sound = True
        self.click_timer = 0
        self.start_click_check = True
        self.txt = txt
        self.disabled = False
        self.do_someting = False
        self.clicked_outside = True
        self.bg_offset = 2
        self.on_hover_opacity = 200
        self.on_click_opacity = 150
        self.background_color = background_color
        self.txt_color = txt_color
        self.size = size
        self.mouse_was_clicked = pygame.mouse.get_pressed()[0]
        
        if sound_info is not None:
            if isinstance(sound_info, list | tuple):
                if len(sound_info) == 2:
                    if isinstance(sound_info[0], list | tuple):
                        self.clicked_sound = pygame.mixer.Sound(sound_info[0][0])
                        self.hover_sound = pygame.mixer.Sound(sound_info[1][0])
                        self.clicked_sound.set_volume(sound_info[0][1])
                        self.hover_sound.set_volume(sound_info[1][1])
                    else:
                        self.clicked_sound = pygame.mixer.Sound(sound_info[0])
                        self.clicked_sound.set_volume(sound_info[1])
                        self.hover_sound = None
                else:
                    raise Exception('Too many arguements passed')
            elif isinstance(sound_info, str):
                self.clicked_sound = pygame.mixer.Sound(sound_info)
                self.hover_sound = None
            else:
                raise TypeError('Invalid type passed')
        else:
            self.clicked_sound = None
            self.hover_sound = None
        
        if (txt is not None and txt_color is None) or (txt is None and txt_color is not None) or (txt is None and txt_color is None):
            self.txt_color = background_color
        
        if self.txt is not None:
            self.txt_surf = pygame.transform.scale(pygame.font.Font(size=int(self.size) if isinstance(self.size, int) or isinstance(self.size, float) else int(self.size[1])).render(self.txt, False, self.txt_color), (self.size, self.size) if isinstance(self.size, int) or isinstance(self.size, float) else self.size)
            self.text_surf_rect = self.txt_surf.get_rect(topleft=position)
        else:
            if isinstance(size, int) or isinstance(size, float):
                the_size = (size, size)
            else:
                the_size = size
                
            self.text_surf_rect = pygame.Rect(*position, *the_size)
        
        self.button_rect = pygame.Rect(self.position[0] - (self.bg_offset/2), self.position[1] - (self.bg_offset/2), self.text_surf_rect.width + self.bg_offset, self.text_surf_rect.height + self.bg_offset)
    
    def on_hover(self, action_performed):
        self.button_opacity = self.on_hover_opacity
        if action_performed is not None:
            action_performed()
    
    def _mouse_clicked(self, mouse_rect: pygame.Rect, target: pygame.Rect, clicked: bool, hover_func, not_hover_func, hover_sound: pygame.mixer.Sound):
        mouse_collission = mouse_rect.colliderect(target)
        if hover_sound is not None:
            if mouse_collission and self.start_playing_hover_sound:
                hover_sound.play()
                self.start_playing_hover_sound = False
        
        if mouse_collission:
            hover_func()
        else:
            self.start_playing_hover_sound = True
            not_hover_func()
            
        if clicked and mouse_collission:
            self.clicked = True
        if not clicked:
            self.clicked = False

        if not self.clicked and not mouse_collission:
            self.clicked_outside = False
        if not clicked:
            self.clicked_outside = True
        
        return self.clicked and self.clicked_outside
    
    def isclicked(self, mouse_rect: pygame.Rect, target: pygame.Rect, clicked: bool, hover_func, not_hover_func, click_func, not_clicked_func, hover_sound=None):
        mouse_clicked = self._mouse_clicked(mouse_rect, target, clicked, hover_func, not_hover_func, hover_sound)
        if mouse_clicked:
            click_func()
        else:
            not_clicked_func()
    
    def get_rect(self):
        return self.button_rect
    
    def set_rect(self, left: float = None, top: float = None, width: float = None, height: float = None, centerx: float = None, centery: float = None):
        if left is not None:
            self.button_rect.left = left
        if top is not None:
            self.button_rect.top = top
        if width is not None:
            self.button_rect.width = width
        if height is not None:
            self.button_rect.height = height
        if centerx is not None:
            self.button_rect.centerx = centerx
        if centery is not None:
            self.button_rect.centery = centery
    
    def _clicking(self, state: str, action_performed, action_on_not_click, action_on_hover):
        match state:
            case'click':
                self.button_opacity = self.on_click_opacity
                if self.start_click_check:
                    if self.clicked_sound is not None:
                        self.clicked_sound.play()
                    if action_performed is not None:
                        action_performed()
                    self.start_click_check = False
            
            case 'unclick':
                if action_on_not_click is not None:
                    action_on_not_click()
            
            case 'hover':
                self.on_hover(action_on_hover)
            
            case 'unhover':
                self.button_opacity = 255
    
    def on_activate(self, mouse_rect, mouse_was_clicked, action_performed, action_on_hover, action_on_not_click, no_bounce: bool, sound_info: tuple):
        if self.txt is not None:
            self.txt_surf = pygame.transform.scale(pygame.font.Font(size=int(self.size) if isinstance(self.size, int) or isinstance(self.size, float) else int(self.size[1])).render(self.txt, False, self.txt_color), (self.size, self.size) if isinstance(self.size, int) or isinstance(self.size, float) else self.size)
        
        if sound_info is not None:
            self.clicked_sound = pygame.mixer.Sound(self.sound_info[0])
            self.clicked_sound.set_volume(self.sound_info[1])
        
        self.start_click_check = True if no_bounce else self.start_click_check
        
        self.isclicked(mouse_rect,
                       self.button_rect,
                       mouse_was_clicked,
                       hover_func       = lambda: self._clicking('hover'  , action_performed, action_on_not_click, action_on_hover),
                       not_hover_func   = lambda: self._clicking('unhover', action_performed, action_on_not_click, action_on_hover),
                       click_func       = lambda: self._clicking('click'  , action_performed, action_on_not_click, action_on_hover),
                       not_clicked_func = lambda: self._clicking('unclick', action_performed, action_on_not_click, action_on_hover)
                       ,
                       hover_sound=self.hover_sound
                       )
        
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
        
        self.border_radius = int(self.border_radius)
        
        pygame.draw.rect(self.screen, background_color, self.button_rect, 0, self.border_radius, self.border_radius, self.border_radius, self.border_radius, self.border_radius)
        
        if self.txt is not None:
            if pos is not None:
                self.text_surf_rect.x = pos[0]
                self.text_surf_rect.y = pos[1]
            
            self.txt_surf = pygame.transform.scale(pygame.font.Font(size=int(self.size) if isinstance(self.size, int) or isinstance(self.size, float) else int(self.size[1])).render(self.txt, False, self.txt_color), (self.size, self.size) if isinstance(self.size, int) or isinstance(self.size, float) else self.size)
            self.text_surf_rect = self.txt_surf.get_rect(topleft=(self.button_rect.topleft[0] + (self.bg_offset/2), self.button_rect.topleft[1] + (self.bg_offset/2)))
            
            self.screen.blit(self.txt_surf, self.text_surf_rect)

    def activate_button(self, mouse_rect: pygame.Rect, mouse_clicked: bool, on_click=None, on_hover=None, on_not_click=None, pos=None, color: tuple | Any = None, no_bounce=False, sound_info: tuple = None, text: str = None):
        '''
        color: (Background color, Text color) | Background color
        '''
        if text is not None:
            self.txt = text
            self.txt_surf = pygame.transform.scale(pygame.font.Font(size=int(self.size) if isinstance(self.size, int) or isinstance(self.size, float) else int(self.size[1])).render(self.txt, False, self.txt_color), (self.size, self.size) if isinstance(self.size, int) or isinstance(self.size, float) else self.size)
            self.text_surf_rect = self.txt_surf.get_rect(topleft=self.position)
        if not self.disabled:
            self.on_activate(mouse_rect, mouse_clicked, on_click, on_hover, on_not_click, no_bounce, sound_info)
        self.draw(pos, color, disabled=self.disabled)

class Selector:
    def __init__(self, screen: pygame.Surface, options: list[str], index: int, pos, font: pygame.font.Font, color, border_radius: int = BORDER_RAD, f_r_width: int = FOCUS_RECT_WIDTH, width: int = None, circular: bool = False):
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
        self.pos = pos
        self.color = color
        self.font = font
        self.circular = circular
        
    def _inc_dec(self, inc: bool, circular: bool):
        if inc:
            if circular:
                if self.index == len(self.options) - 1:
                    self.index = 0
                else:
                    self.index += 1
            else:
                self.index += 1    
        else:
            if circular:
                if self.index == 0:
                    self.index = len(self.options) - 1
                else:
                    self.index -= 1
            else:
                self.index -= 1
    
    def _get_largest_index(self, pos):
        store = 0
        surf = None
        for i in self.options:
            size = self.font.render(i, False, 'red').get_size()
            if size[0] > store:
                store = size[0]
                surf = self.font.render(i, False, 'red')
                rect = surf.get_rect(topleft=pos)
        return surf, rect
    
    def text_and_selector_logic_and_draw(self, mouse_rect: pygame.Rect, mouse_clicked: bool, text_surf: pygame.Surface, text_rect: pygame.Rect, color, options: list, circular: bool):
        self.keys = pygame.key.get_pressed()
        self.index = pygame.math.clamp(self.index, 0, len(self.options) - 1)
        self.value = self.options[self.index]
        
        self.ptr_y = self.outline.top + ((self.outline.height - self.ptr_size) / 2)
        
        if self.assigned:
            self.ptr_left = Button(self.screen, color, ((self.outline.left - self.ptr_size) - 10, self.ptr_y), self.ptr_size)
            self.ptr_right = Button(self.screen, color,(self.outline.right + 10, self.ptr_y), self.ptr_size)
            self.assigned = False
        
        if self.index != len(options) - 1 or circular:
            self.ptr_right.activate_button(mouse_rect, mouse_clicked, on_click=lambda: self._inc_dec(True, circular), pos=((self.outline.left - self.ptr_size) - 10, self.ptr_y), color=color)
        if self.index != 0 or circular:
            self.ptr_left.activate_button(mouse_rect, mouse_clicked, on_click=lambda: self._inc_dec(False, circular), pos=(self.outline.right + 10, self.ptr_y), color=color)

        if self.start_click_check and (self.keys[pygame.K_LEFT] or self.keys[pygame.K_RIGHT]):
            if self.keys[pygame.K_LEFT]:
                self._inc_dec(True, circular)
            elif self.keys[pygame.K_RIGHT]:
                self._inc_dec(False, circular)
            
            self.start_click_check = False
        
        if not self.start_click_check:
            self.click_timer += 1
            if self.click_timer >= 20:
                self.start_click_check = True
                self.click_timer = 0
    
    def draw_val(self, text_surf: pygame.Surface, text_rect: pygame.Rect):
        self.screen.blit(text_surf, text_rect)
    
    def display_outline(self, color):
        self.outline = pygame.Rect(self.outline_rect.x - X_OPTION_SPACE_OFFSET//2,
                                   self.outline_rect.y,
                                   (self.outline_surf.get_width() + X_OPTION_SPACE_OFFSET) if self.width is None else self.width,
                                   self.outline_surf.get_height()
                                    )
        pygame.draw.rect(self.screen, color, self.outline, self.f_r_width, self.border_radius, self.border_radius, self.border_radius, self.border_radius, self.border_radius)
    
    def draw(self, mouse_rect: pygame.Rect, mouse_clicked: bool, color, pos, draw_val, text_surf: pygame.Surface, text_rect: pygame.Rect, options, circular: bool):
        self.outline_surf, self.outline_rect = self._get_largest_index(pos)
        
        self.text_surf = self.font.render(self.value, False, color)
        self.text_rect = self.text_surf.get_rect(center=self.outline_rect.center)

        self.display_outline(color)
        self.text_and_selector_logic_and_draw(mouse_rect, mouse_clicked, self.text_surf, self.text_rect, color, options, circular)
        
        if text_surf is not None:
            self.text_surf = text_surf
        if text_rect is not None:
            self.text_rect = text_rect
        
        if draw_val:
            self.draw_val(self.text_surf, self.text_rect)
    
    def activate_selector(self, mouse_rect: pygame.Rect, mouse_clicked: bool, draw_val = True, text_surf: pygame.Surface = None, text_rect: pygame.Rect = None, pos = None, color = None, options = None, circular = None):
        if color is not None:
            self.color = color
        if options is not None:
            self.options = options
        if pos is not None:
            self.pos = pos
        if circular is not None:
            self.circular = circular
        
        self.draw(mouse_rect, mouse_clicked, self.color, self.pos, draw_val, text_surf, text_rect, self.options, self.circular)
        
        return self.value, self.index

class InputSeletor:
    def __init__(self, screen: pygame.Surface, character: str, bg_color, fg_color, mini_win_title: str, pos: tuple, font: pygame.font.Font, outline_color, mini_win_logo_path = None, border_radius: int = BORDER_RAD, mini_outline_width: int = 700, mini_outline_height: int = 120, main_outline_width: int = X_OPTION_SPACE_OFFSET, f_r_width: int = FOCUS_RECT_WIDTH, win_pos = None, _prefix: str = '', suffix_: str = '') -> None:
        self.character = self.blit_char = self.display_char = character
        self.suffix_ = suffix_
        self._prefix = _prefix
        self.special_keys = SPECIAL_KEYS
        self.display_ord = self.special_keys.get(self.character) if self.special_keys.get(self.character) is not None else ord(self.character)
        self.outline_opacity = 255
        self.screen = screen
        self.mini_outline_width = mini_outline_width
        self.mini_outline_height = mini_outline_height
        self.main_outline_width = main_outline_width
        self.border_radius = border_radius
        self.f_r_width = f_r_width
        self.bg_color = bg_color
        self.fg_color = fg_color
        self.pos = pos
        self.font = font
        self.outline_color = outline_color
        
        self.mini_win_size = 300
        self.txt_size = self.mini_win_size // 2

        self.keys = pygame.key.get_pressed()
        self.click_timer = 0

        self.mini_win_active = False
        
        win_pos = [(self.screen.get_width() / 2) - (self.mini_win_size / 2), (self.screen.get_height() / 2) - (self.mini_win_size / 2)] if win_pos is None else win_pos
        self.mini_win = _MiniWindow(self.screen,
                                   self.mini_win_size,
                                   win_pos,
                                   mini_win_title,
                                   self.fg_color,
                                   self.bg_color,
                                   mods.set_color(self.bg_color, 120),
                                   window_activated=self.mini_win_active,
                                   logo=mini_win_logo_path)

        self.start_click_check = True
        self.start_click_check = True
        self.clicked_outside = True
        self.start_the_check = False
        self.check_it_now = False
    
    def _set_outline_color(self, opac: int):
        self.outline_opacity = opac
    
    def char_input(self):
        for i in range(len(self.keys)):
            invalids_not_clciked = not self.keys[pygame.K_ESCAPE] and not self.keys[pygame.K_RETURN] and not self.keys[pygame.K_BACKSPACE]
            if self.keys[i] and i not in [k for _, k in self.special_keys.items()] and invalids_not_clciked:
                self.character = chr(i)
                self.display_ord = i
        
    def get_special_keys(self):
        for k, v in list(zip([k for k, _ in self.special_keys.items()], [v for _, v in self.special_keys.items()])):
            if self.keys[v]:
                self.character = k
                self.display_ord = v
    
    def isclicked(self, mouse_rect: pygame.Rect, target: pygame.Rect, clicked: bool, func = None):
        if clicked and (not mouse_rect.colliderect(target)):
            self.clicked_outside = True
        elif not clicked:
            self.clicked_outside = False
        
        if mouse_rect.colliderect(target) and not self.clicked_outside:
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
        
        self.mini_win.add_widgets(mini_widgets)
        self.mini_win.activate_window(mouse_rect, clicked, colors=colors, rel=rel)
        
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
    
    def draw_val(self, text_surf: pygame.Surface, text_rect: pygame.Rect):
        if not self.mini_win.isactive():
            self.blit_char = self.character
        self.screen.blit(text_surf, text_rect)
    
    def draw(self, draw_val, color, text_surf: pygame.Surface, text_rect: pygame.Rect):
        if color is not None:
            self.fg_color = color
        
        self.text_surf = self.font.render(f'{self._prefix}{self.blit_char}{self.suffix_}', False, self.fg_color)
        self.text_rect = self.text_surf.get_rect(topleft=self.pos)
        
        if text_surf is not None:
            self.text_surf = text_surf
        if text_rect is not None:
            self.text_rect = text_rect
        
        self.display_outline(self.text_surf, self.text_rect, self.fg_color)
        if draw_val:
            self.draw_val(self.text_surf, self.text_rect)
    
    def activate_input_selector(self, mouse_rect: pygame.Rect, clicked: bool, rel, color=None, min_win_bg_color=None, mini_win_fg_color=None, draw_val = True, text_surf: pygame.Surface = None, text_rect: pygame.Rect = None):
        self.draw(draw_val, color, text_surf, text_rect)
        
        self.mini_prompt_window(mouse_rect, clicked, rel, mini_win_fg_color, min_win_bg_color)
        self.open_mini_window(mouse_rect, self.main_outline, clicked)
        
        return str(self.display_char), self.display_ord

class _MiniWindow:
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
        self.exit_button = Button(self.main_window, 'red', (self.title_bar_rect.right - self.btn_size - self.offset, self.title_bar_rect.top + self.offset), self.btn_size, border_radius=0, txt='x', txt_color='black')

    def set_window_state(self, close_window):
        self.window_activated = not close_window
    
    def isclicked(self, mouse_rect: pygame.Rect, target: pygame.Rect, clicked: bool, func = None):
        if clicked and (not mouse_rect.colliderect(target)):
            self.clicked_outside = True
        elif not clicked:
            self.clicked_outside = False
        
        if mouse_rect.colliderect(target) and not self.clicked_outside:
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
    
    def draw_window(self, mouse_rect: pygame.Rect, clicked: bool, colors: dict = None, rel = None):
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
            
            self.exit_button.activate_button(mouse_rect, clicked, lambda: self.set_window_state(True), pos=(self.exit_button.button_rect.x + self.btn_move[0], self.exit_button.button_rect.y + self.btn_move[1]))

    def add_widgets(self, widgets: tuple[tuple[str, pygame.Surface | pygame.Color, pygame.Rect, Any, str]] = None):
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
    
    def activate_window(self, mouse_rect, clicked, colors: dict = None, rel=None):
        self.draw_window(mouse_rect, clicked, colors, rel)
        self.check_win_moved(mouse_rect, clicked)

class Slider:
    def __init__(self, screen: pygame.Surface, pos: tuple, length, color, key_clicked_left = None, key_clicked_right = None, init_val: float = 50.0, max_thresh: float = 100.0, min_thresh: float = 0.0, write_number = True, inc_val = None) -> None:
        self.screen = screen
        self.length = length
        self.init_val = init_val
        self.max_thresh = max_thresh
        self.min_thresh = min_thresh
        self.key_clicked_left = key_clicked_left
        self.key_clicked_right = key_clicked_right
        self.write_number = write_number
        self.color = color
        self.inc_val = (self.length / self.max_thresh) if inc_val is None else inc_val
        self.mouse_was_clicked = False
        self.clicked_outside = False
        self.clicked = False
        
        origin, coords = pos
        x, y = coords
        line_height = 5
        
        match origin:
            case 'topleft':
                self.slider_line_rect_bg = pygame.Rect(x, y, length, line_height)
            case 'bottomleft':
                self.slider_line_rect_bg = pygame.Rect(x, y + line_height, length, line_height)
            case 'topright':
                self.slider_line_rect_bg = pygame.Rect(x + length, y, length, line_height)
            case 'bottomright':
                self.slider_line_rect_bg = pygame.Rect(x + length, y + line_height, length, line_height)
            case 'midtop':
                self.slider_line_rect_bg = pygame.Rect(x + (length / 2), y, length, line_height)
            case 'midbottom':
                self.slider_line_rect_bg = pygame.Rect(x + (length / 2), y + line_height, length, line_height)
            case 'midleft':
                self.slider_line_rect_bg = pygame.Rect(x, y + (line_height / 2), length, line_height)
            case 'midright':
                self.slider_line_rect_bg = pygame.Rect(x + length, y + (line_height / 2), length, line_height)
            case 'center':
                self.slider_line_rect_bg = pygame.Rect(x + (length / 2), y + (line_height / 2), length, line_height)
        
        self.slider_line_rect = self.slider_line_rect_bg.copy()
        
        self.ball_size = line_height * 3
        self.ball_y = y - (self.ball_size / 2) + (line_height / 2)
        self.ball_x = ((self.init_val/self.max_thresh) * (self.slider_line_rect_bg.width - self.ball_size)) + self.slider_line_rect_bg.left
        self.slider_ball_rect = pygame.Rect(self.ball_x, self.ball_y, self.ball_size, self.ball_size)
    
    def _get_correct_click_instance_no2(self, mouse_rect: pygame.Rect, target: pygame.Rect, clicked: bool):
        collision = mouse_rect.colliderect(target)
        
        if collision and clicked:
            return True
        return False
    
    def _mouse_clicked(self, mouse_rect: pygame.Rect, target: pygame.Rect, clicked: bool, hover_func, not_hover_func, hover_sound: pygame.mixer.Sound):
        mouse_collission = mouse_rect.colliderect(target)
        
        if hover_sound is not None:
            if mouse_collission and self.start_playing_hover_sound:
                hover_sound.play()
                self.start_playing_hover_sound = False
        
        if mouse_collission:
            if hover_func:
                hover_func()
        else:
            self.start_playing_hover_sound = True
            if not_hover_func:
                not_hover_func()
            
        if clicked and mouse_collission:
            self.clicked = True
        if not clicked:
            self.clicked = False

        if not self.clicked and not mouse_collission:
            self.clicked_outside = False
        if not clicked:
            self.clicked_outside = True
        return self.clicked and self.clicked_outside
    
    def _isclicked(self, mouse_rect: pygame.Rect, target: pygame.Rect, clicked: bool, hover_func = None, not_hover_func = None, click_func = None, not_clicked_func = None, hover_sound=None):
        mouse_clicked = self._mouse_clicked(mouse_rect, target, clicked, hover_func, not_hover_func, hover_sound)
        
        if mouse_clicked:
            if click_func:
                click_func()
        else:
            if not_clicked_func:
                not_clicked_func()
        
        return mouse_clicked
    
    def key_move(self, key_clicked_left: int = None, key_clicked_right: int = None):
        if key_clicked_left is not None:
            self.key_clicked_left = key_clicked_left
        
        if key_clicked_right is not None:
            self.key_clicked_right = key_clicked_right
        
        if None not in (self.key_clicked_left, self.key_clicked_right):
            keys = pygame.key.get_pressed()
    
            ball_x_pos = ((self.init_val/self.max_thresh) * ((self.slider_line_rect_bg.width - self.ball_size)) + self.slider_line_rect_bg.left)
            self.slider_line_rect.width = self.ball_x - self.slider_line_rect_bg.left
            if keys[self.key_clicked_right]:
                self.init_val += self.inc_val
                self.ball_x = ball_x_pos
            if keys[self.key_clicked_left]:
                self.init_val -= self.inc_val
                self.ball_x = ball_x_pos
            
    def mouse_move(self, mouse_rect: pygame.Rect, mouse_clicked: bool, mouse_rel: tuple[int]):
        if self._isclicked(mouse_rect, self.slider_ball_rect, mouse_clicked):
                self.ball_x = mouse_rect.x - (self.slider_ball_rect.width / 2)
                self.slider_line_rect.width = self.ball_x - self.slider_line_rect.left
                self.init_val = ((self.slider_line_rect_bg.left - self.ball_x) / (self.slider_ball_rect.width - self.slider_line_rect_bg.width)) * self.max_thresh
        
    def const_update(self):
        self.ball_x = pygame.math.clamp(self.ball_x, self.slider_line_rect_bg.left, self.slider_line_rect_bg.right - self.slider_ball_rect.width)
        self.slider_line_rect.width = self.ball_x - self.slider_line_rect_bg.left
        self.init_val = pygame.math.clamp(self.init_val, self.min_thresh, self.max_thresh)
        self.init_val = round(self.init_val, 1)

        self.slider_ball_rect.x = self.ball_x
    
    def draw(self, color):
        if color is not None:
            self.color = color
        
        pygame.draw.rect(self.screen, mods.set_color(self.color, 200), self.slider_line_rect_bg)
        pygame.draw.ellipse(self.screen, self.color, self.slider_ball_rect, self.ball_size)
        pygame.draw.rect(self.screen, self.color, self.slider_line_rect)
        
        if self.write_number:
            number_offset = 20
            number = pygame.font.Font(size=25).render(f'{self.init_val}', False, 'white')
            number_rect = number.get_rect(center=(self.slider_line_rect_bg.right + number_offset, self.slider_ball_rect.centery))
            
            self.screen.blit(number, number_rect)
        
    def activate_slider(self, mouse_rect, mouse_clicked, mouse_rel, key_clicked_left = None, key_clicked_right = None, color = None):
        self.draw(color)
        self.key_move(key_clicked_left, key_clicked_right)
        self.mouse_move(mouse_rect, mouse_clicked, mouse_rel)
        self.const_update()
    
        return self.init_val

class Text(Input):
    def __init__(self, screen: pygame.Surface, init_input: str, pos: list, font: pygame.font.Font, fg_color, directory = 'utils/json/continue.json', key = 'key', debug: bool = False) -> None:
        super().__init__(screen, init_input, 100, pos, font, fg_color, 0, 0, 0, 0)
        self.debug = debug
        if self.debug:
            self.dir = directory
            self.key = key
            self.mouse_x_dist = 1
            self.mouse_y_dist = 1
            self.pos = self._load_position(self.dir)['pos']
            self.tv_input = self._load_position(self.dir)['text']
            self.cursor = len(self.tv_input)
            *self.words_list, = str(self.tv_input)
            self.rotate_button = Button(self.screen, self.fg_color, (self.screen.get_width() / 2, self.screen.get_height() / 2), 100)
            self.update_rotational_dir = True
            self.just_started = True
            self.angle = 0
    
    def _load_position(self, directory):
        try:
            with open(directory) as d:
                self.vals = json.loads(d.read())
            vals = self.vals[self.key]
            
        except KeyError:
            self.vals[self.key] = {}
            self.vals[self.key]['pos'] = self.pos
            self.vals[self.key]['text'] = self.tv_input
            vals = self.vals[self.key]

        return vals
    
    def _save_position(self, directory, pos, text):
        self.vals[self.key]['pos'] = pos
        self.vals[self.key]['text'] = text
        with open(directory, 'w') as d:
            info = json.dumps(self.vals, indent=2)
            d.write(info)
    
    def _get_correct_click_instance(self, mouse_rect: pygame.Rect, target: pygame.Rect, clicked: bool, not_clicked: bool):
        self.clicked_outside = False
        self.within_click_area = mouse_rect.colliderect(target)
        
        if not self.within_click_area:
            if not self.mouse_was_clicked and clicked:
                self.outside_of_bounds = True
            elif not clicked:
                self.outside_of_bounds = False
        
        if self.clicked_outside and self.within_click_area:
            self.clicked_outside = False
        
        if not clicked and not self.within_click_area:
            self.mouse_was_clicked = False
        
        if clicked and self.within_click_area:
            self.mouse_was_clicked = True
        
        self.mouse_was_clicked = (not self.within_click_area and clicked) if not_clicked else self.mouse_was_clicked
        self.outside_of_bounds = (not self.outside_of_bounds) if not_clicked else self.outside_of_bounds
        
        return self.mouse_was_clicked and not self.outside_of_bounds
    
    def isclicked(self, mouse_rect: pygame.Rect, target: pygame.Rect, clicked: bool, on_click_func = None, on_hover_func = None, not_clicked = False):
        is_clicked_correctly = self._get_correct_click_instance(mouse_rect, target, clicked, not_clicked)
        if mouse_rect.colliderect(target):
            if is_clicked_correctly:
                if on_hover_func is not None:
                    on_hover_func()
                if on_click_func is not None:
                    if clicked:
                        on_click_func()
                return clicked
        return False
    # Fix the clicked problem
     
    def draw_outline(self, text_surf: pygame.Surface, text_rect: pygame.Rect, fg_color, width: int | float):
        pass
    
    def partial_activate_text_view(self, clicked: bool, rel: tuple, draw_words=True, text_surf: pygame.Surface = None, text_rect: pygame.Rect = None, fg_color=None, bg_color=None, width: int = None):
        pass
    
    def activate_text_view(self, mouse_rect: pygame.Rect, clicked: bool, draw_words=True, text_surf: pygame.Surface = None, text_rect: pygame.Rect = None, fg_color=None, bg_color=None, width: int = None):
        pass
    
    def _activate_label(self, mouse_rect: pygame.Rect, clicked: bool, draw_words = True, text_surf: pygame.Surface = None, text_rect: pygame.Rect = None, fg_color = None, bg_color = None, width: int = None, text: str = None, func=None):
        if text is not None:
            def a_function():
                self.text_surf = self.font.render(text, False, self.fg_color)
                self.text_rect = self.text_surf.get_rect(topleft=self.pos)
        else:
            def a_function():
                pass
            if func is not None:
                def a_function():
                    func()
        
        self._constant_update(mouse_rect, self.outline, draw_words, clicked, text_surf, text_rect, fg_color, bg_color, width, func = a_function)
        if self.enabled:
            self.tv_special_keys()
            self.text_view_input()
        
        if not self.debug:
            self.enabled = False

        return self.tv_input
    
    def activate_label(self, mouse_rect: pygame.Rect, clicked: bool, rel: tuple, draw_words = True, text_surf: pygame.Surface = None, text_rect: pygame.Rect = None, fg_color = None, bg_color = None, width: int = None, text: str = None):
        if self.debug:
            mouse_is_moving = rel not in ((0, 0), [0, 0])
            
            if clicked and not mouse_rect.colliderect(self.text_rect):
                self.enabled = False
            else:
                if self.isclicked(mouse_rect, self.text_rect, clicked):
                    if mouse_is_moving:
                        self.enabled = True
                        self.pos[0] = mouse_rect.x
                        self.pos[1] = mouse_rect.y
            
            def rotational_movement(part: int):
                if part == 1:
                    self.mouse_x_dist = mouse_rect.x - self.pos[0]
                    self.mouse_y_dist = -(mouse_rect.y - self.pos[1])
                    self.angle = math.degrees(math.atan2(self.mouse_y_dist, self.mouse_x_dist))
                    self.text_surf = pygame.transform.rotate(self.text_surf, self.angle - 90)
                    self.text_rect = self.text_surf.get_rect(center=self.pos)
                    self.update_rotational_dir = False
                
                elif part == 2:
                    if self.just_started:
                        self.angle = 0
                        self.just_started = False
                        
                    self.text_surf = pygame.transform.rotate(self.text_surf, self.angle)
            print(self.angle)
            # def center():
            #     self.text_rect = self.text_surf.get_rect(center=self.pos)
            
            self._activate_label(mouse_rect,
                                 clicked,
                                 draw_words,
                                 text_surf,
                                 text_rect,
                                 fg_color,
                                 bg_color,
                                 width,
                                 func=lambda: self.rotate_button.activate_button(mouse_rect,
                                                                                 clicked, 
                                                                                 on_click=lambda: rotational_movement(1),
                                                                                 on_not_click=lambda: rotational_movement(2),
                                                                                #  pos=(self.pos[0],
                                                                                #       self.pos[1] - 20
                                                                                #       )
                                                                                 )
                                 )
            if self.enabled:
                self.draw_cursor(self.text_surf, self.text_rect, self.fg_color)
            
            for _ in pygame.event.get():
                self.thread = Thread(target=self._save_position, args=(self.dir, self.pos, self.tv_input))
                self.thread.start()
        
        else:
            self._activate_label(mouse_rect, clicked, draw_words, text_surf, text_rect, fg_color, bg_color, width, text)

class ClickableText:
    def __init__(self, screen: pygame.Surface, text: str, font: pygame.font.Font, color, scr_color, pos: tuple | list, sound_info=None) -> None:
        self.screen = screen
        self.text = text
        self.color = color
        self.scr_color = scr_color
        self.font = font
        self.start_playing_hover_sound = True
        
        self.text_surf = self.font.render(text, False, color)
        self.text_rect = self.text_surf.get_rect(topleft=pos)
        
        hover_bg_offset = 20
        dest_size = self.text_surf.get_size()[0] + hover_bg_offset, self.text_surf.get_size()[1] + hover_bg_offset
        
        self.hover_rect = pygame.Rect(self.text_rect.center[0] - (dest_size[0] / 2), self.text_rect.center[1] - (dest_size[1] / 2), *dest_size)
        
        self.bounce_delay = 10
        self.start_click_check = False
        self.clicked = False
        self.click_timer = 0
    
        if sound_info is not None:
            if isinstance(sound_info, list | tuple):
                if len(sound_info) == 2:
                    if isinstance(sound_info[0], list | tuple):
                        self.clicked_sound = pygame.mixer.Sound(sound_info[0][0])
                        self.hover_sound = pygame.mixer.Sound(sound_info[1][0])
                        self.clicked_sound.set_volume(sound_info[0][1])
                        self.hover_sound.set_volume(sound_info[1][1])
                    else:
                        self.clicked_sound = pygame.mixer.Sound(sound_info[0])
                        self.clicked_sound.set_volume(sound_info[1])
                        self.hover_sound = None
                else:
                    raise Exception('Too many arguements passed')
            elif isinstance(sound_info, str):
                self.clicked_sound = pygame.mixer.Sound(sound_info)
                self.hover_sound = None
            else:
                raise TypeError('Invalid type passed')
        else:
            self.clicked_sound = None
            self.hover_sound = None
        
    def _mouse_clicked(self, mouse_rect: pygame.Rect, target: pygame.Rect, clicked: bool, mouse_rel, hover_func, not_hover_func, hover_sound: pygame.mixer.Sound):
        mouse_collission = mouse_rect.colliderect(target)
        if hover_sound is not None:
            if mouse_collission and self.start_playing_hover_sound: # and mouse_rel != (0, 0):
                hover_sound.play()
                self.start_playing_hover_sound = False
        
        if mouse_collission:
            if hover_func:
                hover_func()
        else:
            self.start_playing_hover_sound = True
            if not_hover_func:
                not_hover_func()
            
        if clicked and mouse_collission:
            self.clicked = True
        if not clicked:
            self.clicked = False

        if not self.clicked and not mouse_collission:
            self.clicked_outside = False
        if not clicked:
            self.clicked_outside = True
        
        return self.clicked and self.clicked_outside
    
    def _isclicked(self, mouse_rect: pygame.Rect, target: pygame.Rect, clicked: bool, mouse_rel, hover_func = None, not_hover_func = None, click_func = None, not_clicked_func = None, hover_sound=None):
        mouse_clicked = self._mouse_clicked(mouse_rect, target, clicked, mouse_rel, hover_func, not_hover_func, hover_sound)
        
        if mouse_clicked:
            if click_func:
                click_func()
        else:
            if not_clicked_func:
                not_clicked_func()
        
        return mouse_clicked
    
    def _on_hover(self, mouse_rel):
        # if mouse_rel != (0, 0):
        pygame.draw.rect(self.screen, mods.set_color(self.scr_color, 200), self.hover_rect, 0, 100)
        # self.screen.blit(self.hover_img, self.hover_rect)
        
    def _check_clicked(self, mouse_rect: pygame.Rect, clicked: bool, mouse_rel, func):
        if self._isclicked(mouse_rect, self.hover_rect, clicked, mouse_rel, hover_func=lambda: self._on_hover(mouse_rel), hover_sound=self.hover_sound):
            self.color_opac = 200
        else:
            self.color_opac = 255
        
        if self._isclicked(mouse_rect, self.hover_rect, clicked, mouse_rel, hover_func=lambda: self._on_hover(mouse_rel)) and self.start_click_check:
            if self.clicked_sound is not None:
                self.clicked_sound.play()
            func()
            self.start_click_check = False
        
        if not self.start_click_check:
            self.click_timer += 1
            if self.click_timer >= self.bounce_delay:
                self.start_click_check = True
                self.click_timer = 0
        
        color = mods.set_color(self.color, self.color_opac)
        self.text_surf = self.font.render(self.text, False, color)
            
    def _draw(self):
        self.screen.blit(self.text_surf, self.text_rect)
    
    def activate_text(self, mouse_rect: pygame.Rect, clicked: bool, func):
        self._check_clicked(mouse_rect, clicked, (), func)
        self._draw()



