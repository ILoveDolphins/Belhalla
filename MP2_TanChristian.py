##Christian Francis Albert Tan, 2016-00331##
##Battle of Belhalla code##
##Goal of the game: Survival game, defeat as many of Arvis' army as you can before they overrun Sigurd's army##
##Sigurd's army is overrun if an enemy reaches the bottom of the map or when Sigurd is defeated##

import pygame
import random ##will affect enemy spawn##
import time
import BelhallaModules

pygame.mixer.init(48000, -16, 2, 1024)
pygame.init()
pygame.mixer.init()
screen = pygame.display.set_mode((1080,960))
pygame.display.set_caption('Battle of Belhalla')

clock = pygame.time.Clock()

openmanual = open('help.txt', 'r')
manualsound = pygame.mixer.Sound('Assets/Se_sys_home_board.wav')

middlefont = pygame.font.SysFont(None, 50) ##font for game middle text##
numberfont = pygame.font.SysFont(None, 25)

def midmessage(msg,color, x, y): ##will be used for all text displays for the game, so calling for x, y coordinates is needed##
    screen_text = middlefont.render(msg, True, color)
    screen.blit(screen_text, [x, y])

def numbermessage(msg, color, x, y):
	screen_text = numberfont.render(msg, True, color)
	screen.blit(screen_text, [x,y])

spawnlist = [0,5] ##rows already occupied by enemies will not be used to spawn more enemies##
row = [170,260,350,440,530,620,710]
column = [280, 370, 460, 550, 640, 720]

SigurdReady = ['Assets/SigurdReady1.wav', 'Assets/SigurdReady2.wav', 'Assets/SigurdReady3.wav', 'Assets/SigurdReady4.wav']
ArdenReady = ['Assets/ArdenReady1.wav', 'Assets/ArdenReady2.wav', 'Assets/ArdenReady3.wav', 'Assets/ArdenReady4.wav']
AyraReady = ['Assets/AyraReady1.wav', 'Assets/AyraReady2.wav', 'Assets/AyraReady3.wav', 'Assets/AyraReady4.wav']
JamkeReady = ['Assets/JamkeReady1.wav', 'Assets/JamkeReady2.wav', 'Assets/JamkeReady3.wav', 'Assets/JamkeReady4.wav']

class GameUnit: ##initializes units for game##
	def __init__(self, Name, HP, Atk, Def, Mov, Ran, Ability, UnitType, sprite, xcoord, ycoord):
		self.Name = Name
		self.HP = HP ##Total Health Points, dies when HP reaches 0##
		self.Atk = Atk ##Attack, amount of damage unit can deal
		self.Def = Def ##Defense, reduces damage taken##
		self.Mov = Mov ##Movement, amount of spaces unit can move at a turn##
		self.Ability = Ability ##Unit's special ability##
		self.UnitType = UnitType ##Tag that checks which phase unit can act on##
		self.currentHP = HP ##starts game with max HP##
		self.displayHP = str(self.HP) ##for displaying HP ingame##
		self.displayAtk = str(self.Atk) ##for displaying Atk ingame##
		self.displayDef = str(self.Def) ##for displaying Def ingame##
		self.sprite = pygame.image.load(sprite)
		self.xcoord = xcoord
		self.ycoord = ycoord
		self.position = (column[xcoord], row[ycoord])

##Game Units List with starting positions##
Sigurd = GameUnit('Sigurd', 41, 38, 32, 3, 1,'Tyrfing', 'player', 'Assets/Sigurd.png', 1, 6)
Arden = GameUnit('Arden', 61, 35, 41, 1, 1,'Strong and Tough','player', 'Assets/Arden.png', 2, 6)
Ayra = GameUnit('Ayra', 41, 33, 28, 2, 1,'Astra', 'player', 'Assets/Ayra.png', 3, 6)
Jamke = GameUnit('Jamke', 34, 36, 26, 2, 2,'Killer Bow', 'player', 'Assets/Jamke.png', 4, 6)
Knight = GameUnit('Armor Knight', 40, 33, 23, 1, 1, 'Safeguard', 'enemy', 'Assets/Knight.png', 1, 0) 
Pegasus = GameUnit('Pegasus Knight', 28, 20, 25, 2, 1, 'Ridersbane', 'enemy', 'Assets/Pegasus.png', 2, 0) 
Thief = GameUnit('Thief', 28, 29, 19, 3, 1, 'Pickpocket', 'enemy', 'Assets/Thief.png', 3, 0)
Fighter = GameUnit('Fighter', 37, 30, 25, 2, 1, 'Armorsmasher', 'enemy', 'Assets/Fighter.png', 4, 0)
##Note: Enemies respawn at top row##


background = pygame.image.load('Assets/GameUI.png') ##assets used to making background also found separately in assets folder##
currententities = {Sigurd : Sigurd.position, Arden : Arden.position, Ayra : Ayra.position, Jamke : Jamke.position, 
Knight : Knight.position, Pegasus : Pegasus.position, Thief : Thief.position, Fighter : Fighter.position}

