import pygame
from pygame.locals import *

from rt import RayTracer
from figures import *
from lights import *
from materials import *


width = 256
height = 256

pygame.init()

screen = pygame.display.set_mode((width,height),pygame.DOUBLEBUF|pygame.HWACCEL|pygame.HWSURFACE)
screen.set_alpha(None)

raytracer = RayTracer(screen)
raytracer.envMap = pygame.image.load("textures/utopia.bmp")
raytracer.rtClearColor(0.25,0.25,0.25)

marsTexture = pygame.image.load("textures/mars.bmp")

brick = Material(diffuse=(1,0.4,0.4),spec=8,Ks=0.01)
grass = Material(diffuse=(0.4,1,0.4),spec=32,Ks=0.1)
water = Material(diffuse=(0.4,0.4,1),spec=256,Ks=0.2, matType=OPAQUE)
mars = Material(texture = marsTexture,spec=64,Ks=0.1,matType=OPAQUE)
mirror = Material(diffuse=(0.9,0.9,0.9),spec=64,Ks=0.2,matType=REFLECTIVE)
blueMirror = Material(diffuse=(0.4,0.4,0.9),spec=32,Ks=0.15,matType=REFLECTIVE)
redMirror = Material(diffuse=(0.9,0.9,0.9),spec=64,Ks=0.2,matType=TRANSPARENT)
greenMirror = Material(diffuse=(0.9,0.9,0.9),spec=64,Ks=0.2,matType=TRANSPARENT)


raytracer.scene.append(Sphere(position=(-2,2,-5),radius=0.8,material=mirror))
raytracer.scene.append(Sphere(position=(2,2,-5),radius=0.8,material=mars))
raytracer.scene.append(Sphere(position=(0,2,-5),radius=0.8,material=blueMirror))
raytracer.scene.append(Sphere(position=(0,0,-5),radius=0.8,material=water))
raytracer.scene.append(Sphere(position=(-2,0,-5),radius=0.8,material=brick))
raytracer.scene.append(Sphere(position=(2,0,-5),radius=0.8,material=grass))

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