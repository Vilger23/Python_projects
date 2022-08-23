from GUI import GUI
import pygame as pg
from pygame.locals import *

pg.init()
def main():
	gui = GUI()
	while True:
		for event in pg.event.get():
			gui.update(event)
			if event.type == QUIT:
				pg.quit()
				sys.quit()
		pg.display.update()

if __name__ == '__main__':
	main()