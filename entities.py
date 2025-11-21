import pygame
import random
from time import sleep
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, YELLOW, GREEN, RED

sounds = {}

def init_sounds():
	sounds['laser7'] = pygame.mixer.Sound("sound/laser7.wav")
	sounds['laser8'] = pygame.mixer.Sound("sound/laser8.wav")
	sounds['mini_boss_laser'] = pygame.mixer.Sound("sound/sfx_toggle.ogg")
	sounds['death'] = pygame.mixer.Sound("sound/grenade.ogg")
	sounds['explode'] = pygame.mixer.Sound("sound/sfx_explosionGoo.ogg")
	sounds['alert'] = pygame.mixer.Sound("sound/alarm.ogg")
	sounds['hit'] = pygame.mixer.Sound("sound/sfx_shocked.ogg")
	sounds['damage'] = pygame.mixer.Sound("sound/qubodupPunch01.ogg")
	sounds['health'] = pygame.mixer.Sound("sound/sfx_health.ogg")
	sounds['highScore'] = pygame.mixer.Sound("sound/Rise05.ogg")


# basic rect class, can be used to create color rectangles, or store sprites, with simple movement
class rect:
	def __init__(self, x, y, w, h, color):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.size = [w, h]
		self.angle = 0

		self.alpha = 0

		self.sprite = None
		self.surface = pygame.Surface(self.size)
		self.surface.fill(color)

		self.black_screen = pygame.Surface(self. size, flags=pygame.SRCALPHA)

		self.texture_surface = None


	def draw(self, window):
		window.blit(self.surface, (self.x , self.y))

	def drawSprite(self, window):
		window.blit(self.sprite, (self.x, self.y))

	def loadSprite(self, file):
		texture = pygame.image.load(file)
		self.texture_surface = pygame.image.load(file)
		self.sprite = pygame.transform.scale(texture, self.size)

	def changeColor(self, color):
		self.surface = pygame.Surface(self.size)
		self.surface.fill(color)

	def collidesWith(self, other_body):
		if self.x + self.w < other_body.x or self.x > other_body.x + other_body.w:
			return False
		elif self.y + self.h < other_body.y or self.y > other_body.y + other_body.h:
			return False
		else:
			return True

	def drawBlackScreen(self, window):
		self.black_screen.fill((255, 255, 255, self.alpha))
		window.blit(self.black_screen, (self.x, self.y))

	def fadeOut(self):
		self.alpha += 1
		if self.alpha >= 254:
			self.alpha = 0

	def rotate(self, window):
		self.angle %= 360
		self.angle += 5
		self.rotation_sprite = pygame.transform.rotate(self.sprite, self.angle)
		window.blit(self.rotation_sprite, (self.x - self.rotation_sprite.get_width() // 2, self.y - self.rotation_sprite.get_width() // 2))


class Entity:
	def __init__(self, x, y, w, h, file):
		self.x = x
		self.y = y
		self.w = w
		self.h = h
		self.angle = 0 # 90 180 270 360
		self.speed = 12
		self.life = 100
		self.alarm = False

		self.explode = False
		self.alive = True
		self.played = False

		self.laser_speed = 36
		self.lasers = []

		# creating the sprite
		texture = pygame.image.load(file)
		self.sprite = pygame.transform.scale(texture, (self.w, self.h))
		self.angle_sprite = pygame.transform.rotate(self.sprite, self.angle)

		self.score = 0

		self.not_game_over = True


		# explosion sprites, other clases will inherit these sprites, so they can excplode when they die
		self.current_explosion_sprite = 0
		self.explosion_sprites = []
		self.explosion_sprites.append(pygame.image.load("assets/e1.png"))
		self.explosion_sprites.append(pygame.image.load("assets/e2.png"))
		self.explosion_sprites.append(pygame.image.load("assets/e3.png"))
		self.explosion_sprites.append(pygame.image.load("assets/e4.png"))
		self.explosion_sprites.append(pygame.image.load("assets/e5.png"))
		self.explosion_sprites.append(pygame.image.load("assets/e6.png"))
		self.explosion_sprites.append(pygame.image.load("assets/e7.png"))
		self.explosion_sprites.append(pygame.image.load("assets/e8.png"))
		self.explosion_sprites.append(pygame.image.load("assets/e9.png"))
		self.explosion_sprites.append(pygame.image.load("assets/e10.png"))
		self.explosion_sprites.append(pygame.image.load("assets/e11.png"))
		self.explosion_sprites.append(pygame.image.load("assets/e12.png"))


	# regular method to draw the entity
	def draw(self, window):
		window.blit(self.sprite, (self.x, self.y))

	# player sprite was pointing up, so I repositioned it in code, 2 lazy to edit the sprite
	def rotationDraw(self, window):
		#window.blit(self.angle_sprite, (self.x, self.y))
		if self.alive:
			window.blit(self.angle_sprite, (self.x, self.y))

		# aimating the explotion when player dies
		if self.explode:
			if self.current_explosion_sprite < 1:
				sounds['death'].play()

			if self.current_explosion_sprite > 11 and self.current_explosion_sprite < 12:
				self.life = 0
				self.explode = False
				self.current_explosion_sprite = 0
				self.x = -100
				self.y = -100
				sleep(1.0)
				self.not_game_over = False

			self.current_explosion_sprite += 0.6
			window.blit(self.explosion_sprites[int(self.current_explosion_sprite)], (self.x, self.y))
		# drawing the laser in the window
		self.drawLaser(window)


	# if sprite is not at desired angle, use this method outside of the game loop
	def setAngle(self, a):
		self.angle = a
		self.angle_sprite = pygame.transform.rotate(self.sprite, self.angle)

	# player movement
	def update(self, moving_up, moving_down, moving_left, moving_right):
		# prevents glitches when drawing the life bar
		if self.life < 0:
			self.life = 0

		if self.alive:
			if moving_up:
				self.y -= self.speed
			if moving_down:
				self.y += self.speed
			if moving_left:
				self.x -= self.speed
			if moving_right:
				self.x += self.speed

		if self.life < 31:
			self.alarm = True

		if self.alarm and not self.played:
			sounds['alert'].play()
			self.played = True
			self.alarm = False

		if self.life < 1:
			self.alive = False
			self.explode = True
			pygame.mixer.music.stop()

	# every time we prees the space bar this method will be called, and create a new rect object, and will append it to the array
	def shoot(self):
		if self.alive:
			self.laser = rect(self.x, self.y + (self.h // 2), 80, 6, YELLOW)
			self.lasers.append(self.laser)
			sounds['laser7'].play()

	def drawLaser(self, window):
		#drawing and moving the laser
		for i in range(len(self.lasers)):
			if self.lasers[i].x > WINDOW_WIDTH:
				self.lasers.pop(i)
				break
			self.lasers[i].x += self.laser_speed
			self.lasers[i].draw(window)

	def score100(self):
		self.score += 100

	def collidesWith(self, other_body):
		if self.x + self.w < other_body.x or self.x > other_body.x + other_body.w:
			return False
		elif self.y + self.h < other_body.y or self.y > other_body.y + other_body.h:
			return False
		else:
			return True

	def getLife(self):
		return self.life

class Enemy(Entity):
	def __init__(self, x, y, w, h, file):
		super(Enemy, self).__init__(x, y, w, h, file)
		self.speed = 1
		self.laser_speed = 16
		self.shooting_timer = 0
		self.spawn_time = 0
		self.death_time = 6

		self.alive = False
		self.rand_move = [False, False]
		self.life = 15

		# normal UFO SPRITES
		self.current_sprite = 0
		self.sprites = []
		self.sprites.append(pygame.image.load(file))
		self.sprites.append(pygame.image.load("assets/u2.png"))
		self.sprites.append(pygame.image.load("assets/u3.png"))
		self.sprites.append(pygame.image.load("assets/u4.png"))

		for i in range(len(self.sprites)):
			self.sprites[i] = pygame.transform.scale(self.sprites[i], (self.w, self.h))

	def draw(self, window):
		# only draw the sprite when it's alive
		if self.alive and not self.explode:
			window.blit(self.sprites[int(self.current_sprite)], (self.x, self.y))

		if self.explode:
			if self.current_explosion_sprite < 1:
				sounds['explode'].play()
			elif self.current_explosion_sprite > 11:
				self.life = 15
				self.resetPos()
				self.alive = False
				self.explode = False
				self.current_explosion_sprite = 0
			self.current_explosion_sprite += 0.6
			window.blit(self.explosion_sprites[int(self.current_sprite)], (self.x, self.y))

		# if the ufo dies, keep the laser on the screen until it goes out of bounds
		# notice we are not calling the drawLaser method fomr the inheritance,
		# that's because enemy laser moves to the left
		for i in range(len(self.lasers)):
			if self.lasers[i].x < 0:
				self.lasers.pop(i)
				break
			self.lasers[i].x -= self.laser_speed
			self.lasers[i].draw(window)

	def resetPos(self):
			self.alive = False
			self.x = WINDOW_WIDTH + self.w


	def update(self):
		# if it takes 15 hits kill the ufo
		if self.life < 1:
			self.explode = True

		# increment the spawning time
		if not self.alive:
			self.spawn_time += 0.012

		# if the enemy is dead, spawn it after 6 secs
		if self.spawn_time > self.death_time:
			self.alive = True

		# if it goes out of bounds kill it
		if self.x < -self.w:
			self.resetPos()

		if self.alive:
			self.spawn_time = 0
			self.x -= self.speed

			# animating the sprite
			self.current_sprite %= len(self.sprites) - 1
			self.current_sprite += 0.26


			#### UFO AI MOVEMENT AND SHOOTING ###########################################
			# reset the counter
			self.shooting_timer %= 1.6
			# incrementing shooting time how often is the UFO going to shoot
			self.shooting_timer += 0.012

			# when reach 1 seccond, shoot and choose if it's going to move either up or down
			if self.shooting_timer > 0.98 and self.shooting_timer < 1.0:
				self.shoot()
				self.rand_move[0] = False
				self.rand_move[1] = False
				self.rand_move[random.randint(0,1)] = True

			# for about a second randomly move up or down
			if self.shooting_timer < 0.6:
				if self.rand_move[0]:
					self.y -= self.speed + 3
				if self.rand_move[1]:
					self.y += self.speed + 3

	# overriding shoot method, original methot contains yellow color, the enemy's laser will be green
	def shoot(self):
		self.laser = rect(self.x, self.y + (self.h // 2), 80, 6, GREEN)
		self.lasers.append(self.laser)
		sounds['laser8'].play()


class Asteroid(Entity):
	def __init__(self, x, y, w, h, file):
		super(Asteroid, self).__init__(x, y, w, h, file)
		self.asteroid_speed = random.randint(6, 14)
		self.explode = False
		self.counter = 0

		# explosion texture
		explosion_texture = pygame.image.load("assets/exp.png")
		self.explosion_sprite = pygame.transform.scale(explosion_texture, (self.w, self.h))


	def update(self):
		# if it goes out of bounds reset the position
		if self.x < -self.w:
			self.resetPosition()

		self.x -= self.asteroid_speed

	def resetPosition(self):
		self.x = WINDOW_WIDTH + self.w
		self.y = random.randint(0, WINDOW_HEIGHT - self.h)
		self.asteroid_speed = random.randint(1, 20)

	def draw(self, window):
		if not self.explode:
			window.blit(self.sprite, (self.x, self.y))
		if self.explode:
			self.counter += 0.012
			window.blit(self.explosion_sprite, (self.x, self.y))
			if self.counter > 0.09:
				self.resetPosition()
				self.explode = False
				self.counter = 0

class MidBoss(Enemy):
	def __init__(self, x, y, w, h, file):
		super(MidBoss, self).__init__(x, y, w, h, file)
		self.reset_timer = 0
		self.retreat = False
		self.speed = 1
		self.laser_speed = 20

	def rotationDraw(self, window):
		# only draw the sprite when it's alive
		if self.alive and not self.explode:
			window.blit(self.angle_sprite, (self.x, self.y))

		if self.explode:
			if self.current_explosion_sprite < 1:
				sounds['explode'].play()

			elif self.current_explosion_sprite > 11:
				self.life = 15
				self.resetPos()
				self.alive = False
				self.explode = False
				self.current_explosion_sprite = 0
			self.current_explosion_sprite += 0.6
			window.blit(self.explosion_sprites[int(self.current_sprite)], (self.x, self.y))

		for i in range(len(self.lasers)):
			if self.lasers[i].x < 0:
				self.lasers.pop(i)
				break
			self.lasers[i].x -= self.laser_speed
			self.lasers[i].draw(window)

	def newUpdate(self):
		if self.life < 1:
			self.explode = True


		# if it goes out of bounds kill it
		if self.x < WINDOW_WIDTH // 2:
			self.retreat = True

		if self.retreat:
			self.resetPos2()

		if self.alive:
			# self.spawn_time = 0
			self.x -= self.speed


			#### AI MOVEMENT AND SHOOTING ####
			# reset the counter
			self.shooting_timer %= 3
			# incrementing shooting time how often is the UFO going to shoot
			self.shooting_timer += 0.068

			# when reach 1 seccond, shoot and choose if it's going to move either up or down
			if self.shooting_timer > 0.920 and self.shooting_timer < 1.0 or  self.shooting_timer > 1.920 and self.shooting_timer < 2.0:
				self.shoot()

	def resetPos2(self):
		self.reset_timer += 0.012
		if self.reset_timer < 10.0:
			self.speed = 0
			self.x += 6
		if self.reset_timer > 11.0:
			self.reset_timer = 0

		if self.x > WINDOW_WIDTH - self.w:
			self.retreat = False
			self.speed = random.randint(2, 6)

	def followPlayer(self, player):
		if player.y < self.y:
			self.y -= 6
		elif player.y > self.y:
			self.y += 6
		# if self.y < player.y

	def shoot(self):
		self.laser = rect(self.x, self.y + (self.h // 2), 80, 6, RED)
		self.lasers.append(self.laser)
		sounds['laser7'].play()