vulnerary = 0 ##counter for healing item, starts at 0 and gain 1 from defeating a Thief, restores 10 HP to all player units on use##
KO = 0 ##KO count##
turn = 1 ##turn counter, always starts at turn 1, 1 turn = one player and enemy phase##
t = turn
turndisplay = str(turn) ##for displaying turn on screen#
phase = 'player' ##game will start in player phase but will switch between player and enemy phase constantly##
running = True ##to keep the game running##
##set all important factors before game starts##

def playerphase(x,y,z):
	playsound = pygame.mixer.Sound('Assets/Se_sys_phase_player1.wav')
	playsound.set_volume(0.8)
	playsound.play()
	midmessage('Player Phase', (0,100,200), 450, 440)
	midmessage('Turn', (0, 100, 200), 490, 490)
	midmessage(z, (0, 100, 200), 580, 490)
	pygame.display.flip()
	time.sleep(1.5)
	playsound = pygame.mixer.Sound('Assets/Map_7.wav')
	playsound.set_volume(0.50)
	playsound.play()
	BelhallaModules.updateboard(currententities)

def enemyphase(x, y, z): ##all actions to occur during enemy phase##
	playsound = pygame.mixer.Sound('Assets/Se_sys_phase_enemy1.wav')
	playsound.set_volume(0.8)
	playsound.play()
	midmessage('Enemy Phase', (200,0,0), 440, 440)
	midmessage('Turn', (200, 0, 0), 490, 490)
	midmessage(z, (200, 0, 0), 580, 490)
	pygame.display.flip()
	time.sleep(1.5)
	if (y % 5) != 0:
		playsound = pygame.mixer.Sound('Assets/Map_2.wav')
		playsound.set_volume(0.80)
		playsound.play()
		BelhallaModules.updateboard(currententities)
	if (y % 5) == 0:
		BelhallaModules.Valflame(currententities)
	if Knight.currentHP <= 0:
		BelhallaModules.spawn(Knight, spawnlist, currententities, column, row)
		Knight.currentHP = Knight.HP
	if Pegasus.currentHP <= 0:
		BelhallaModules.spawn(Pegasus, spawnlist, currententities, column, row)
		Pegasus.currentHP = Pegasus.HP
	if Thief.currentHP <= 0:
		BelhallaModules.spawn(Thief, spawnlist, currententities, column, row)
		Thief.currentHP = Thief.HP
	if Fighter.currentHP <= 0:
		BelhallaModules.spawn(Fighter, spawnlist, currententities, column, row)
		Fighter.currentHP = Fighter.HP
	phase = 'player'

##constants in the game##
pygame.mixer.music.load('Assets/WhatLiesattheEnd.wav')
pygame.mixer.music.set_volume(0.40)
pygame.mixer.music.play(-1) ##loops##
##constants in the game##
##Note: map will be in a 6 x 7 grid (6 columns, 7 rows), enemies will spawn at row A every enemy phase, after existing enemies have moved##

Sigurd.movestate = True ##set everyone's move and attack state to be ready##
Sigurd.attackstate = True
Sigurd.Ready = False
Arden.movestate = True
Arden.attackstate = True
Arden.Ready = False
Ayra.movestate = True
Ayra.attackstate = True
Ayra.Ready = False
Jamke.movestate = True
Jamke.attackstate = True
Jamke.Ready = False

select = pygame.mixer.Sound('Assets/Map_4.wav')
invalid = pygame.mixer.Sound('Assets/Common_1.wav')
BelhallaModules.updateboard(currententities)
playerphase(phase, turn, turndisplay)

if Sigurd.currentHP <= 0:
	playsound = pygame.mixer.Sound('Assets/SigurdDefeat.wav')
	playsound.play()
	time.sleep(10)
	running = False

