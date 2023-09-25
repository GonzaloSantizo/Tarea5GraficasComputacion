import pygame
from pygame.locals import *
from rt import Raytracer
from figures import *
from lights import *
from materials import *

width = 256
height = 256

pygame.init()

screen = pygame.display.set_mode((width, height), pygame.DOUBLEBUF | pygame.HWACCEL | pygame.HWSURFACE)
screen.set_alpha(None)

raytracer = Raytracer(screen)
raytracer.rtClearColor(0.25,0.25,0.25)

brick = Material(diffuse = (1, 0.4, 0.4), spec = 8)
grass = Material(diffuse = (0.4, 1, 0.4), spec = 32)
water = Material(diffuse = (0.4, 0.4, 1), spec = 256)
Snow = Material(diffuse = (1,1,1), spec = 8)
Coal = Material(diffuse = (0,0,0), spec = 8)
Carrot = Material(diffuse = (1, 0.65, 0), spec = 8)


#Body
raytracer.scene.append(Sphere(position=(2,2,-5), radius = 0.5, material=brick))
raytracer.scene.append(Sphere(position=(0,0,-7), radius = 1, material=brick))


raytracer.lights.append(AmbientLight(intensity = 0.1))
raytracer.lights.append(DirectionalLight(direction=(-1,-1,-1), intensity = 0.7))
raytracer.lights.append(PointLight(point = (5, 0, -5), intensity = 0.5, color = (1,0,1)))

isRunning = True
while isRunning:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            isRunning = False
        elif event.type == pygame.KEYDOWN:
            if event.KEY == pygame.K_ESCAPE:
                isRunning == False
    
    raytracer.rtClear()



    raytracer.rtRender()    
    pygame.display.flip()

pygame.quit()