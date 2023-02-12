from random import choice
from typing import Tuple
import time
from keyboard import is_pressed
import sys
from copy import deepcopy

from utils import has_duplicate_lists, cls

BINDS = {"quit": "q",
"up": "w",
"down": "s",
"left": "a",
"right": "d",
"restart": "r"}


class Piece:
	def __init__(self, name, look) -> None:
		self.look = look
		self.name = name

	def __repr__(self) -> str:
		return repr(self.look)

	def __str__(self) -> str:
		return self.look

class Graphic:
	def __init__(self, snake, empty_cell, apple) -> None:
		self.snake = Piece("snake", snake)
		self.empty_cell = Piece("empty_cell", empty_cell)
		self.apple = Piece("apple", apple)

class Game:
	def __init__(self, size: Tuple[int, int], graphic: Graphic) -> None:
		cls()
		self.run = True
		self._size = size
		self.graphic = graphic
		self.matrix = list()
		self.__generate_matrix()
		self.apple_spawn_repeat = 5 # Tries to spawn apple every x second
		self.snake_movement_repeat = 0.2


		self.snake_moved = False
		self.snake_positions = list()
		self.snake_positions.append([-1,0])
		self.snake_positions.append([-2,0])
		self.snake_positions.append([-3,0])
		self.snake_positions.append([-4,0])
		self.snake_positions.append([-5,0])

		self.snake_direction = "up"

		self.cant_go_up = False
		self.cant_go_down = True
		self.cant_go_left = False
		self.cant_go_right = False

		self.collected_apples_length = 0

	def gameover(self):
		self.run = False


	def move_snake(self):
		# Deleting moved tail of snake
		if len(self.snake_positions) > 1 and self.snake_moved and self.collected_apples_length == 0:
			self.matrix[self.snake_positions[0][0]][self.snake_positions[0][1]] = self.graphic.empty_cell
			del self.snake_positions[0]

		elif self.collected_apples_length != 0:
			self.collected_apples_length -= 1

		if self.snake_direction == "up":
			self.cant_go_up = False
			self.cant_go_down = True
			self.cant_go_left = False
			self.cant_go_right = False
			try:
				self.matrix[self.snake_positions[-1][0]-1][self.snake_positions[-1][1]]
				self.snake_positions.append([self.snake_positions[-1][0]-1, self.snake_positions[-1][1]])
			except IndexError:
				#Moving head to the y[-1] index postion
				self.snake_positions.append([-1, self.snake_positions[-1][1]])

		if self.snake_direction == "down":
			self.cant_go_up = True
			self.cant_go_down = False
			self.cant_go_left = False
			self.cant_go_right = False
			if len(self.matrix)-1 >= self.snake_positions[-1][0]+1:
				self.snake_positions.append([self.snake_positions[-1][0]+1, self.snake_positions[-1][1]])
			else:
				#Moving head to y[0]
				self.snake_positions.append([0, self.snake_positions[-1][1]])

		if self.snake_direction == "right":
			self.cant_go_up = False
			self.cant_go_down = False
			self.cant_go_left = True
			self.cant_go_right = False
			if len(self.matrix[self.snake_positions[-1][0]])-1 >= self.snake_positions[-1][1]+1:
				self.snake_positions.append([self.snake_positions[-1][0], self.snake_positions[-1][1]+1])
			else:
				#Moving head to the x[0] index postion
				self.snake_positions.append([self.snake_positions[-1][0], 0])

		if self.snake_direction == "left":
			self.cant_go_up = False
			self.cant_go_down = False
			self.cant_go_left = False
			self.cant_go_right = True
			try:
				self.matrix[self.snake_positions[-1][0]][self.snake_positions[-1][1]-1]
				self.snake_positions.append([self.snake_positions[-1][0], self.snake_positions[-1][1]-1])
			except IndexError:
				#Moving head to the x[-1] index postion
				self.snake_positions.append([self.snake_positions[-1][0], -1])


		self.snake_moved = True

		# Drawing snake
		for position in self.snake_positions:
			if has_duplicate_lists(self.snake_positions):
				self.gameover()
				return
			if self.matrix[position[0]][position[1]] == self.graphic.apple:
				self.collected_apples_length += 1
			self.matrix[position[0]][position[1]] = self.graphic.snake



	@property
	def size(self):
		return self._size
	
	@size.setter
	def size(self, x: Tuple[int, int]):
		self._size = x
		self.__generate_matrix()

	def __generate_matrix(self):
		'''Generates the board'''
		self.matrix = list()
		for y in range(self.size[1]):
			self.matrix.append(list())
			for x in range(self.size[0]):
				self.matrix[-1].append(self.graphic.empty_cell)
	
	def refresh_matrix(self):
		'''Use it every time when you are editing looks of pieces'''
		for row in self.matrix:
			for piece in row:
				# Replacing Piece with the new Piece that has different attribute look
				piece = self.graphic.__getattribute__(piece.name)

	def generate_apples(self):
		'''Randomly generates one apple on the empty_cell'''
		empty_cells = list()
		y = 0
		for row in self.matrix:
			x = 0
			for p in row:
				if p.name == "empty_cell":
					empty_cells.append((y, x))
				x += 1
			y += 1
		
		if empty_cells != list():
			# If there is an empty_cell piece left, it places apple there
			y, x = choice(empty_cells)
			self.matrix[y][x] = self.graphic.apple

	def create_matrix_string(self) -> str:
		text = "\n"
		for row in self.matrix:
			text += "".join([str(p) for p in row]) + "\n"
		return text

	def print_matrix(self):
		cls()
		text = "\n"
		for row in self.matrix:
			text += "".join([str(p) for p in row]) + "\n"
		print(text)

	def change_direction(self):
		if is_pressed(BINDS['up']):
			if not self.cant_go_up:
				self.snake_direction = "up"

		if is_pressed(BINDS['down']):
			if not self.cant_go_down:
				self.snake_direction = "down"

		if is_pressed(BINDS['left']):
			if not self.cant_go_left:
				self.snake_direction = "left"

		if is_pressed(BINDS['right']):
			if not self.cant_go_right:
				self.snake_direction = "right"

	def mainloop(self, tick: int = 0.01):
		self.default_settings = deepcopy([self.graphic,
							self.snake_direction, self.snake_positions,
							self.size, self.collected_apples_length])
		apple_timer = 0
		snake_movement_timer = 0
		self.run = True
		while self.run == True:
			self.print_matrix()
			time.sleep(tick)


			# Apple generation
			apple_timer += tick
			if apple_timer >= self.apple_spawn_repeat:
				apple_timer = 0
				self.generate_apples()
			
			snake_movement_timer += tick
			# Snake movement
			if snake_movement_timer >= self.snake_movement_repeat:
				snake_movement_timer = 0
				self.move_snake()

			self.change_direction()

			if is_pressed(BINDS['quit']):
				print('You left the game!')
				sys.exit()
			elif is_pressed(BINDS['restart']):
				self.graphic = self.default_settings[0]
				self.snake_direction = self.default_settings[1]
				self.snake_positions =  self.default_settings[2]
				self.size = self.default_settings[3]
				self.collected_apples_length = self.default_settings[4]
				self.mainloop(tick)
		print("You lost")

if __name__ == "__main__":
	game = Game((70, 30), Graphic("*", "x", "@"))

	game.print_matrix()
	game.mainloop()