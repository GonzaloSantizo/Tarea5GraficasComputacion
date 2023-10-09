import pygame
from pygame.locals import *

from rt import RayTracer
from figures import *
from lights import *
from materials import *


width = 512
height = 512

pygame.init()

screen = pygame.display.set_mode((width,height),pygame.DOUBLEBUF|pygame.HWACCEL|pygame.HWSURFACE)
screen.set_alpha(None)

raytracer = RayTracer(screen)
raytracer.envMap = pygame.image.load("textures/utopia.bmp")
raytracer.rtClearColor(0.25,0.25,0.25)

marsTexture = pygame.image.load("textures/mars.bmp")

brick = Material(diffuse=(1,0.4,0.4),spec=8,Ks=0.01)
grass = Material(diffuse=(0.4,1,0.4),spec=32,Ks=0.1)
water = Material(diffuse=(0.4,0.4,1),spec=256,Ks=0.2)
mirror = Material(diffuse=(0.9,0.9,0.9),spec=64,Ks=0.2,matType=REFLECTIVE)
blueMirror = Material(diffuse=(0.4,0.4,0.9),spec=32,Ks=0.15,matType=REFLECTIVE)
earth = Material(texture = marsTexture,spec=64,Ks=0.1,matType=REFLECTIVE)

 
#paredes
raytracer.scene.append(Plane(position=(0,-5,-5),normal=(0,1,0),material=water))
raytracer.scene.append(Plane(position=(0,5,-5),normal=(0,-1,0),material=grass))
raytracer.scene.append(Plane(position=(0,0,-10),normal=(0,0,1),material=brick))
raytracer.scene.append(Plane(position=(-5,0,-5),normal=(1,0,0),material=water))


#objetos
raytracer.scene.append(Disk(position=(0,-1.5,-5),normal=(0,1,0),radius=1.5,material=water))
raytracer.scene.append(AABB(position=(1.5,1.5,-5),size=(1,1,1),material=water))
raytracer.scene.append(AABB(position=(-1.5,1.5,-5),size=(1,1,1),material=water))


raytracer.lights.append(AmbientLight(intensity=0.1))
raytracer.lights.append(DirectionalLight(direction=(-1,-1,-1),intensity=0.9))
#raytracer.lights.append(PointLight(point=(1.5,0,-5),intensity=1,color=(1,0,1)))

raytracer.rtClear()
raytracer.rtRender()

print("\nRender Time:",pygame.time.get_ticks()/1000,"secs")

isRunning = True
while isRunning:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			isRunning = False
		elif event.type == pygame.KEYDOWN:
			if event.key == pygame.K_ESCAPE:
				isRunning = False

pygame.quit()