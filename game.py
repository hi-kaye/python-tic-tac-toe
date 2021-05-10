import pygame, sys
import numpy as np

# initializes pygame
pygame.init()

# consts
WIDTH = 600
HEIGHT = 600
LINE_WIDTH = 15
WIN_LINE_WIDTH = 15
BOARD_ROWS = 3
BOARD_COLS = 3
SQUARE_SIZE = 200
CIRCLE_RADIUS = 60
CIRCLE_WIDTH = 15
CROSS_WIDTH = 25
SPACE = 55

#colours
BG_COLOUR = (0, 128, 255)
LINE_COLOUR = (23, 102, 204)
CIRCLE_COLOUR = (153, 204, 255)
CROSS_COLOUR = (204, 229, 255)
WHITE = (255,255,255)

# screen board
screen = pygame.display.set_mode( (WIDTH, HEIGHT) )
pygame.display.set_caption( 'TIC TAC TOE' )
screen.fill( BG_COLOUR )


# console board
board = np.zeros( (BOARD_ROWS, BOARD_COLS) )


def draw_lines():
	# 1st horizontal
	pygame.draw.line( screen, LINE_COLOUR, (0, SQUARE_SIZE), (WIDTH, SQUARE_SIZE), LINE_WIDTH )
	# 2nd horizontal
	pygame.draw.line( screen, LINE_COLOUR, (0, 2 * SQUARE_SIZE), (WIDTH, 2 * SQUARE_SIZE), LINE_WIDTH )
	# 1st vertical
	pygame.draw.line( screen, LINE_COLOUR, (SQUARE_SIZE, 0), (SQUARE_SIZE, HEIGHT), LINE_WIDTH )
	# 2nd vertical
	pygame.draw.line( screen, LINE_COLOUR, (2 * SQUARE_SIZE, 0), (2 * SQUARE_SIZE, HEIGHT), LINE_WIDTH )

def draw_figures():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 1:
				pygame.draw.circle( screen, CIRCLE_COLOUR, (int( col * SQUARE_SIZE + SQUARE_SIZE//2 ), int( row * SQUARE_SIZE + SQUARE_SIZE//2 )), CIRCLE_RADIUS, CIRCLE_WIDTH )
			elif board[row][col] == 2:
				pygame.draw.line( screen, CROSS_COLOUR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SPACE), CROSS_WIDTH )	
				pygame.draw.line( screen, CROSS_COLOUR, (col * SQUARE_SIZE + SPACE, row * SQUARE_SIZE + SPACE), (col * SQUARE_SIZE + SQUARE_SIZE - SPACE, row * SQUARE_SIZE + SQUARE_SIZE - SPACE), CROSS_WIDTH )

def mark_square(row, col, player):
	board[row][col] = player

def available_square(row, col):
	return board[row][col] == 0

def check_board():
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			if board[row][col] == 0:
				return False
	return True

def check_win(player):
	# vertical win check
	for col in range(BOARD_COLS):
		if board[0][col] == player and board[1][col] == player and board[2][col] == player:
			draw_vertical(col, player)
			return True

	# horizontal win check
	for row in range(BOARD_ROWS):
		if board[row][0] == player and board[row][1] == player and board[row][2] == player:
			draw_horizontal(row, player)
			return True

	# asc diagonal win check
	if board[2][0] == player and board[1][1] == player and board[0][2] == player:
		draw_asc_diagonal(player)
		return True

	# desc diagonal win check
	if board[0][0] == player and board[1][1] == player and board[2][2] == player:
		draw_desc_diagonal(player)
		return True

	return False

# winning lines
def draw_vertical(col, player):
	posX = col * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		colour = CIRCLE_COLOUR
	elif player == 2:
		colour = CROSS_COLOUR

	pygame.draw.line( screen, colour, (posX, 15), (posX, HEIGHT - 15), LINE_WIDTH )

def draw_horizontal(row, player):
	posY = row * SQUARE_SIZE + SQUARE_SIZE//2

	if player == 1:
		colour = CIRCLE_COLOUR
	elif player == 2:
		colour = CROSS_COLOUR

	pygame.draw.line( screen, colour, (15, posY), (WIDTH - 15, posY), WIN_LINE_WIDTH )

def draw_asc_diagonal(player):
	if player == 1:
		colour = CIRCLE_COLOUR
	elif player == 2:
		colour = CROSS_COLOUR

	pygame.draw.line( screen, colour, (15, HEIGHT - 15), (WIDTH - 15, 15), WIN_LINE_WIDTH )

def draw_desc_diagonal(player):
	if player == 1:
		colour = CIRCLE_COLOUR
	elif player == 2:
		colour = CROSS_COLOUR

	pygame.draw.line( screen, colour, (15, 15), (WIDTH - 15, HEIGHT - 15), WIN_LINE_WIDTH )

def restart():
	screen.fill( BG_COLOUR )
	draw_lines()
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			board[row][col] = 0

def game_end(player):
	screen.fill((153,204,255))
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			board[row][col] = 0
	font = pygame.font.Font('freesansbold.ttf', 32)
	if player == 1:
		text = font.render('Player 1 wins! Press r to restart game!', True, WHITE)
	elif player == 2:
		text = font.render('Player 2 wins! Press r to restart game!', True, WHITE)
	textRect = text.get_rect()
	textRect.center = (WIDTH // 2, HEIGHT // 2)
	screen.blit(text, textRect)

def game_draw():
	screen.fill((153,204,255))
	for row in range(BOARD_ROWS):
		for col in range(BOARD_COLS):
			board[row][col] = 0
	font = pygame.font.Font('freesansbold.ttf', 32)
	text = font.render('It\'s a draw! Press r to restart game!', True, WHITE)
	textRect = text.get_rect()
	textRect.center = (WIDTH // 2, HEIGHT // 2)
	screen.blit(text, textRect)

draw_lines()

#variables
player = 1
game_over = False

#main loop
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			sys.exit()

		if event.type == pygame.MOUSEBUTTONDOWN and not game_over:

			mouseX = event.pos[0] # x
			mouseY = event.pos[1] # y

			clicked_row = int(mouseY // SQUARE_SIZE)
			clicked_col = int(mouseX // SQUARE_SIZE)

			if available_square(clicked_row, clicked_col):
				mark_square(clicked_row, clicked_col, player)

				if check_win(player):
					game_over = True
					game_end(player)

				if check_board() and check_win(player) is False:
					game_draw()
			
				player = player % 2 + 1
				draw_figures()
			
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_r:
				restart()
				player = 1
				game_over = False

	pygame.display.update()