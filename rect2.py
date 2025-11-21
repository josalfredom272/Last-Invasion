import pygame
import math


YELLOW = (255,255,0)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)


class Rect(object):
	def __init__(self, x, y, w, h, color):
		self.active = False
		self.life = 10
		self.initialX = x
		self.initialY = y
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.size = [self.w, self.h]
		self.angleX = 0.00
		self.angleY = 0.00
		self.angleXSpeed = 0.08
		self.angleYSpeed = 0.08
		self.distance = 100
		self.surface = pygame.Surface(self.size)
		self.surface.fill(color)

	def draw(self, window):
		if self.active:
			window.blit(self.surface, (self.x, self.y))

	def drawCircle(self, window):
		if self.active:
			pygame.draw.circle(window, YELLOW, (int(self.x), int(self.y)), self.w)

	def update(self, x, y):
		self.initialX = x
		self.initialY = y
		if self.life < 1:
			self.deactivate()

	def spin(self):
		self.angleX += self.angleXSpeed
		self.angleX %= math.tau
		self.angleY += self.angleYSpeed
		self.angleY %= math.tau
		self.x = self.initialX + math.cos(self.angleX) * self.distance
		self.y = self.initialY + math.sin(self.angleY) * self.distance

	def collidesWith(self, othe_body):
		if self.x + self.w < othe_body.x or self.x > othe_body.x + othe_body.w:
			return False
		elif self.y + self.h < othe_body.y or self.y > othe_body.y + othe_body.h:
			return False
		else:
			return True

	def setDistance(self, d):
		self.distance = d

	def setAngleSpeed(self, x, y):
		self.angleXSpeed = x
		self.angleYSpeed = y

	def setAngles(self, x, y):
		self.angleX = x
		self.angleY = y

	def activate(self):
		self.active = True

	def deactivate(self):
		self.active = False
		self.life = 25
