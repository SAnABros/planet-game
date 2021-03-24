import pygame
import random
from math import sin,cos,degrees
screen = pygame.Vector2(600, 600)
sc = pygame.display.set_mode((int(screen.x),int(screen.y)))
screen = pygame.Vector2(sc.get_width(), sc.get_height())

planet = pygame.image.load('texture/planet.png').convert_alpha()
planet = pygame.transform.scale(planet, (60,60))
moon = pygame.image.load('texture/moon.png').convert_alpha()
moon = pygame.transform.scale(moon, (25,25))

class Asteroid():
	def __init__(self, image, pos):
		self.image = pygame.image.load(image).convert_alpha()
		self.image = pygame.transform.scale(self.image,(self.image.get_width()*3, self.image.get_height()*3)) if '1' in image else pygame.transform.scale(self.image,(self.image.get_width()*2, self.image.get_height()*2))
		self.x, self.y = pos
		self.rotate = 0
		self.dist = 0

asteroid = [Asteroid('texture/asteroid1.png', (random.randint(0,1)*screen.x, random.randint(0,1)*screen.y)),
			Asteroid('texture/asteroid1.png', (random.randint(0,1)*screen.x, random.randint(0,1)*screen.y))]
for i in range(10):
	asteroid.append(Asteroid('texture/asteroid1.png', (random.randint(0,1)*screen.x, random.randint(0,1)*screen.y)))
class BOOM():
	particles = []
	@staticmethod
	def new(x, y, min, max, count_particle):
		for i in range(count_particle):
			BOOM.particles.append([[x,y], [random.randint(min, max)/10, random.randint(min,max)/10], random.randint(4,6)])
	@staticmethod
	def draw():
		if len(BOOM.particles)>100:
			del BOOM.particles[99:len(BOOM.particles)-1]
		for particle in BOOM.particles:
			particle[0][0] += particle[1][0]*(random.randint(100,5000)/1000)
			particle[0][1] += particle[1][1]*(random.randint(100,5000)/1000)
			particle[2] -= 0.1
			pygame.draw.rect(sc, (random.randint(170, 230), random.randint(70, 130), random.randint(0, 50)), (particle[0], (particle[2], particle[2])))
			if particle[2]<=0:
				BOOM.particles.remove(particle)
planetLifes = 10
direction = 0 #planet direction
Mdir = 0 #moon direction
seed = random.randint(0,1000)
shift = pygame.Vector2(0,0)
clock = pygame.time.Clock()
while True:
	FPS = clock.tick()
	for event in pygame.event.get():
		if event.type == pygame.QUIT or (event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE):
			from sys import exit
			exit()
			pygame.quit()
	key = pygame.key.get_pressed()
	if key[pygame.K_ESCAPE]:
		gameON = False
	sc.fill((10,10,10))

	random.seed(seed)
	for i in range(0,int(screen.x/3)):
		pygame.draw.circle(sc, (255,255,255), (random.randint(0,screen.x)+shift.x, random.randint(0,screen.y)+shift.y), 1)

	rotateSpeed = (pygame.mouse.get_pressed()[0] - pygame.mouse.get_pressed()[2])*10

	plan = pygame.transform.rotate(planet, direction)
	sc.blit(plan, (screen.x/2-plan.get_width()/2+shift.x, screen.y/2-plan.get_height()/2+shift.y))

	Mpos = pygame.Vector2(cos(Mdir)*50, sin(Mdir)*50)
	Moon = pygame.transform.rotate(moon, 180-degrees(Mdir))
	sc.blit(Moon, (screen.x/2+Mpos.x-Moon.get_width()/2+shift.x, screen.y/2+Mpos.y-Moon.get_height()/2+shift.y))

	from math import hypot
	for asteroid1 in asteroid:
		asteroid1.dist = hypot(screen.x/2-asteroid1.x, screen.y/2-asteroid1.y)
		asteroid1.x += (screen.x/2-asteroid1.x)/asteroid1.dist*FPS/10
		asteroid1.y += (screen.y/2-asteroid1.y)/asteroid1.dist*FPS/10
		astr = pygame.transform.rotate(asteroid1.image, asteroid1.rotate)
		asteroid1.rotate += FPS/10
		sc.blit(astr, (asteroid1.x-astr.get_width()/2+shift.x, asteroid1.y-astr.get_height()/2+shift.y))
		MoonRect = pygame.Rect(screen.x/2+Mpos.x-Moon.get_width()/2, screen.y/2+Mpos.y-Moon.get_height()/2, Moon.get_width(), Moon.get_height())
		AsteroidRect = pygame.Rect((asteroid1.x-asteroid1.image.get_width()/2, asteroid1.y-asteroid1.image.get_height()/2), asteroid1.image.get_rect().size)
		from time import time
		random.seed(time())
		if MoonRect.colliderect(AsteroidRect):
			asteroid.remove(asteroid1)
			shift.x = random.randint(-5,5)
			shift.y = random.randint(-5,5)
			BOOM.new(asteroid1.x, asteroid1.y, -10, 10, random.randint(20,40))
			for i in range(random.randint(1,2)):
				if random.randint(-100,100)>=0:
					asteroid.append(Asteroid('texture/asteroid'+str(random.randint(1,3))+'.png', (random.randint(0,1)*screen.x, random.randint(0,screen.y))))
				else:
					asteroid.append(Asteroid('texture/asteroid'+str(random.randint(1,3))+'.png', (random.randint(0,screen.x), random.randint(0,1)*screen.y)))
			planetLifes += 0.25
		if AsteroidRect.colliderect((screen.x/2-plan.get_width()/2, screen.y/2-plan.get_height()/2), plan.get_rect().size):
			if asteroid1 in asteroid:
				planetLifes -= 1
				asteroid.remove(asteroid1)
				BOOM.new(asteroid1.x, asteroid1.y, -15.0, 15.0, random.randint(80,100))
				if random.randint(-100,100)>=0:
					asteroid.append(Asteroid('texture/asteroid'+str(random.randint(1,3))+'.png', (random.randint(0,1)*screen.x, random.randint(0,screen.y))))
				else:
					asteroid.append(Asteroid('texture/asteroid'+str(random.randint(1,3))+'.png', (random.randint(0,screen.x), random.randint(0,1)*screen.y)))
				shift.x = random.randint(-15,15)
				shift.y = random.randint(-15,15)
	if planetLifes<=0:
		pygame.time.wait(250)
		planetLifes = 10
		seed = random.randint(0,1000)
		asteroid = [Asteroid('texture/asteroid'+str(random.randint(1,3))+'.png', (random.randint(0,1)*screen.x, random.randint(0,1)*screen.y)),
					Asteroid('texture/asteroid'+str(random.randint(1,3))+'.png', (random.randint(0,1)*screen.x, random.randint(0,1)*screen.y))]
	shift.x /= -4
	shift.y /= -4
	BOOM.draw()
	pygame.draw.rect(sc, (0,200,0), [screen.x/2-50+shift.x, screen.y/2+planet.get_height(), planetLifes*10+shift.y, 10])
	pygame.draw.rect(sc, (0,0,0), [screen.x/2-50+shift.x, screen.y/2+planet.get_height()+shift.y, 100, 10], 4)
	pygame.display.update()
	direction += 2*rotateSpeed*FPS/10 if rotateSpeed else 2*FPS/10
	Mdir -= rotateSpeed*3.14/180*FPS/10 if rotateSpeed else 3.14/180*FPS/10
	pygame.display.set_caption(str(1000//FPS)) if FPS else pygame.display.set_caption('0')
