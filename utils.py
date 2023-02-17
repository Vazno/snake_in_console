import os
import contextlib
import sys
import colorama
import shutil
import io

def cls():
	'''Clear console'''
	os.system('cls' if os.name=='nt' else 'clear')

def has_duplicate_lists(lst):
	for i in range(len(lst)):
		for j in range(i + 1, len(lst)):
			if lst[i] == lst[j]:
				return True
	return False

def replace_console_text(new_text):
	# get the current console text
	console_text = get_console_text()

	# find the position of the old text in the console text
	old_text_pos = console_text.index(console_text)

	# calculate the position of the cursor after the old text
	console_width = shutil.get_terminal_size()[1]
	cursor_pos = old_text_pos + len(console_text)
	cursor_row = cursor_pos // console_width
	cursor_col = cursor_pos % console_width

	# move the cursor to the position after the old text
	print(colorama.Cursor.POS(cursor_row, cursor_col), end='')

	# overwrite the old text with the new text
	print(colorama.Fore.RESET + new_text + colorama.Style.RESET_ALL)

def get_console_text():
	# capture the current console output as a string
	console_text = io.StringIO()
	with contextlib.redirect_stdout(console_text):
		# force a flush to make sure all output is captured
		sys.stdout.flush()
	# get the captured output as a string
	console_text = console_text.getvalue()
	return console_text