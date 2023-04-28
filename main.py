"""
Code from: x4nth055/pythoncode-tutorials Github
"""
import pygame

from board import Board
from gui import GUI


pygame.init()

gui_size = 125
WINDOW_SIZE = (600, 600+gui_size)
screen = pygame.display.set_mode(WINDOW_SIZE)

board = Board(WINDOW_SIZE[0], WINDOW_SIZE[1]-gui_size)
gui = GUI()

def draw(display):
	display.fill((190, 190, 190))
	board.draw(display)
	gui.draw(display)
	pygame.display.update()


if __name__ == '__main__':
	clock = pygame.time.Clock()
	running = True

	while running:
		mx, my = pygame.mouse.get_pos()
		for event in pygame.event.get():

			# Quit the game if the user presses the close button
			if event.type == pygame.QUIT:
				running = False
			elif event.type == pygame.MOUSEBUTTONDOWN: 
       			
				# If the mouse is clicked
				if event.button == 1 and my < WINDOW_SIZE[0] and mx < WINDOW_SIZE[1] - gui_size:
					board.handle_click(mx, my)

				gui.handle_mouse(mx, my, is_click=True, board=board)
			elif event.type == pygame.MOUSEMOTION:
				gui.handle_mouse(mx, my, is_click=False)
		
		if board.is_in_checkmate('black'): # If black is in checkmate
			print('White wins!')
			# running = False

		elif board.is_in_checkmate('white'): # If white is in checkmate
			print('Black wins!')
			# running = False
		
		# Draw the board
		clock.tick(24)
		draw(screen)
		