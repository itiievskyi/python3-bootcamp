from os import system

keys = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (3, 5, 7), (1, 5, 9)]
game_on = True

def display_board(board):
	print("")
	for x in [7, 8, 9, 4, 5, 6, 1, 2, 3]:
		if board[x] == 'X':
			print("\033[1;31m", end='')
		elif board[x] == 'O':
			print("\033[1;32m", end='')
		print(f"{board[x]: ^3}", end='')
		print("\033[0;0m", end='')

		if x % 3 == 0:
			print("")
		else:
			print("|", end='')
		if x == 9 or x == 6:
			print("-----------")

	print("")

def check_winner(board):
	p1_list = [k for k, v in board.items() if v == 'X']
	p2_list = [k for k, v in board.items() if v == 'O']
	for (a, b, c) in keys:
		if (a in p1_list) and (b in p1_list) and (c in p1_list):
			return 1
		elif (a in p2_list) and (b in p2_list) and (c in p2_list):
			return 2
	return 0

while game_on:
	board = {1:'₁', 2:'₂', 3:'₃', 4:'₄', 5:'₅', 6:'₆', 7:'₇', 8:'₈', 9:'₉'}
	players = {'p1':'X', 'p2':'O'}
	start_msg = "Please choose 'X' or 'O' for Player 1: "
	turn = 0
	winner = 0

	while True:
		system('clear')
		p1 = input(start_msg).upper()
		if p1 == 'X':
			break
		elif p1 == 'O':
			players['p1'] = 'O'
			players['p2'] = 'X'
			break
		else:
			start_msg = "Please use only 'X' or 'O' while choosing for Player 1: "

	while turn < 9:
		system('clear')
		display_board(board)
		player = turn % 2 + 1
		raw_cell = input(f"Player {player}, please choose the cell (1-9) for for {players['p' + str(player)]}: ")
		if not raw_cell.isdigit():
			continue
		cell = int(raw_cell)
		if cell not in range(1, 10):
			continue
		elif board[cell] == 'X' or board[cell] == 'O':
			continue
		else:
			turn += 1
			board[cell] = players['p' + str(player)]
			winner = check_winner(board)
			if winner > 0:
				break

	while True:

		system('clear')
		display_board(board)
		if winner == 0:
			print("There is no winner :(\n")
		else:
			print(f"Player {winner} wins!\n")

		replay = input("Do you want to replay? (y/n): ").lower()
		if replay == 'y':
			break
		elif replay == 'n':
			game_on = False
			break