while running:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			running = False
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				running = False
			if event.key == pygame.K_h:
				print(openmanual.read())
				manualsound.play()
			if event.key == pygame.K_ESCAPE:
				running = False
			if event.key == pygame.K_1:
				if Sigurd.attackstate == True:
					Sigurd.Ready = True
					Arden.Ready = False
					Ayra.Ready = False
					Jamke.Ready = False
					random.shuffle(SigurdReady)
					playsound = pygame.mixer.Sound(SigurdReady[0])
					select.play()
					playsound.play()
					if Sigurd.currentHP >= (Sigurd.HP / 2):
						art = pygame.image.load('Assets/SigurdHealthy.png')
						BelhallaModules.updateboard(currententities)
						screen.blit(art, (0,0))
					else:
						art = pygame.image.load('Assets/SigurdInjured.png')
						BelhallaModules.updateboard(currententities)
						screen.blit(art, (0,0))
				else:
					invalid.play()
			if event.key == pygame.K_2:
				if Arden.attackstate == True:
					Arden.Ready = True
					Sigurd.Ready = False
					Ayra.Ready = False
					Jamke.Ready = False
					random.shuffle(ArdenReady)
					playsound = pygame.mixer.Sound(ArdenReady[0])
					select.play()
					playsound.play()
					if Arden.currentHP >= (Arden.HP / 2):
						art = pygame.image.load('Assets/ArdenHealthy.png')
						BelhallaModules.updateboard(currententities)
						screen.blit(art, (0,0))
					else:
						art = pygame.image.load('Assets/ArdenInjured.png')
						BelhallaModules.updateboard(currententities)
						screen.blit(art, (0,0))
				else:
					invalid.play()
			if event.key == pygame.K_3:
				if Ayra.attackstate == True:
					Ayra.Ready = True
					Sigurd.Ready = False
					Arden.Ready = False
					Jamke.Ready = False
					random.shuffle(AyraReady)
					playsound = pygame.mixer.Sound(AyraReady[0])
					select.play()
					playsound.play()
					if Ayra.currentHP >= (Ayra.HP / 2):
						art = pygame.image.load('Assets/AyraHealthy.png')
						BelhallaModules.updateboard(currententities)
						screen.blit(art, (0,0))
					else:
						art = pygame.image.load('Assets/AyraInjured.png')
						BelhallaModules.updateboard(currententities)
						screen.blit(art, (0,0))
				else:
					invalid.play()
			if event.key == pygame.K_4:
				if Jamke.attackstate == True:
					Jamke.Ready = True
					Sigurd.Ready = False
					Arden.Ready = False
					Ayra.Ready = False
					random.shuffle(JamkeReady)
					playsound = pygame.mixer.Sound(JamkeReady[0])
					select.play()
					playsound.play()
					if Jamke.currentHP >= (Jamke.HP / 2):
						art = pygame.image.load('Assets/JamkeHealthy.png')
						BelhallaModules.updateboard(currententities)
						screen.blit(art, (0,0))
					else:
						art = pygame.image.load('Assets/JamkeInjured.png')
						BelhallaModules.updateboard(currententities)
						screen.blit(art, (0,0))
				else:
					invalid.play()
			if event.key == pygame.K_RETURN:
				playsound = pygame.mixer.Sound('Assets/Common_2.wav')
				playsound.play()
				BelhallaModules.check(currententities, spawnlist)
				if Thief.currentHP <= 0:
					KO += 1
					vulnerary += 1
				if Knight.currentHP <= 0:
					KO += 1
				if Pegasus.currentHP <= 0:
					KO += 1
				if Fighter.currentHP <= 0:
					KO += 1
				BelhallaModules.updateboard(currententities)
				phase = 'enemy'
				enemyphase(phase, turn, turndisplay)
				BelhallaModules.updateboard(currententities)
				activeunits = list(currententities.keys())
				coordinates = list(currententities.values())
				try:
					for unit in activeunits:
						if unit.UnitType == 'enemy':
							movement = unit.Mov
							for coordinate in coordinates:
								unitcheck = unit.ycoord + 1
								backtrack = unit.ycoord - 2
								coordinate == (column[unit.xcoord], row[unitcheck])
								if coordinate in coordinates:
									coordinate = (column[unit.xcoord], row[backtrack])
							while movement > 0:
								unit.ycoord += 1
								unit.position = (column[unit.xcoord], row[unit.ycoord])
								currententities[unit] = unit.position
								movement -= 1
								activeunits = list(currententities.keys())
								coordinates = list(currententities.values())
							BelhallaModules.updateboard(currententities)
					turn += 1
					turndisplay = str(turn)
					playerphase(phase, turn, turndisplay)
					phase = 'player'
					activeunits = list(currententities.keys())
					coordinates = list(currententities.values())
					for x in activeunits:
						if x.UnitType == 'player':
							x.movestate = True
							x.attackstate = True
				except IndexError:
					playsound = pygame.mixer.Sound('Assets/SigurdDefeat.wav')
					playsound.play()
					time.sleep(2)
					running = False
			if event.key == pygame.K_BACKQUOTE and vulnerary == 0:
				invalid.play()
			if event.key == pygame.K_BACKQUOTE and Sigurd.currentHP == Sigurd.HP and Arden.currentHP == Arden.HP and Ayra.currentHP == Ayra.HP and Jamke.currentHP == Jamke.HP:
				invalid.play()
			if event.key == pygame.K_BACKQUOTE and vulnerary > 0 and Sigurd.currentHP < Sigurd.HP and Arden.currentHP < Arden.HP and Ayra.currentHP < Ayra.HP and Jamke.currentHP < Jamke.HP:
				BelhallaModules.healing(Sigurd)
				BelhallaModules.healing(Arden)
				BelhallaModules.healing(Ayra)
				BelhallaModules.healing(Jamke)
				vulnerary -= 1
	pygame.display.flip()
	clock.tick(60)
pygame.display.flip()