import pygame
import webbrowser as web
from utils.constants import SCR_WIDTH, SCR_HEIGHT, SCORE_FONTS
import json

with open('utils/settings.json') as file:
    saved_color = json.loads(file.read())

    fg_color = saved_color['fg_color']
    link_color = saved_color['link_color']

# Text functions
def font_renderer(txt, font: pygame.font.Font, fore_col = fg_color):
    return font.render(str(txt), False, fore_col)

def font_rect_renderer(txt, font_size, y_offset: int = 0, x_offset: int = 0):
    return pygame.Rect(position(SCR_WIDTH, 'center', str(txt), font_size)+ x_offset, position(SCR_HEIGHT, 'center', ' ', font_size) + y_offset, len(str(txt))*30, 50)

# Functions that help with complex things that I can't do int the main file
def multiline_write(txt: str, line_len: int, font: pygame.font.Font, link_col = link_color, fore_col = fg_color): #  Clean this up
    orig_txt = txt
    div = len(orig_txt)-1
    for _ in range(line_len):
        orig_txt += ' '
    orig_txt = orig_txt[div:]+orig_txt
    rm = ''
    if len(txt) >= line_len and '\n' not in orig_txt:
        temp_len = line_len
        surf = []
        for k, _ in enumerate(orig_txt):
            if (k >= temp_len-line_len and str(orig_txt)[k] == ' ') or orig_txt[k] == '\n':
                temp_len += line_len
                final = orig_txt[line_len : k].replace(rm, '')
                surf.append(final.replace('\n', ''))
                rm = orig_txt[line_len : k]
        surf.remove(surf.pop(0))
        surf[0] = surf[0].removeprefix(' ')
        
        return surf, [font.render(i, False, fore_col) for i in surf], False
    else:
        if '\n' in txt:
            t = txt.replace('`', '*!')
            t = t.replace('|', '!*')
            t = t.split('\n')
            t = '&'.join(t)
            t = t.split('*')
            t = '&'.join(t)
            t = t.split('&')
            t.pop(0)
            t.pop(-1)
            return t, [font.render(i.replace('!',''), False, link_col if '!' in i else fore_col) for i in t], False
        return txt, font.render(txt, False, fore_col), True

def draw_nums(txt: int, x: int, y: int, FONT_CELL_SIZE: int, screen: pygame.Surface, img: pygame.Surface = None, col = fg_color):
    temp_x = x
    for k, _ in enumerate(str(txt)):
        for i in SCORE_FONTS[int(str(txt)[k])]:
            if i == '#':
                x += FONT_CELL_SIZE
                pygame.draw.rect(screen, col, pygame.Rect(x, y, FONT_CELL_SIZE, FONT_CELL_SIZE))\
                    if img is None else screen.blit(
                        pygame.transform.scale(
                                img, 
                                (FONT_CELL_SIZE, FONT_CELL_SIZE),
                                screen),
                        (x,y)
                        )
            else:
                if i == '\n':
                    x = temp_x
                    y += FONT_CELL_SIZE
                elif i == ' ':
                    x += FONT_CELL_SIZE

def correct_color_keys(color: tuple):
    colors = []
    for k, v in enumerate(color):
        if k != len(color)-1:
            colors.append(255-v)
        else:
            colors.append(255)
    return tuple(colors)

def check_valid_color(color_val, orig_val):
    if isinstance(color_val, str):
        current_val = []
        if len(color_val) == 6:
            for i in color_val:
                if i in ('1','2','3','4','5','6','7','8','9','0','a','b','c','d','e','f'):
                    current_val.append(i)
            if len(current_val) == 6:
                color_val = f'#{"".join(current_val)}'
    elif isinstance(color_val, tuple):
        pass
    try:
        pygame.Surface((1,2)).fill(color_val)
    except ValueError:
        color_val = orig_val
    return color_val

def check_valid_file_name(file_val: str, orig_file: str = 'none'):
    try:
        pygame.image.load(orig_file)
    except FileNotFoundError:
        orig_file = 'none'
    except pygame.error:
        orig_file = 'none'
    except TypeError:
        orig_file = 'none'

    if file_val != 'none' and file_val != 'None' and file_val != 'NONE':
        if file_val:
            if file_val.endswith(('.png', '.jpg')):
                if file_val[0] not in ('|','\\','?', '>', '<', '/', '"', ' '):
                    try:
                        pygame.image.load(file_val)
                        final_file =  file_val
                    except FileNotFoundError:
                        final_file =  orig_file
                    except pygame.error:
                        final_file =  orig_file
                else:
                    final_file =  orig_file
            else:
                final_file =  orig_file
        else:
            final_file =  orig_file
    else:
        final_file = 'none'
    
    return final_file

def get_correct_control_key(key: str, point: str):
    from utils.constants import SPECIAL_KEYS
    
    key_char = SPECIAL_KEYS.get(key)

    if key_char is not None:
        return key_char, key
    
    else:
        try:
            key_char = ord(key), key
        except TypeError:
            with open('utils/settings.json') as file:
                saved_output = json.loads(file.read())
                if point == '1u':
                    key_char = SPECIAL_KEYS.get(saved_output['key1_up']) if SPECIAL_KEYS.get(saved_output['key1_up']) is not None else ord(saved_output['key1_up']), saved_output['key1_up']
                elif point == '1d':
                    key_char = SPECIAL_KEYS.get(saved_output['key1_down']) if SPECIAL_KEYS.get(saved_output['key1_down']) is not None else ord(saved_output['key1_down']), saved_output['key1_down']
                elif point == '2u':
                    key_char = SPECIAL_KEYS.get(saved_output['key2_up']) if SPECIAL_KEYS.get(saved_output['key2_up']) is not None else ord(saved_output['key2_up']), saved_output['key2_up']
                elif point == '2d':
                    key_char = SPECIAL_KEYS.get(saved_output['key2_down']) if SPECIAL_KEYS.get(saved_output['key2_down']) is not None else ord(saved_output['key2_down']), saved_output['key2_down']
        
        return key_char

# Helper functions
def position(scr_width: int, justify: str, txt, font_size: int):
    txt = str(txt)
    if justify == 'left':pos = scr_width/4 - (len(txt)*font_size)/2
    elif justify == 'center':pos = scr_width/2 - font_size * (len(txt)/2)
    elif justify == 'right':pos = ((scr_width*3) - (len(txt)*font_size)) / 4
    return pos

def clamp(val: int, max_val: int, min_val: int):
    return min(max(val,min_val),max_val)

def repeat(val: int, max_val: int, min_val: int):
    if val > max_val:val = min_val
    elif val < min_val:val = max_val
    return val

def link_opener(link: str):
    try:
        web.open(link)
    except Exception:
        pass




