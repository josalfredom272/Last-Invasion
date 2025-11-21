import sys
import pygame
import title
import ending
from settings import WINDOW_WIDTH, WINDOW_HEIGHT
from resources import init_sounds
from game import Game

pygame.init()
pygame.display.set_caption("Last Invasion By: Lu")

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#initializes mixer for audio|original buffer=4096
pygame.mixer.pre_init(44100, 16, 2, 512)

# Initialize sounds
init_sounds()

# create and start the main menu
mainTitle = title.mainScreen()
mainTitle.run()

# if player chooses to play run the game, otherwise, quit pygame
if mainTitle.playGame:
	mainGame = Game(window)
	mainGame.run()
	#system("clear")
	mainGame.game_over()
	print(mainGame.not_game_over)

	ending = ending.mainScreen(mainGame.final_score, mainGame.final_life)
	ending.run()
	while ending.playGame:
		if ending.playGame:
			mainGame.run()
			#system("clear")
			mainGame.game_over()
			ending.score = mainGame.final_score
			ending.player_life = mainGame.final_life
			ending.run()
			#system("clear")

pygame.quit()
sys.exit()
