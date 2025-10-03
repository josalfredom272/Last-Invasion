import pygame
import random
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
	pygame.mixer.music.load("sound/MyVeryOwnDeadShip.ogg")
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
	def __init__(self):
		self.playGame = False

	def run(self):
		background = rect(0,0,WINDOW_WIDTH, WINDOW_HEIGHT, WHITE)
		background.loadSprite("asets/Background-1.png")

		title_background = rect(296, 30, 500,400, BLUE)
		title_background.loadSprite("asets/titlebg.png")

		play = rect(345, 195, 140, 40, BLUE)
		exit = rect(580,195,140, 40, BLUE)

		cursor = rect(0,0, 40, 40, WHITE)
		cursor.loadSprite("asets/cursor.png")

		sprite = rect(WINDOW_WIDTH // 2 - 150, 360, 300, 300, WHITE)
		sprite.loadSprite("asets/ship.png")


		clicked = False
		pygame.mouse.set_visible(False)

		playMusic()
		running = True
		while running:
			for event in pygame.event.get():
				# closing the window with [x]
				if event.type == pygame.QUIT:
					running = False

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
			playFont = playFont.render("Play", True, (255,255,255))

			exitFont = pygame.font.Font("font/4B.ttf", 25)
			exitFont = exitFont.render("Exit", True, (255,255,255))

			author = pygame.font.Font("font/Arcade.ttf", 80)
			author = author.render("Game created by Lu", True, (0,255,0))

			window.fill(0)
			# main background
			background.drawSprite(window)

			# UI AND TITLE
			title_background.drawSprite(window)
			window.blit(title, (400, 120))
			play.draw(window)
			exit.draw(window)
			window.blit(playFont, (370, 200))
			window.blit(exitFont, (610, 200))
			window.blit(author, (0, WINDOW_HEIGHT - 80))


			sprite.drawSprite(window)

			# moving and drawing the cursor
			cursor.x = mp[0] - cursor.w // 2
			cursor.y = mp[1] - cursor.h // 2
			cursor.drawSprite(window)

			pygame.display.update()
			sleep(10 / 1000)
