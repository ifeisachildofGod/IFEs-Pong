import pygame
import webbrowser as web
from utils.code.constants.game_constants import SCR_WIDTH, SCR_HEIGHT, SCORE_FONTS, CURSOR_ADJUST, SETTINGS_DIR, FN3_SIZE, TXT_PAD
import json
import matplotlib

with open(SETTINGS_DIR) as file:
    saved_color = json.loads(file.read())

    fg_color = saved_color['fg_color']

if isinstance(fg_color, str):
    try:
        matplib_color = fg_color
        matplotlib.colors.to_rgb(matplib_color)
    except ValueError:
        matplib_color = tuple([i/255 for i in pygame.colordict.THECOLORS[fg_color]])
elif isinstance(fg_color, tuple):
    matplib_color = tuple([i/255 for i in fg_color])
elif isinstance(fg_color, int):
    matplib_color = tuple([i/255 for i in pygame.Color(fg_color)])

link_color = [i * 105 for i in matplotlib.colors.to_rgb(matplib_color)]

# Text functions
def font_renderer(txt, font: pygame.font.Font, fore_col = fg_color):
    return font.render(str(txt), False, fore_col)

def font_rect_renderer(txt, font_size, y_offset: int = 0, x_offset: int = 0):
    width = len(str(txt))*font_size
    for i in str(txt).lower():
        if CURSOR_ADJUST.get(i) is not None:
            width += CURSOR_ADJUST.get(i)
    return pygame.Rect(position(SCR_WIDTH, 'center', str(txt), font_size)+ x_offset, position(SCR_HEIGHT, 'center', ' ', font_size) + y_offset, width, font_size*2.5)

# Functions that help with complex things that I can't do in the main file
def multiline_write(txt: str, font: pygame.font.Font, link_col = link_color, fore_col = fg_color, y_val = 0, scr_focus = 0):
    surf_rect = []
    t = txt.replace('`', '*!')
    t = t.replace('|', '!*')
    t = t.split('\n')
    t = '&'.join(t)
    t = t.split('*')
    t = '&'.join(t)
    t = t.split('&')

    surf = [font.render(i.replace('!',''), False, link_col if '!' in i else fore_col) for i in t]
    list_val = [i.replace('!','') for i in t]
    
    for k, _ in enumerate(surf):
        x = position(SCR_WIDTH, 'center', t[k], FN3_SIZE)
        y = clamp(y_val-scr_focus, y_val, -(FN3_SIZE+TXT_PAD + 5))
        surf_rect.append(pygame.Rect(x, y, 0, 0))
    
    return t, surf, list_val, surf_rect
    
def draw_nums(txt: int, scr_width: int, y: int, FONT_CELL_SIZE: int, screen: pygame.Surface, left: bool, img: pygame.Surface = None, col = fg_color):
    if img is not None:
        img = pygame.transform.scale(img, (FONT_CELL_SIZE, FONT_CELL_SIZE))
    if left:
        scr_width = (scr_width / 2) - (8*FONT_CELL_SIZE)-9
    else:
        scr_width = (scr_width / 2) + (FONT_CELL_SIZE / 2)
    temp_x = scr_width
    for k, _ in enumerate(str(txt)):
        for i in SCORE_FONTS[int(str(txt)[k])]:
            if i == '#':
                scr_width += FONT_CELL_SIZE
                pygame.draw.rect(screen, col, pygame.Rect(scr_width, y, FONT_CELL_SIZE, FONT_CELL_SIZE)) if img is None else screen.blit(img, (scr_width, y))
            else:
                if i == '\n':
                    scr_width = temp_x
                    y += FONT_CELL_SIZE
                elif i == ' ':
                    scr_width += FONT_CELL_SIZE

def correct_color_keys(color: tuple):
    colors = []
    for k, v in enumerate(color):
        if k != len(color)-1:
            colors.append(255-v)
        else:
            colors.append(255)
    return tuple(colors)

def check_valid_color(color_val, orig_val):
    for i in str(color_val):
        global valid
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
        except ValueError:
            color_val = orig_val
        
        return color_val
    else:
        return orig_val

def check_valid_file_name(file_val: str, orig_file: str = 'none'):
    try:
        pygame.image.load(f'SKINS/{orig_file}')
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
                        pygame.image.load(f'SKINS/{file_val}')
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

def isclicked(mouse_rect: pygame.Rect, target, clicked: bool, func = None, func2 = None):
    if not (isinstance(target, tuple) or isinstance(target, set)):
        if mouse_rect.colliderect(target):
            if func is not None:
                func()
            return clicked
        else:
            if func2 is not None:
                func2()
            else:
                pass
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
            else:
                pass
            return False

def secs_to_time(secs: int):
    s = secs % 60
    m = ((secs // 60) if secs >= 60 else 0) % 60
    h = ((secs // 3600) if secs >= 3600 else 0) % 24
    
    return f"{h}hrs {m}mins {s}secs"

def set_color(color, opacity: int):
    if isinstance(color, str):
        try:
            matplib_color = color
            matplotlib.colors.to_rgb(matplib_color)
        except ValueError:
            matplib_color = tuple([i/255 for i in pygame.colordict.THECOLORS[color]])
    elif isinstance(color, tuple) or isinstance(color, list):
        matplib_color = tuple([i/255 for i in color])
    elif isinstance(color, int):
        matplib_color = tuple([i/255 for i in pygame.Color(color)])
    else:
        raise Exception('Invalid color argument')

    for i in [i * opacity for i in matplotlib.colors.to_rgb(matplib_color)]:
        black = i == 0
        if not black:
            break
    
    if not black:
        color = [i * opacity for i in matplotlib.colors.to_rgb(matplib_color)]
    else:
        color = [i + (opacity if opacity != 255 else 0) for i in matplotlib.colors.to_rgb(matplib_color)]
    
    return color



