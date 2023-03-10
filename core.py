from random import choice
from typing import Tuple
import threading
import time
import colorama
from keyboard import is_pressed
from copy import deepcopy

from utils import has_duplicate_lists, cls, replace_console_text

BINDS = {"up": "w",
		"down": "s",
		"left": "a",
		"right": "d",}


class Piece:
	def __init__(self, name, look, color: colorama.Fore) -> None:
		self.look = look
		self.name = name
		self.color = color

	def __repr__(self) -> str:
		return repr(self.look)

	def __str__(self) -> str:
		return self.look

class Graphic:
	def __init__(self, snake, empty_cell, apple, border) -> None:
		self.snake = Piece("snake", snake, colorama.Fore.GREEN)
		self.empty_cell = Piece("empty_cell", empty_cell, colorama.Fore.RESET)
		self.apple = Piece("apple", apple, colorama.Fore.RED)
		self.border = Piece("border", border, colorama.Fore.LIGHTBLACK_EX)

class Game:
	def __init__(self, size: Tuple[int, int], graphic: Graphic, fps: int = 75, show_score: bool = True) -> None:
		cls()
		self.show_score = show_score
		self.run = True
		self.fps = fps
		self._size = size
		self.graphic = graphic
		self.matrix = list()
		self.__generate_matrix()
		self.apple_spawn_repeat = 5 # Tries to spawn apple every x second
		self.snake_movement_repeat = 0.2 # Snake's speed


		self.snake_moved = False
		# Snakes spawn position
		self.snake_positions = [[-1, 0], [-2, 0], [-3, 0], [-4, 0], [-5, 0]]

		self.snake_direction = "up"
		self.set_snake_direction_limits()

		# Says how many apples were collected, and snake's body should grow to that x number
		self.collected_apples_length = 0

		self.__apples_collected = 0

	@property
	def size(self):
		return self._size
	
	@size.setter
	def size(self, x: Tuple[int, int]):
		self._size = x
		self.__generate_matrix()

	def gameover(self):
		self.run = False

	def set_snake_direction_limits(self):
		if self.snake_direction == "up":
			self.cant_go_up = False
			self.cant_go_down = True
			self.cant_go_left = False
			self.cant_go_right = False
		elif self.snake_direction == "down":
			self.cant_go_up = True
			self.cant_go_down = False
			self.cant_go_left = False
			self.cant_go_right = False
		elif self.snake_direction == "right":
			self.cant_go_up = False
			self.cant_go_down = False
			self.cant_go_left = True
		elif self.snake_direction == "left":
			self.cant_go_up = False
			self.cant_go_down = False
			self.cant_go_left = False
			self.cant_go_right = True

	def move_snake(self):
		self.set_snake_direction_limits()

		# Deleting moved tail of snake
		if len(self.snake_positions) > 1 and self.snake_moved and self.collected_apples_length == 0:
			self.matrix[self.snake_positions[0][0]][self.snake_positions[0][1]] = self.graphic.empty_cell
			del self.snake_positions[0]

		elif self.collected_apples_length != 0:
			self.collected_apples_length -= 1

		if self.snake_direction == "up":
			try:
				self.matrix[self.snake_positions[-1][0]-1][self.snake_positions[-1][1]]
				self.snake_positions.append([self.snake_positions[-1][0]-1, self.snake_positions[-1][1]])
			except IndexError:
				#Moving head to the y[-1] index postion
				self.snake_positions.append([-1, self.snake_positions[-1][1]])

		if self.snake_direction == "down":
			if len(self.matrix)-1 >= self.snake_positions[-1][0]+1:
				self.snake_positions.append([self.snake_positions[-1][0]+1, self.snake_positions[-1][1]])
			else:
				#Moving head to y[0]
				self.snake_positions.append([0, self.snake_positions[-1][1]])

		if self.snake_direction == "right":
			if len(self.matrix[self.snake_positions[-1][0]])-1 >= self.snake_positions[-1][1]+1:
				self.snake_positions.append([self.snake_positions[-1][0], self.snake_positions[-1][1]+1])
			else:
				#Moving head to the x[0] index postion
				self.snake_positions.append([self.snake_positions[-1][0], 0])

		if self.snake_direction == "left":
			try:
				self.matrix[self.snake_positions[-1][0]][self.snake_positions[-1][1]-1]
				self.snake_positions.append([self.snake_positions[-1][0], self.snake_positions[-1][1]-1])
			except IndexError:
				#Moving head to the x[-1] index postion
				self.snake_positions.append([self.snake_positions[-1][0], -1])


		self.snake_moved = True

		# Adding snake to matrix
		for position in self.snake_positions:
			if has_duplicate_lists(self.snake_positions):
				self.gameover()
				return
			if self.matrix[position[0]][position[1]] == self.graphic.apple:
				self.collected_apples_length += 1
				self.__apples_collected += 1
			self.matrix[position[0]][position[1]] = self.graphic.snake

	def __generate_matrix(self):
		'''Generates the board'''
		self.matrix = list()
		for y in range(self.size[1]):
			self.matrix.append(list())
			for x in range(self.size[0]):
				self.matrix[-1].append(self.graphic.empty_cell)

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

	def print_matrix_loop(self):
		while self.run:
			time.sleep(1/self.fps)
			text = "\n"
			new_matrix = deepcopy(self.matrix)
			for row in new_matrix:
				row.insert(0, self.graphic.border)
				row.append(self.graphic.border)
			
			new_matrix.append([self.graphic.border]*(len(self.matrix[0])+2))
			new_matrix.insert(0, [self.graphic.border]*(len(self.matrix[0])+2))
			
			for row in new_matrix:
				text += "".join([str(p) for p in row]) + "\n"

			for piece in vars(self.graphic):
				piece = self.graphic.__getattribute__(piece)
				colored_string = piece.color + piece.look + colorama.Fore.RESET
				text = text.replace(piece.look, colored_string)

			if self.show_score:
				text += "\n"
				text += f"| Score: {self.__apples_collected} | Snake length: {len(self.snake_positions)} |\n"
			self.text = text
			replace_console_text(text)

	def button_loop(self):
		while self.run:
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

	def snake_loop(self):
		while self.run:
			# Snake movement
			time.sleep(self.snake_movement_repeat)
			self.move_snake()

	def apple_loop(self):
		while self.run:
			# Apple generation
			time.sleep(self.apple_spawn_repeat)
			self.generate_apples()

	def start(self):
		t1 = threading.Thread(target=self.snake_loop)
		t1.start()

		t2 = threading.Thread(target=self.button_loop)
		t2.start()

		t3 = threading.Thread(target=self.print_matrix_loop)
		t3.start()

		t4 = threading.Thread(target=self.apple_loop)
		t4.start()

		t1.join()
		t2.join()
		t3.join()
		t4.join()
		print("You lost")



if __name__ == "__main__":
	game = Game((70, 30), Graphic("*", " ", "@", "#"), fps=100)
	game.snake_movement_repeat = 0.25
	game.apple_spawn_repeat = 1
	game.start()