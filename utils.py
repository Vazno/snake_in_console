import os

def cls():
	'''Clear console'''
	os.system('cls' if os.name=='nt' else 'clear')

def has_duplicate_lists(lst):
	for i in range(len(lst)):
		for j in range(i + 1, len(lst)):
			if lst[i] == lst[j]:
				return True
	return False
