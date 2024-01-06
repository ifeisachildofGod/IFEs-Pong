import pygame
import webbrowser as web
from assets.settings import SCR_WIDTH, SCR_HEIGHT, SCORE_FONTS, FOREGROUND_COL, LINK_COL

# Font writers
def font_renderer(txt, font: pygame.font.Font):
    return font.render(str(txt), False, FOREGROUND_COL)

def font_rect_renderer(txt, font_size, y_offset: int = 0, x_offset: int = 0):
    return pygame.Rect(position(SCR_WIDTH, 'center', str(txt), font_size)+ x_offset, position(SCR_HEIGHT, 'center', ' ', font_size) + y_offset, len(str(txt))*30, 50)

# Functions that help with complex things that I can't do on my own
def multiline_write(txt: str, line_len: int, font: pygame.font.Font): #  Clean this up
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
        
        return surf, [font.render(i, False, FOREGROUND_COL) for i in surf], False
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
            return t, [font.render(i.replace('!',''), False, LINK_COL if '!' in i else FOREGROUND_COL) for i in t], False
        return txt, font.render(txt, False, FOREGROUND_COL), True

def draw_nums(txt: int, x: int, y: int, FONT_CELL_SIZE: int, screen: pygame.Surface, img: pygame.Surface = None):    
    temp_x = x
    for k, _ in enumerate(str(txt)):
        for i in SCORE_FONTS[int(str(txt)[k])]:
            if i == '#':
                x += FONT_CELL_SIZE
                pygame.draw.rect(screen, FOREGROUND_COL, pygame.Rect(x, y, FONT_CELL_SIZE, FONT_CELL_SIZE))\
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

def link_opener(link: str):
    # Opens my links
    web.open(link)

# Helper functions
def position(scr_width: int, justify: str, txt, font_size: int):
    txt = str(txt)
    if justify == 'left':pos = int(scr_width//4-(len(txt)*font_size)/2)
    elif justify == 'center':pos = int(scr_width//2-(font_size*(len(txt)//2)))
    elif justify == 'right':pos = int(((scr_width*3)-(len(txt)*font_size))//4)
    return pos

def clamp(val: int, max_val: int, min_val: int):
    return min(max(val,min_val),max_val)

def repeat(val: int, max_val: int, min_val: int):
    if val > max_val:val = min_val
    elif val < min_val:val = max_val
    return val
