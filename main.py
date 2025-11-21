import sys
import pygame
import random
import title
import ending
import rect2
from time import sleep
from settings import WINDOW_WIDTH, WINDOW_HEIGHT, RED, YELLOW, GREEN, BLUE, VIOLET, ORANGE, WHITE
from entities import Entity, Enemy, Asteroid, MidBoss, rect, sounds, init_sounds

pygame.init()
pygame.display.set_caption("Last Invasion By: Lu")

window = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

#initializes mixer for audio|original buffer=4096
pygame.mixer.pre_init(44100, 16, 2, 512)

# Initialize sounds from entities
init_sounds()

# Map sounds to global variables for compatibility
laser7 = sounds['laser7']
laser8 = sounds['laser8']
mini_boss_laser = sounds['mini_boss_laser']
death = sounds['death']
explode = sounds['explode']
alert = sounds['alert']
hit = sounds['hit']
damage = sounds['damage']
health = sounds['health']
highScore = sounds['highScore']

# main theme
def playMusic():
	pygame.mixer.music.load("sound/Subdream-Space_Philately.mp3")
	pygame.mixer.music.play(-1)

# mini boss theme
def playMidBossMusic():
	pygame.mixer.music.load("sound/Alert! Outsider!.ogg")
	pygame.mixer.music.play(-1)

