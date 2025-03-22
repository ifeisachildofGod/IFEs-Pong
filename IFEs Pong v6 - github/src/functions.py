
import os
import math
import pygame
from src.constants import *

general_font_size = 12

# Text functions
def font_renderer(txt, font: pygame.font.Font, color):
    return font.render(str(txt), False, color)

def font_rect_renderer(screen: pygame.Surface, txt, font_surf: pygame.Surface, y: int = 0, x_offset: int = 0):
    width = font_surf.get_width()
    for i in str(txt):
        adjust = CURSOR_ADJUST.get(i)
        if adjust is not None:
            width += adjust
    
    return pygame.Rect(((screen.get_width() / 2) - (width / 2)) + x_offset, y, width, font_surf.get_height())

# Functions that help with complex things that I can't do in the main file
def _split_help_text(text: str):
    t = text.replace('`', '*!')
    t = t.replace('|', '!*')
    t = t.split('\n')
    t = '&'.join(t)
    t = t.split('*')
    t = '&'.join(t)
    t = t.split('&')
    
    return t

def multiline_write(intial_pos: tuple, txt: str, font: pygame.font.Font, link_col, color):
    t = _split_help_text(txt)
    surf = [(font.render(text_value.replace('!',''), False, link_col if '!' in text_value else color), font.render(text_value.replace('!',''), False, link_col if '!' in text_value else color).get_rect(topleft=(intial_pos[0], intial_pos[1] + (text_index * (general_font_size + 20))))) for text_index, text_value in enumerate(t)]
    list_val = [i.replace('!','') for i in t]
    
    return surf, list_val
    
def draw_nums(screen: pygame.Surface, txt, y: int, cell_size: int, left: bool, color, img: pygame.Surface | None = None):
    text = str(txt)
    if img is not None:
        img = pygame.transform.scale(img, (cell_size, cell_size))
    if left:
        scr_width = (screen.get_width() / 2) - (8 * cell_size) - 9
    else:
        scr_width = (screen.get_width() / 2) + (cell_size / 2)
    temp_x = scr_width
    for k, _ in enumerate(text):
        for i in SCORE_FONTS[int(text[k])]:
            if i == '#':
                scr_width += cell_size
                pygame.draw.rect(screen, color, pygame.Rect(scr_width, y, cell_size, cell_size)) if img is None else screen.blit(img, (scr_width, y))
            else:
                if i == '\n':
                    scr_width = temp_x
                    y += cell_size
                elif i == ' ':
                    scr_width += cell_size

def check_valid_color(color_val, orig_val):
    valid = False
    for i in str(color_val):
        if i == ' ':
            valid = False
        else:
            valid = True
            break
    
    if len(str(color_val)) != 0 and valid:
        if isinstance(color_val, str):
            current_val = []
            if len(color_val) <= 10:
                for i in color_val:
                    if i in ('1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f', '.', '#'):
                        current_val.append(i)
                if len(current_val) == 7:
                    if current_val[0] == '.' or current_val[0] == '#':
                        color_val = color_val.replace('.', '#')
                    else:
                        if ''.join(current_val).isdecimal() and current_val[0] != '.':
                            color_val = int(''.join(current_val))
                else:
                    if ''.join(current_val).isdecimal() and current_val[0] != '.':
                        color_val = int(''.join(current_val))
        elif isinstance(color_val, tuple):
            pass
        try:
            pygame.Surface((1,2)).fill(color_val)
        except (ValueError, SystemError):
            color_val = orig_val
        
        return color_val
    
    return orig_val

def list_intersect(first_list: list, second_list: list):
    if len(second_list) > len(first_list):
        list_oo1 = second_list.copy()
        list_oo2 = first_list.copy()
    else:
        list_oo1 = first_list.copy()
        list_oo2 = second_list.copy()
    
    final_list = list_oo2.copy()
    
    for i in list_oo1:
        if i not in list_oo2:
            final_list.append(i)
        
    return final_list

def multiplayer_multiline_update(screen: pygame.Surface, objects, y_offset: int, ct_func, params_for_clickabletext_before_ct_func: tuple):
    for obj in objects:
        if not isinstance(obj, tuple | list):
            obj.activate_text(*params_for_clickabletext_before_ct_func, lambda: ct_func(obj), (obj.pos[0], obj.pos[1] + y_offset))
        else:
            screen.blit(obj[0], (obj[1].x, obj[1].y + y_offset))

# Helper functions
def clamp(val: int, max_val: int, min_val: int):
    return min(max(val,min_val),max_val)

def isclicked(mouse_rect: pygame.Rect, target, clicked: bool, func = None, func2 = None):
    if not (isinstance(target, tuple) or isinstance(target, set)):
        if mouse_rect.colliderect(target):
            if func is not None:
                func()
            return clicked
        else:
            if func2 is not None:
                func2()
            return False
    else:
        x, y = target
        if mouse_rect.collidepoint(x, y):
            if func is not None:
                func()
            return clicked
        else:
            if func2 is not None:
                func2()
            return False

def special_calcualation(num, target, delta):
    if len(str(num).split(".")) > 1:
        index = 1
    else:
        index = 0

    start_delta = float((f'.{str(num).split(".")[index]}') if num > 0 else (f'-.{str(num).split(".")[index]}'))
    num -= start_delta
    if target != num:
        num += delta if num < target else -delta
    return num

def make_font(font_index, size) -> pygame.font.Font:
    font_file = f'src/fonts/font({font_index}).ttf'
    return pygame.font.Font(font_file, size)

def set_color(color, opacity: int) -> ColorType:
    if isinstance(color, str):
        if '#' in color:
            matplib_color = tuple(math.fabs(255 - (col * 255)) for col in pygame.Color(color).cmy)
        else:
            matplib_color = tuple([i/255 for i in pygame.colordict.THECOLORS[color]])
    elif isinstance(color, tuple) or isinstance(color, list):
        matplib_color = tuple([i/255 for i in color])
    elif isinstance(color, int):
        matplib_color = tuple([i/255 for i in pygame.Color(color)])
    else:
        raise Exception('Invalid color argument')

    black = False
    for i in matplib_color[:3]:
        black = i == 0
        if not black:
            break
    
    final_color = [255 - opacity for _ in matplib_color] if black else [int(i * opacity) for i in matplib_color]
    
    if len(final_color) < 4:
        final_color.append(255)
    else:
        final_color[3] = 255
    
    final_color = tuple(final_color)
    
    return final_color

def update_path(path: str):
    return os.path.join(os.getcwd(), path)


