import json

import pygame

from square import Square
from pieces.rook import Rook
from pieces.bishop import Bishop
from pieces.knight import Knight
from pieces.queen import Queen
from pieces.king import King
from pieces.pawn import Pawn


# Game state checker
class Board:
	BASE_BOARD_PATH = "base_board.json"

	def __init__(self, width, height, path=BASE_BOARD_PATH):
		self.init(width, height, path)

	def load(self):
		pass

	def save(self):
		with open("saved_board.json", "w+") as file:
			json.dump({
				"board": self.config,
				"moves": self.moves,
				"turn": self.turn
			}, file)

	def restart(self):
		self.init(self.width, self.height)
	
	def init(self, width, height, path=BASE_BOARD_PATH):
		self.width = width
		self.height = height
		self.tile_width = width // 8
		self.tile_height = height // 8
		self.selected_piece = None

		with open(path, "r") as file:
			data = json.load(file)
			self.config = data["board"]
			self.turn = data["turn"]
			self.moves = data["moves"]

		self.squares = self.generate_squares()
		self.setup_board()


	def generate_squares(self):
		output = []
		for y in range(8):
			for x in range(8):
				output.append(
					Square(x,  y, self.tile_width, self.tile_height)
				)
		return output


	def get_square_from_pos(self, pos):
		for square in self.squares:
			if (square.x, square.y) == (pos[0], pos[1]):
				return square


	def get_piece_from_pos(self, pos):
		return self.get_square_from_pos(pos).occupying_piece


	def setup_board(self):
		# iterating 2d list
		for y, row in enumerate(self.config):
			for x, piece in enumerate(row):
				if piece != '':
					square = self.get_square_from_pos((x, y))

					# looking inside contents, what piece does it have
					if piece[1] == 'R':
						square.occupying_piece = Rook(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)
					# as you notice above, we put `self` as argument, or means our class Board

					elif piece[1] == 'N':
						square.occupying_piece = Knight(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)

					elif piece[1] == 'B':
						square.occupying_piece = Bishop(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)

					elif piece[1] == 'Q':
						square.occupying_piece = Queen(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)

					elif piece[1] == 'K':
						square.occupying_piece = King(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)

					elif piece[1] == 'P':
						square.occupying_piece = Pawn(
							(x, y), 'white' if piece[0] == 'w' else 'black', self
						)


	def handle_click(self, mx, my):
		x = mx // self.tile_width
		y = my // self.tile_height
		clicked_square = self.get_square_from_pos((x, y))

		if self.selected_piece is None:
			if clicked_square.occupying_piece is not None:
				if clicked_square.occupying_piece.color == self.turn:
					self.selected_piece = clicked_square.occupying_piece

		elif self.selected_piece.move(self, clicked_square):
			self.turn = 'white' if self.turn == 'black' else 'black'

		elif clicked_square.occupying_piece is not None:
			if clicked_square.occupying_piece.color == self.turn:
				self.selected_piece = clicked_square.occupying_piece


	def is_in_check(self, color, board_change=None): # board_change = [(x1, y1), (x2, y2)]
		output = False
		king_pos = None

		changing_piece = None
		old_square = None
		new_square = None
		new_square_old_piece = None

		if board_change is not None:
			for square in self.squares:
				if square.pos == board_change[0]:
					changing_piece = square.occupying_piece
					old_square = square
					old_square.occupying_piece = None
			for square in self.squares:
				if square.pos == board_change[1]:
					new_square = square
					new_square_old_piece = new_square.occupying_piece
					new_square.occupying_piece = changing_piece

		pieces = [
			i.occupying_piece for i in self.squares if i.occupying_piece is not None
		]

		if changing_piece is not None:
			if changing_piece.notation == 'K':
				king_pos = new_square.pos
		if king_pos == None:
			for piece in pieces:
				if piece.notation == 'K' and piece.color == color:
						king_pos = piece.pos
						break
		for piece in pieces:
			if piece.color != color:
				for square in piece.attacking_squares(self):
					if square.pos == king_pos:
						output = True

		if board_change is not None:
			old_square.occupying_piece = changing_piece
			new_square.occupying_piece = new_square_old_piece
						
		return output


	def who_is_checking(self, king_pos, color):
		pieces = [
			i.occupying_piece for i in self.squares if i.occupying_piece is not None
		]
		checking_piece = []

		for piece in pieces:
			if piece.color == color:
				continue
			for square in piece.attacking_squares(self):
				if square.pos == king_pos:
					checking_piece.append(piece)

		return checking_piece


	def is_in_checkmate(self, color):
		output = False
		king = None

		for piece in [i.occupying_piece for i in self.squares]:
			if piece == None:
				continue
			if piece.notation == 'K' and piece.color == color:
				king = piece
				break

		if len(king.get_valid_moves(self)) == 0:
			# get checking piece, and check if it can be taken
			# do not checkmate if there is one from the above
			# checkmate if there is more than one from the above
			checking_pieces = self.who_is_checking(king.pos, color)
			can_be_blocked = [False for c in checking_pieces]
			pieces = [
				i.occupying_piece for i in self.squares if i.occupying_piece is not None
			]
			
			# Check if they can be blocked
			for i, checking_piece in enumerate(checking_pieces):
				for piece in pieces:
					if piece.color != color:
						continue
					defend_moves = piece.get_valid_moves(self)
					attack_moves = checking_piece.attacking_squares(self)

					for defend_move in defend_moves:
						if defend_move in attack_moves:
							can_be_blocked[i] = True
							break
					
					if can_be_blocked[i]:
						break

				if can_be_blocked[i]:
					continue

			if self.is_in_check(color) and can_be_blocked.count(False) > 0:
				output = True

		return output


	def draw(self, display):
		if self.selected_piece is not None:
			self.get_square_from_pos(self.selected_piece.pos).highlight = True
			for square in self.selected_piece.get_valid_moves(self):
				square.highlight = True

		for square in self.squares:
			square.draw(display)