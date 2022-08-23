import src.gui_framework
from src.pages import startpage
import src.themes
import pygame as pg

class GUI():
	def __init__(self):
		self.screensize = (300, 500)
		self.screen_width, self.screen_height = self.screensize
		self.screen = pg.display.set_mode(self.screensize)
		pg.display.set_caption('Calculator 2.0')

		self.pages = [startpage.StartPage(self, self.screen)]
		self.set_page(0)

	def update(self, event):

		self.current_page.update(event)

	def set_page(self, index):
		self.current_page = self.pages[index]
