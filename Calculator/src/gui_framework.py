import pygame as pg
from pygame.locals import *
import sys
import src.themes
from src.objecthandler import ObjectHandler
text_theme = src.themes.text_theme


class Text:
    def __init__(self, handler, display_, text_ = "Text here", pos_ = (0, 0), theme_ = "standard"):
        self.text = text_
        self.pos = pos_
        self.posx, self.posy = self.pos
        self.theme = theme_
        self.display = display_
        self.scale_value = 1
        self.offsetx, self.offsety = 0, 0
        self.alignment = 'center'
        self.set_theme(self.theme)
        handler.objects.append(self)


    def set_text(self, text_):
        self.text = text_
        self.update_visuals()
        return self

    def set_pos(self, pos_):
        self.pos = pos_
        self.posx, self.posy = self.pos
        self.update_visuals()
        return self

    def set_font(self, font_name_):
        self.font_name = font_name_
        self.init_font()
        return self

    def set_fontsize(self, fontsize_):
        self.fontsize = fontsize_
        self.init_font()
        return self

    def set_font_colour(self, font_colour_):
        self.font_colour = font_colour_
        self.update_visuals()
        return self

    def init_font(self):
        self.font = pg.font.SysFont(self.font_name, int(self.fontsize))
        self.update_visuals()
        return self

    def set_background_marginal(self, background_size_multiplier_):
        self.background_marginal = background_size_multiplier_
        self.update_visuals()
        return self

    def set_background_colour(self, background_colour_):
        self.background_colour = background_colour_
        self.update_visuals()
        return self

    def inflate_background_size(self, inflation_x, inflation_y):
        self.inflation_x, self.inflation_y = int(inflation_x), int(inflation_y)
        self.update_visuals()
        return self

    def set_background_size(self, bg_width, bg_height):
        self.background_size = bg_width, bg_height
        self.update_visuals()
        return self

    def set_scale_value(self, scale_value_):
        self*(scale_value_/self.scale_value)
        return self

    def align(self, alignment):
        self.alignment = alignment
        self.calculate_offset()
        self.update_visuals()
        return self

    def calculate_offset(self):
        offset_chart = {
            'topleft': (1, 1),
            'top': (0, 1),
            'topright': (-1, 1),
            'right': (-1, 0),
            'bottomright': (-1, -1),
            'bottom': (0, -1),
            'bottomleft': (1, -1),
            'left': (1, 0),
            'center': (0, 0)
        }
        x_mp, y_mp = offset_chart[self.alignment]
        self.offsetx, self.offsety = self.background_size[0]*x_mp/2, self.background_size[1]*y_mp/2
        return self


    def set_theme(self, theme):
        self.font_name = text_theme[theme]['font']
        self.fontsize = text_theme[theme]['fontsize']
        self.font_colour = text_theme[theme]['font colour']
        self.background_colour = text_theme[theme]['background colour']
        self.background_size = text_theme[theme]['background size']
        self.background_marginal = text_theme[theme]['background marginal']
        self.rounded_colour = text_theme[theme]['rounded colour']
        self.rounded_true_marginal = text_theme[theme]['rounded true marginal']
        self.init_font()
        return self

    def update_visuals(self):
        '''Calculates the necessary information for visualising the object. 
        It is seperate from display_visuals(), 
        the idea being that you do not have to make the calculations for every frame'''
        text_surface = self.font.render(self.text, True, self.font_colour)
        self.text_surface, self.text_rect = text_surface, text_surface.get_rect()
        self.width, self.height = self.text_rect.size
        if not self.background_size:
            self.background_size = self.text_rect.size

        self.center_pos = ( self.posx + self.offsetx, self.posy + self.offsety)
        self.text_rect.center = self.center_pos

        if self.background_marginal:
            true_marginal = self.height*self.background_marginal
            self.background_size = self.width + 2*true_marginal, self.height + 2*true_marginal
            print(5)

        self.background_rect = pg.Rect(self.center_pos, self.background_size)
        self.background_rect.center = self.center_pos

    def display_visuals(self):
        '''displays the pre-calculated visuals on the screen'''
        if self.background_colour: 
            self.display_background()
        if self.rounded_colour:
            self.display_frame()
        self.display.blit(self.text_surface, self.text_rect)

    def display_background(self):
        '''displays rectangular background'''
        pg.draw.rect(self.display, self.background_colour, self.background_rect)

    def display_frame(self):
        '''calculates and displays rounded background, creating "framed" effect'''
        bg_width, bg_height = self.background_size
        rounded_size = bg_width - 2*self.rounded_true_marginal, bg_height - 2*self.rounded_true_marginal
        rounded_rect = pg.Rect(self.center_pos, rounded_size)
        rounded_rect.center = self.center_pos
        pg.draw.rect(self.display, self.rounded_colour, rounded_rect, 0, int(self.rounded_true_marginal))

    def __mul__(self, other):
        '''causes the visuals to scale when the object is multiplied with an integer'''
        self.fontsize*=other
        self.rounded_true_marginal*=other
        
        self.scale_value*=other
        bg_width, bg_height = self.background_size
        self.background_size = bg_width * other, bg_height * other
        self.init_font()
        return self
        
class Button(Text):
    def __init__(self, handler, display_, action_, action_input_, text_ = "button", pos_ = (0, 0), theme_ = "framed"):
        self.text = text_
        self.pos = pos_
        self.posx, self.posy = self.pos
        self.theme = theme_
        self.display = display_
        self.scale_value = 1
        self.offsetx, self.offsety = 0, 0     
        self.alignment = 'center'
        self.set_theme(self.theme)
        self.handler = handler
        handler.objects.append(self)

        '''button specific'''
        handler.buttons.append(self)
        self.action = getattr(ObjectHandler, action_)
        if not self.background_colour:
            self.background_colour = (100, 100, 140)
        self.action_input = action_input_
        self.clicked = False
        self.bio = {action_: 0}


    def mouse_collision(self, point, left_click_status):
        collision = self.background_rect.collidepoint(point)
        if collision:
            self.set_scale_value(1.04)
        else: 
            self.set_scale_value(1)

        if left_click_status and collision:
            self.set_scale_value(0.9)
            if not self.clicked:
                if self.handler.line in ['err','inf','-inf']:
                    self.handler.line = ''
                self.action(self, self.action_input)
                self.clicked = True
        if not left_click_status:
            self.clicked = False