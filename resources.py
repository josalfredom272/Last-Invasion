import pygame

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

# main theme
def playMusic():
	pygame.mixer.music.load("sound/Subdream-Space_Philately.mp3")
	pygame.mixer.music.play(-1)

# mini boss theme
def playMidBossMusic():
	pygame.mixer.music.load("sound/Alert! Outsider!.ogg")
	pygame.mixer.music.play(-1)