#%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%  main game class   %%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%%5
class Game:
	def __init__(self):
		self.level = 1
		self.not_game_over = True
		self.final_score = 0
		self.final_life = 0

	def run(self):
		game_time = 1
		clock = pygame.time.Clock()

		# ^^^^^^^^^^^^^^^^^^^^^^    CREATING ALL THE ENTITIES AND ITEMS FOR THE GAME ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

		# PLAYER    #
		player = Entity(0, 0, 60, 60, "assets/ship.png")
		player.setAngle(270)
		player.laser_speed = 60

		# POWER UPS! 
		powerUps = []
		for i in range(4):
			p = rect2.Rect(player.x, player.y, 20, 20, YELLOW)
			p.setAngles(1.57 * i, 1.57 * i)
			p.setAngleSpeed(0.08 * 2, 0.08 * 2)
			p.setDistance(200)
			powerUps.append(p)

		# mini boss and ufo
		mini_boss = MidBoss(WINDOW_WIDTH + 400, WINDOW_HEIGHT //2, 100, 100, "assets/ship5.png")
		mini_boss.setAngle(90)
		mini_boss.life = 200

		ufo = Enemy(WINDOW_WIDTH + 200, WINDOW_HEIGHT // 2, 80, 40, "assets/u1.png")
		ufo2 = Enemy(WINDOW_WIDTH + 200, WINDOW_HEIGHT // 2, 80, 40, "assets/u1.png")
		ufo2.speed = 3
		ufo2.laser_speed = 32
		ufo2.death_time = 12


		# BARS and ITEMS 
		bar = rect(0,0, player.life, 30, GREEN)
		battery = rect(190, 0, player.life + 40, 46, WHITE)
		battery.loadSprite("assets/battery.png")
		mini_boss_life = rect(0,0, mini_boss.life, 2, GREEN)

		##### LIFE AND POWER UP 
		cell = rect(WINDOW_WIDTH + 60, WINDOW_HEIGHT // 2, 60,60, WHITE)
		cell.loadSprite("assets/cell.png")
		active_cell = False

		cell2 = rect(WINDOW_WIDTH + 60, WINDOW_HEIGHT // 2, 60,60, WHITE)
		cell2.loadSprite("assets/cell2.png")
		active_cell2 = False

		# asteroids and stars
		asteroids = []
		for i in range(10):
			asteroid = Asteroid(WINDOW_WIDTH + 3000, random.randint(0, WINDOW_HEIGHT - 60), 60, 60, "assets/asteroid.png")
			asteroids.append(asteroid)

		stars_amount = 160
		slow_stars_amount = 300
		stars = []
		slow_stars = []
		slow_star_speed = 2
		fast_star_speed = 6

		for i in range(stars_amount):
			star = rect(12 * i, random.randint(0, WINDOW_HEIGHT - 2), 2, 2, WHITE)
			stars.append(star)

		for i in range(slow_stars_amount):
			star = rect(12 * i, random.randint(0, WINDOW_HEIGHT - 2), 1, 1, WHITE)
			slow_stars.append(star)


		# these will mover on the background for visual effect
		planet = rect(WINDOW_WIDTH + 200, 10, 160, 160, WHITE)
		planet.loadSprite("assets/parallax-space-big-planet.png")
		planet2 = rect(WINDOW_WIDTH + 200, 10, 200, 200, WHITE)
		planet2.loadSprite("assets/earth.png")
		planet3 = rect(WINDOW_WIDTH + 200, 10, 180, 240, WHITE)
		planet3.loadSprite("assets/Citronis.png")
		planets = [planet, planet2, planet3]
		planet_index = 0
		# give them a random y position
		for i in range(len(planets)):
			planets[i].y = random.randint(0, WINDOW_HEIGHT - planets[i].w)

		# background sprite
		background = rect(0,0,WINDOW_WIDTH, WINDOW_HEIGHT, WHITE)
		background.loadSprite("assets/Background-4.png")

		black_screen = rect(0,0, WINDOW_WIDTH, WINDOW_HEIGHT, WHITE)

		# ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

		# VARIABLES FOR THE PLAYER AND CELL, CLASSES WERE GETTING TOO LONG

		moving_up = False
		moving_down = False
		moving_left = False
		moving_right = False
		running = True
		# for the + 100 points effect
		colorIndex = 0
		colors = [RED, YELLOW, ORANGE, GREEN, BLUE, VIOLET]

		# before the main loop play the main music
		playMusic()
		#system("clear")
		while running:

			# keep track of the score
			self.final_score = player.score
			# keep checking if the player dies, if it does, GAME OVER
			running = player.not_game_over

			# +++++++++++++++	 game events 	+++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++
			for event in pygame.event.get():
				# closing the window with [x]
				if event.type == pygame.QUIT:
					pygame.quit()
					sys.exit()
					running = False

				#----------   controls ----------------#
				## keypress ##
				elif event.type == pygame.KEYDOWN:

					# $ pressing the up arrow ey
					if event.key == pygame.K_UP:
						moving_up = True

					# $ pressing the down arrow key
					elif event.key == pygame.K_DOWN:
						moving_down = True
					# $ pressing the left arrow key
					elif event.key == pygame.K_LEFT:
						moving_left = True

					# $ pressing the right arrow key
					elif event.key == pygame.K_RIGHT:
						moving_right = True

					# when pressing space, shoot the lasser
					if event.key == pygame.K_SPACE:
						player.shoot()

				### leting go of the keys
				elif event.type == pygame.KEYUP:
					if event.key == pygame.K_UP:
						moving_up = False
					elif event.key == pygame.K_DOWN:
						moving_down = False
					elif event.key == pygame.K_LEFT:
						moving_left = False
					elif event.key == pygame.K_RIGHT:
						moving_right = False
				#------------------------------------------#

			# ++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++++

#____________________ COLLITION DETECTION YANDERE DEV CODE XD ________________________________________________________________

			# for the amount of asteroid, if a player laser hits an asteroid respawn it and add 1 point
			for i in range(len(asteroids)):
				for j in range(len(player.lasers)):
					# print("LASERS: ", len(player.lasers), "ASTEROIDS: ", len(asteroids))  DATA FOR DEBUG
					if player.lasers[j].collidesWith(asteroids[i]) and not asteroids[i].explode:
						asteroids[i].explode = True
						player.lasers.pop(j)
						player.score += 1
						pygame.mixer.Sound.play(hit)
						break

				# if powerups collides with asteroids, destoyr asteroid and decrease power up life
				for k in range(len(powerUps)):
					if powerUps[k].collidesWith(asteroids[i]) and not asteroids[i].explode and powerUps[k].active:
						asteroids[i].explode = True
						player.score += 1
						powerUps[k].life -= 1
						pygame.mixer.Sound.play(hit)
						break

			# if the laser collides with UFO, take 1 ufo life away and add 1 point
			for i in range(len(player.lasers)):
				if player.lasers[i].collidesWith(ufo) and ufo.alive:
					ufo.life -= 1
					player.score += 1
					player.lasers.pop(i)
					pygame.mixer.Sound.play(hit)
					break
				if player.lasers[i].collidesWith(ufo2) and ufo2.alive:
					ufo2.life -= 1.8
					player.score += 1
					player.lasers.pop(i)
					pygame.mixer.Sound.play(hit)
					break


				# if the lasers colide with mini boss take away 1 life from miniboss
				if player.lasers[i].collidesWith(mini_boss) and mini_boss.alive:
					mini_boss.life -= 1
					player.score += 1
					player.lasers.pop(i)
					pygame.mixer.Sound.play(hit)
					break


			# if the power ups collide with ufo take both ufo and power ups take dmg
			for i in range(len(powerUps)):
				if powerUps[i].collidesWith(ufo) and ufo.alive and powerUps[i].active:
					ufo.life -= 0.5
					powerUps[i].life -= 1
					player.score += 1
					pygame.mixer.Sound.play(hit)
					break
				elif powerUps[i].collidesWith(ufo2) and ufo2.alive and powerUps[i].active:
					ufo2.life -= 0.5
					powerUps[i].life -= 1
					player.score += 1
					pygame.mixer.Sound.play(hit)
					break
				elif powerUps[i].collidesWith(mini_boss) and mini_boss.alive and powerUps[i].active:
					mini_boss.life -= 1
					powerUps[i]. life -= 2
					player.score += 1
					pygame.mixer.Sound.play(hit)
					break


			# if the ufo lasser hits the player, take away some life
			for i in range(len(ufo.lasers)):
				if ufo.lasers[i].collidesWith(player):
					player.life -= 12
					ufo.lasers.pop(i)
					pygame.mixer.Sound.play(damage)
					break
			# same as avobe, for ufo2
			for i in range(len(ufo2.lasers)):
				if ufo2.lasers[i].collidesWith(player):
					player.life -= 12
					ufo2.lasers.pop(i)
					pygame.mixer.Sound.play(damage)
					break

			# if the miniboss lasser hits the player, take away some life
			for i in range(len(mini_boss.lasers)):
				if mini_boss.lasers[i].collidesWith(player):
					player.life -= 6
					mini_boss.lasers.pop(i)
					pygame.mixer.Sound.play(damage)
					break

			# if player colides with asteroid, take away 1 life point
			for i in range(len(asteroids)):
				if player.collidesWith(asteroids[i]) and not asteroids[i].explode:
					player.life -= 6
					asteroids[i].explode = True
					pygame.mixer.Sound.play(damage)

			# if player collides with ufo, game over
			if player.collidesWith(ufo):
				player.life = 0
				ufo.life = 0
			if player.collidesWith(ufo2):
				player.life = 0
				ufo2.life = 0

			# if player colides with minibos kill player
			if player.collidesWith(mini_boss):
				player.life = 0
				# mini_boss.life = 0

			# if the ufo explodes, increment 100 score points to the player, regardless if player died, (because I'm a nice guy)
			if ufo.explode and ufo.current_explosion_sprite > 11:
				player.score100()
				active_cell = True
			if ufo2.explode and ufo2.current_explosion_sprite > 11:
				player.score100()
				active_cell2 = True

			if mini_boss.explode and mini_boss.current_explosion_sprite > 11:
				player.score100()
				player.score100()
				player.score100()


			# if player colects the cell, restart cell position and add life to the player
			if player.collidesWith(cell):
				pygame.mixer.Sound.play(health)
				active_cell = False
				cell.x = WINDOW_WIDTH + cell.w
				cell.y = random.randint(0, WINDOW_HEIGHT - cell.h)
				player.life += 25

			if player.collidesWith(cell2):
				pygame.mixer.Sound.play(health)
				active_cell2 = False
				cell2.x = WINDOW_WIDTH + cell.w
				cell2.y = random.randint(0, WINDOW_HEIGHT - cell.h)
				for i in range(len(powerUps)):
					powerUps[i].activate()
#______________________________________________________________________________________________________________________________

			# ==================	prevent entities going out of bounds =============================
			if player.y > WINDOW_HEIGHT - player.h:
				player.y -= player.speed
			elif player.y < 0:
				player.y += player.speed

			if player.x < 0:
				player.x += player.speed
			elif player.x > WINDOW_WIDTH - player.w:
				player.x -= player.speed

			if ufo.y > WINDOW_HEIGHT - ufo.w:
				ufo.y -= ufo.speed + 3
			elif ufo.y < 0:
				ufo.y += ufo.speed + 3

			if ufo2.y > WINDOW_HEIGHT - ufo2.w:
				ufo2.y -= ufo2.speed + 3
			elif ufo2.y < 0:
				ufo2.y += ufo2.speed + 3

			if mini_boss.y < 0:
				mini_boss.y += mini_boss.speed + 3

			elif mini_boss.y > WINDOW_HEIGHT - mini_boss.h:
				mini_boss.y -= mini_boss.speed + 3

			# I was gonna put this in the miniboss class, but the code was getting over complicated
			if not mini_boss.retreat:
				mini_boss.followPlayer(player)
			#========================================================================================


			## FONTS AND LIFE BARS @@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

			if player.life < 31:
				bar.changeColor(RED)
			else:
				bar.changeColor(GREEN)

			score  = pygame.font.Font("font/4B.ttf", 25)
			score = score.render("SCORE " + str(player.score), True, (0,255,0))

			scoreUp  = pygame.font.Font("font/4B.ttf", 25)
			scoreUp = scoreUp.render("SCORE + 100 ", True, colors[colorIndex])
			colorIndex += 1
			colorIndex %= len(colors) - 1

			life = pygame.font.Font("font/Arcade.ttf", 80)
			life = life.render("LIFE ", False, (0,255,0))

			#prevents glitches
			if player.life < 0:
				player.life = 0
			life_bar = pygame.transform.scale(bar.surface, (player.life, bar.h))

			if mini_boss.life < 0:
				mini_boss.life = 0

			# miniboss health bar
			miniboss_bar = pygame.transform.scale(mini_boss_life.surface, (mini_boss.life, mini_boss_life.h))


			#@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@

			# --------	GAME RULES --------------------------------------------
			if game_time > 1030:
				slow_star_speed = 6
				fast_star_speed = 20
				black_screen.fadeOut()

				# hide the asteroids
				for i in range(len(asteroids)):
					asteroids[i].speed = 0
					asteroids[i].y = 2000


			if game_time > 1050 and game_time < 1050.4:
				pygame.mixer.music.stop()
				playMidBossMusic()
				mini_boss.alive = True

			# if pass miniboss spawn time and booth enemies dead game over, player wins
			if game_time > 1050 and not mini_boss.alive and not ufo.alive and not ufo2.alive:
				sleep(1.0)
				running = False

			# -----------------------------------------------------------------

			#<<<<<<<<<<<<<<<<<<<<<<<  movement  <<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<<

			# PLAYER MOVEMENT, ASTEROIDS MOVEMENT, UFO MOVEMENT AND MINI BOSS MOVEMENT
			player.update(moving_up, moving_down, moving_left, moving_right)
			for i in range(len(asteroids)):
				asteroids[i].update()

			ufo.update()
			ufo2.update()
			mini_boss.newUpdate()

			# move the background planets
			planets[planet_index].x -= 0.6
			if planets[planet_index].x < -1000:
				planets[planet_index].x = WINDOW_WIDTH + 200
				planets[planet_index].y = random.randint(0, WINDOW_HEIGHT - planets[planet_index].w)
				planet_index += 1
				planet_index %= len(planets)


			if player.life > 100:
				player.life = 100

			if active_cell:
				cell.x -= 2
				if cell.x < -cell.w:
					active_cell = False
					cell.x = WINDOW_WIDTH + cell.w
					cell.y = random.randint(0, WINDOW_HEIGHT - cell.h)

			if active_cell2:
				cell2.x -= 2
				if cell2.x < -cell.w:
					active_cell2 = False
					cell2.x = WINDOW_WIDTH + cell.w
					cell2.y = random.randint(0, WINDOW_HEIGHT - cell.h)

			# >>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>>


			#***************************    RENDER 		*****************************************************************************************************
			window.fill(0)

			# if no miniboss draw background and planets
			if game_time < 1050:
				background.drawSprite(window)
				#drawing the stars, slow stars will desapear when the boos comes in
				for i in range(slow_stars_amount):
					slow_stars[i].x -= slow_star_speed
					if slow_stars[i].x < - 6:
						slow_stars[i].x = WINDOW_WIDTH + 6
					slow_stars[i].draw(window)

				planets[planet_index].drawSprite(window)

			# this screen is alpha 0 at the begining, before mini boss appear, alpha will increase, giving a fade out effect on screen
			if game_time < 1050:
				black_screen.drawBlackScreen(window)

			for i in range(stars_amount):
				stars[i].x -= fast_star_speed
				if stars[i].x < - 6:
					stars[i].x = WINDOW_WIDTH + 6
				stars[i].draw(window)

			player.rotationDraw(window)
			for i in range(len(powerUps)):
				powerUps[i].update(player.x + player.w // 2, player.y + player.h // 2)
				powerUps[i].spin()
				powerUps[i].drawCircle(window)

			if game_time < 1050:
				for i in range(len(asteroids)):
					asteroids[i].draw(window)

			ufo.draw(window)
			ufo2.draw(window)
			mini_boss.rotationDraw(window)


			# DRAWING SCORE AND LIFE BAR
			window.blit(score, (WINDOW_WIDTH - 300,0))
			window.blit(life, (0, -10))
			window.blit(life_bar,(200,10))
			if ufo.explode:
				window.blit(scoreUp, (ufo.x, ufo.y))
				pygame.mixer.Sound.play(highScore)
			if ufo2.explode:
				window.blit(scoreUp, (ufo2.x, ufo2.y))
				pygame.mixer.Sound.play(highScore)

			if mini_boss.alive:
				window.blit(miniboss_bar,(mini_boss.x, mini_boss.y  - 4))
				battery.drawSprite(window)

			#cell.drawSprite(window)
			cell.rotate(window)
			cell2.rotate(window)

			game_time += 0.12
			pygame.display.update()
			clock.tick(60)
			#*******************************************************************************************************************************************

		# if the main loop breaks get the player life so we can decide if we get a wining screen or loosing screen
		self.final_life = player.getLife()


	def game_over(self):
		self.not_game_over = False


# create and start the main menu
mainTitle = title.mainScreen()
mainTitle.run()

# if player chooses to play run the game, otherwise, quit pygame
if mainTitle.playGame:
	mainGame = Game()
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

#quit()
pygame.quit()
sys.exit()



