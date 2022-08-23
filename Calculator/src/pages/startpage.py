import sys
sys.path.append('C:/Users/vilme/OneDrive/Desktop/PythonProjects/Calculator/src')
from objecthandler import ObjectHandler
from gui_framework import *
import pygame as pg



class StartPage():
    def __init__(self, GUI,screen):
        self.GUI = GUI
        self.screen = screen
        self.handler = ObjectHandler(GUI)
        self.left_click_status = False
        self.padding = 12
        sz_x = (self.GUI.screen_width-5*self.padding)/4
        sz_y = sz_x

        digi_font = pg.font.Font("C:/Users/vilme/OneDrive/Desktop/PythonProjects/Calculator/src/digital-7.ttf", 50)

        for ix in range(3):
            for iy in range(3):

                Button(self.handler, self.screen, 'write', str(ix+1 + iy*3), str(ix + 1 + iy*3)).set_background_size(sz_x, sz_y).set_pos( (  ix*(self.padding+sz_x) + self.padding, ((2-iy)*(self.padding+sz_y) + 80 + 3*self.padding) )).align('topleft')


        Button(self.handler, self.screen, 'write', '/', '/').set_pos( (3*(self.padding+sz_x) + self.padding, 80 + 3*self.padding) ).set_background_size(sz_x, sz_y).align('topleft')
        Button(self.handler, self.screen, 'write', '*', '*').set_pos( (3*(self.padding+sz_x) + self.padding, self.padding+sz_y + 80 + 3*self.padding) ).set_background_size(sz_x, sz_y).align('topleft')
        Button(self.handler, self.screen, 'write', '-' , '-').set_pos( (3*(self.padding+sz_x) + self.padding, 2*(self.padding+sz_y) + 80 + 3*self.padding) ).set_background_size(sz_x, sz_y).align('topleft')
        Button(self.handler, self.screen, 'write', '+' , '+').set_pos( (3*(self.padding+sz_x) + self.padding, 3*(self.padding+sz_y) + 80 + 3*self.padding) ).set_background_size(sz_x, sz_y*2+self.padding).align('topleft')
        Button(self.handler, self.screen, 'eval', '=' , '=').set_pos( (2*(self.padding+sz_x) + self.padding, 4*(self.padding+sz_y) + 80 + 3*self.padding) ).set_background_size(sz_x, sz_y).align('topleft')
        Button(self.handler, self.screen, 'erase', '1' , 'CE').set_pos( (0*(self.padding+sz_x) + self.padding, 4*(self.padding+sz_y) + 80 + 3*self.padding) ).set_background_size(sz_x, sz_y).align('topleft')
        Button(self.handler, self.screen, 'erase', 'all' , 'C').set_pos( (0*(self.padding+sz_x) + self.padding, 3*(self.padding+sz_y) + 80 + 3*self.padding) ).set_background_size(sz_x, sz_y).align('topleft')
        Button(self.handler, self.screen, 'write', '0' , '0').set_pos( (1*(self.padding+sz_x) + self.padding, 3*(self.padding+sz_y) + 80 + 3*self.padding) ).set_background_size(sz_x, sz_y).align('topleft')
        Button(self.handler, self.screen, 'write', '.' , '.').set_pos( (2*(self.padding+sz_x) + self.padding, 3*(self.padding+sz_y) + 80 + 3*self.padding) ).set_background_size(sz_x, sz_y).align('topleft')
     
        self.white_sq = Text(self.handler, self.screen, text_ = '',theme_ = 'standard').set_pos( (self.GUI.screen_width/2, self.padding) )
        self.white_sq.set_background_colour((250, 230, 230)).set_background_size(self.GUI.screen_width-2*self.padding, 80).align('top')
        self.text = Text(self.handler, self.screen, text_ = '1234',theme_ = 'standard').set_pos( (self.GUI.screen_width-2*self.padding, self.padding+40) )
        self.text.set_fontsize(40).set_background_marginal(0.1).set_background_colour((250, 230, 230)).align('right')
        self.text.font = digi_font
        
    
    def update(self, event):
        self.screen.fill( (100, 100 ,200) )
        mouse_pos = pg.mouse.get_pos()

        if event.type == pg.MOUSEBUTTONDOWN:
            self.left_click_status = True
        if event.type == pg.MOUSEBUTTONUP:
            self.left_click_status = False


        self.handler.update(mouse_pos, self.left_click_status)
        self.text.set_text(self.handler.line[max(len(self.handler.line)-10, 0):])
        self.text.calculate_offset().update_visuals()

        self.handler.display_objects()
