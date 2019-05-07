##Christian Francis Albert Tan, 2016-00331##
##Battle of Belhalla modules##

import pygame
import time
import random
screen = pygame.display.set_mode((1080,960))

def highlight(u, x, y, column, row):
	a = column[x - 1]
	b = row[y]
	if u.movestate == True and u.Ready == True:
		pygame.draw.rect(screen, (0,0,255), (a, b, 90, 90))

def updateboard(entities): ##updates images on screen##
	background = pygame.image.load('Assets/GameUI.png')
	screen.blit(background, (0,0))
	units = list(entities.keys())
	coordinates = list(entities.values())
	x = 0
	length = len(units)
	while x < length:
		screen.blit(units[x].sprite, coordinates[x])
		x += 1
	pygame.display.flip()

def spawn(x,y,z, column, row):
	random.shuffle(y)
	x.xcoord = y[0]
	del y[0]
	x.ycoord = 0
	x.position = (column[x.xcoord], row[x.ycoord])
	z[x] = x.position

def check(currententities, spawnlist):
	dead = pygame.mixer.Sound('Assets/Se_btl_dead1.wav')
	units = list(currententities.keys())
	for unit in units:
		if unit.currentHP <= 0:
			del currententities[unit]
			if unit.UnitType == 'player':
				dead.play()
			if unit.UnitType == 'enemy':
				dead.play()
				spawnlist.append(unit.xcoord)
			if unit.Name == 'Thief':
				updateboard(currententities)
				time.sleep(1)
				playsound = pygame.mixer.Sound('Assets/Se_summon_herodic_ring.wav')
				playsound.set_volume(1.5)
				playsound.play()
			updateboard(currententities)


def Valflame(x):
	Valflame = ['Assets/Valflame1.wav', 'Assets/Valflame2.wav', 'Assets/Valflame3.wav', 'Assets/Valflame4.wav']
	flames = pygame.mixer.Sound('Assets/Se_effect_fire02.wav')
	debuff = pygame.mixer.Sound('Assets/Se_sys_powerdown1.wav')
	debuff.set_volume(0.5)
	buff = pygame.mixer.Sound('Assets/Se_sys_powerup1.wav')
	buff.set_volume(0.5)
	random.shuffle(Valflame)
	ValflameActivate = pygame.mixer.Sound(Valflame[0])
	ValflameActivate.play()
	time.sleep(0.5)
	flames.play()
	pygame.draw.rect(screen, (180, 0, 0), (270, 165, 540, 640))
	pygame.display.flip()
	time.sleep(0.8)
	pygame.draw.rect(screen, (200,200,200), (270,165,540,640))
	pygame.display.flip()
	time.sleep(0.2)
	debuff.play()
	buff.play()
	updateboard(x)
	x =list(x.keys())
	for z in x:
		if z.UnitType == 'player' and z.Ability != 'Tyrfing' and z.currentHP > 10:
			z.currentHP -= 10
		if z.UnitType == 'player' and z.Ability != 'Tyrfing' and z.currentHP <= 10:
			z.currentHP == 1
		if z.UnitType == 'player' and z.Ability == 'Tyrfing' and z.currentHP > 5:
			z.currentHP -= 5
		if z.UnitType == 'player' and z.Ability == 'Tyrfing' and z.currentHP <= 5:
			z.currentHP == 1
		if z.UnitType == 'enemy':
			z.HP += 2
			z.currentHP += 2
			z.Atk += 2

def combat(x,y, currententities): ##x initiates, y takes damage then counters##
##ability checks come first before doing combat calculations##
	ding = pygame.mixer.Sound('Assets/Se_btl_damage0.wav')
	hit = pygame.mixer.Sound('Assets/Se_damage_hundred_1.wav')
	damagedealt = 0
	damagereceived = 0
	if x.Ability == 'Strong and Tough' and phase == 'enemy':
		x.Atk += 10
		x.Def += 10
	if x.Ability == 'Strong and Tough' and phase == 'player' and turn > 1: ##reverts buff from Strong and Tough for player phase##
		x.Atk -= 10
		x.Def -= 10
	if x.Ability == 'Safeguard' and phase == 'player':
		x.Def += 6
	if x.Ability == 'Safeguard' and phase == 'enemy': ##like Strong and Tough, reverts in non attacking phase##
		x.Def -= 6
	if x.Ability == 'Ridersbane' and y == 'Sigurd': ##game will round off values by using integer##
		x.Atk = int(x.Atk * 1.5)
	if x.Ability == 'Armorsmasher' and y == 'Arden':
		x.Atk = int(x.Atk * 1.5)
	damagedealt = (x.Atk - y.Def) ##put after Strong and Tough and enemy abilities since they boost Atk and Def##
	if x.Ability == 'Astra' and phase == 'player':
		damagedealt = (damagedealt * 2)
	if x.Ability == 'Ridersbane' and y == 'Sigurd':
		damagedealt += 10
	if damagedealt <= 0:
		if x.ability == 'Astra' and phase == 'player':
			ding.play()
			time.sleep(0.2)
			ding.play()
		else:
			ding.play()
	if damagedealt > 0:
		if x.ability == 'Astra' and phase == 'player':
			hit.play()
			time.sleep(0.2)
			ding.play()
		else:
			hit.play()
	y.currentHP = (y.currentHP - damagedealt) ##put at the end of all ability checks since the damage dealt have been calculated properly##
	if damagedealt >= y.currentHP:
		y.currentHP = 0
		defeat(y)
	if y.currentHP > damagedealt:
		damagereceived = (y.Atk - x.Def)
		if damagereceived <= 0:
			ding.play()
		else:
			hit.play()
		x.currentHP = (x.currentHP - damagereceived)
		if damagereceived >= x.currentHP:
			defeat(x)
	x.attackstate = False

def move(u, x, y, column, row): ##u for unit self value, x for column, y for row##
	movement = u.Mov
	while movement > 0 and u.UnitType == 'player':
		highlight(u, x, y, column, row)
		for event in pygame.event.get():
			if event.type == pygame.KEYDOWN:
				if event.key == pygame.K_UP:
					y -= 1
					u.position = (column[x], row[y])
				if event.key == pygame.K_DOWN:
					y += 1
					u.position = (column[x], row[y])
				if event.key == pygame.K_LEFT:
					x -= 1
					u.position = (column[x], row[y])
				if event.key == pygame.K_RIGHT:
					x += 1
					u.position = (column[x], row[y])
				if event.key == pygame.K_RETURN:
					u.movestate = False
	movement -= 1
	if movement == 0:
		u.movestate = False

def healing(x):
	heal = pygame.mixer.Sound('Assets/Se_btl_cure1.wav')
	heal.set_volume(0.2)
	if x.currentHP < (x.HP - 10):
		x.currentHP += 10
		heal.play()
	if (x.currentHP + 10) >= x.HP:
		x.currentHP = x.HP
		heal.play()