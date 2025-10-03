import pygame
import random
import sys
from time import sleep

pygame.init()
pygame.mixer.pre_init(44100, 16, 2, 512)

YELLOW = (255,255,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)
BLUE = (0,120,255)
WINDOW_WIDTH = 1080
WINDOW_HEIGHT = 720

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

select = pygame.mixer.Sound("sound/select.ogg")
confirm = pygame.mixer.Sound("sound/confirm.ogg")
# main theme
def playMusic():
	pygame.mixer.music.load("sound/magic space.mp3")
	pygame.mixer.music.play(-1)

class rect:
	def __init__(self, x, y, w, h, color):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.size = [w, h]

		self.sound = False
		self.played = False

		self.sprite = None
		self.surface = pygame.Surface(self.size)
		self.surface.fill(color)

	def draw(self, window):
		window.blit(self.surface, (self.x , self.y))

	def drawSprite(self, window):
		window.blit(self.sprte, (self.x, self.y))

	def loadSprite(self, file):
		texture = pygame.image.load(file)
		self.sprte = pygame.transform.scale(texture, self.size)

	def changeColor(self, color):
		self.surface = pygame.Surface(self.size)
		self.surface.fill(color)

	def colidesWith(self, othe_body):
		if self.x + self.w < othe_body.x or self.x > othe_body.x + othe_body.w:
			return False
		elif self.y + self.h < othe_body.y or self.y > othe_body.y + othe_body.h:
			return False
		else:
			return True

class mainScreen:
	def __init__(self, score, player):
		self.playGame = False
		self.score = score
		self.player_life = player

	def run(self):
		background = rect(0,0,WINDOW_WIDTH, WINDOW_HEIGHT, WHITE)
		background.loadSprite("asets/Background-1.png")

		title_background = rect(296, 30, 500,400, BLUE)
		title_background.loadSprite("asets/titlebg.png")

		play = rect(414, 295, 220, 40, BLUE)
		exit = rect(450, 415, 140, 40, BLUE)

		cursor = rect(0,0, 40, 40, WHITE)
		cursor.loadSprite("asets/cursor.png")

		sprite = rect(WINDOW_WIDTH // 2 - 150, 400, 300, 300, WHITE)
		sprite.loadSprite("asets/ship.png")

		credits = rect(0,WINDOW_HEIGHT,WINDOW_WIDTH, 3543, WHITE)
		credits.loadSprite("asets/creditsAlpha.png")


		clicked = False
		pygame.mouse.set_visible(False)

		slow_stars = []
		slow_stars_amount = 300
		for i in range(slow_stars_amount):
			star = rect(12 * i, random.randint(0, WINDOW_HEIGHT - 2), 1, 1, WHITE)
			slow_stars.append(star)

		playMusic()
		running = True
		while running:
			for event in pygame.event.get():
				# closing the window with [x]
				if event.type == pygame.QUIT:
					quit()

				elif event.type == pygame.MOUSEBUTTONDOWN:
					clicked = True
				elif event.type == pygame.MOUSEBUTTONUP:
					clicked = False

			if play.colidesWith(cursor):
				play.changeColor(GREEN)
				play.sound = True
				if clicked:
					pygame.mixer.Sound.play(confirm)
					self.playGame = True
					pygame.mixer.music.stop()
					running = False

			else:
				play.changeColor(BLUE)
				play.sound = False
				play.played = False

			if exit.colidesWith(cursor):
				exit.changeColor(GREEN)
				exit.sound = True
				if clicked:
					pygame.mixer.Sound.play(confirm)
					sleep(1)
					running = False
					self.playGame = False

			else:
				exit.changeColor(BLUE)
				exit.sound = False
				exit.played = False

			if play.sound and not play.played:
				pygame.mixer.Sound.play(select)
				play.played = True
				play.sound = False

			if exit.sound and not exit.played:
				pygame.mixer.Sound.play(select)
				exit.played = True
				exit.sound = False

			mp = pygame.mouse.get_pos()


			title  = pygame.font.Font("font/Arcade.ttf", 50)
			title = title.render("Last Invasion ", True, (0,255,0))

			playFont = pygame.font.Font("font/4B.ttf", 25)
			playFont = playFont.render("Play Again", True, (255,255,255))

			exitFont = pygame.font.Font("font/4B.ttf", 25)
			exitFont = exitFont.render("Exit", True, (255,255,255))

			finalScore = pygame.font.Font("font/4B.ttf", 25)
			finalScore = finalScore.render("Your Score Was: " + str(self.score), True, (0,255,0))

			gameOver = pygame.font.Font("font/4B.ttf", 100)
			gameOver = gameOver.render("Game Over", True, (255,0,0))

			youWin = pygame.font.Font("font/4B.ttf", 100)
			youWin = youWin.render("You Win!", True, (0,255,0))

			window.fill(0)

			credits.drawSprite(window)
			credits.y -= 1

			if credits.y < -3487:
				credits.y = WINDOW_HEIGHT


			for i in range(slow_stars_amount):
				slow_stars[i].x -= 2
				if slow_stars[i].x < -6:
					slow_stars[i].x = WINDOW_WIDTH + 6
				slow_stars[i].draw(window)

			# BUTTONS
			play.draw(window)
			exit.draw(window)


			# FONT
			window.blit(playFont, (422, 295))
			window.blit(exitFont, (486, 420))
			window.blit(finalScore,(350, 560))

			if self.player_life < 1:
				window.blit(gameOver, (160, 80))
			elif self.player_life > 0:
				window.blit(youWin, (200, 80))


			#sprite.drawSprite(window)

			# moving and drawing the cursor
			cursor.x = mp[0] - cursor.w // 2
			cursor.y = mp[1] - cursor.h // 2
			cursor.drawSprite(window)

			pygame.display.update()
			sleep(10 / 1000)
