import mt
import numpy as np

from math import acos,asin

def reflectVector(normal,direction):
    reflect = 2*mt.producto_punto(normal,direction)
    reflect = mt.multiply_scalar_array(reflect,normal)
    reflect = mt.subtract_arrays(reflect,direction)
    reflect = mt.normalizar_vector(reflect)
    
    return reflect

def refractVector(incident,normal,n1,n2):
    #Snell's Law
    refract = np.multiply(np.dot(incident,normal),normal)
    refract = np.subtract(incident,refract)
    refract = n1*refract
    refract = refract/n2
    refract = refract/np.linalg.norm(refract)
    return refract

def totalInternalReflection(incident,normal,n1,n2):
    if n1<n2:
        n1,n2=n2,n1
        
    Ai = acos(np.dot(incident,normal))
    Ac = asin(n2/n1)
    
    return Ai>=Ac

def fresnel(n1,n2):
    Kr = ((n1**0.5-n2**0.5)**2/((n1**0.5+n2**0.5)))    

class Light(object):
    def __init__(self,intensity=1,color=(1,1,1),lightType="None"):
        self.intensity = intensity
        self.color = color
        self.lightType = lightType
        
    def getLightColor(self):
        return [self.color[0]*self.intensity,
                self.color[1]*self.intensity,
                self.color[2]*self.intensity]
    
    def getDiffuseColor(self,intercept):
        return None
    
    def getSpecularColor(self,intercept,viewPos):
        return None
    
class AmbientLight(Light):
    def __init__(self,intensity=1,color=(1,1,1)):
        super().__init__(intensity,color,"Ambient")
        
class DirectionalLight(Light):
    def __init__(self, direction=(0,-1,0),intensity=1, color=(1, 1, 1)):
        self.direction=mt.normalizar_vector(direction)
        super().__init__(intensity, color,"Directional")
        
    def getDiffuseColor(self,intercept):
        dir = [(i*-1) for i in self.direction]
        
        intensity = mt.producto_punto(intercept.normal,dir)*self.intensity
        intensity = max(0,min(1,intensity))
        intensity *= 1-intercept.obj.material.Ks
        diffuseColor = [(i*intensity) for i in self.color]
        
        return diffuseColor
    
    def getSpecularColor(self, intercept, viewPos):
        dir = [(i*-1) for i in self.direction]
        
        reflect = reflectVector(intercept.normal,dir)
        
        viewDir = mt.subtract_arrays(viewPos,intercept.point)
        viewDir = mt.normalizar_vector(viewDir)
        
        specIntensity = max(0,mt.producto_punto(viewDir,reflect))**intercept.obj.material.spec
        specIntensity *= intercept.obj.material.Ks
        specIntensity *= self.intensity
        
        specColor = [(i*specIntensity) for i in self.color]
        
        return specColor
    
class PointLight(Light):
    def __init__(self, point=(0,0,0),intensity=1, color=(1, 1, 1)):
        self.point = point
        super().__init__(intensity, color, "Point")
        
    def getDiffuseColor(self, intercept):
        dir = mt.subtract_arrays(self.point,intercept.point)
        R = mt.calcular_norma(dir)
        dir = mt.divide_array_scalar(dir,R)
        
        intensity = mt.producto_punto(intercept.normal,dir)*self.intensity
        intensity *= 1-intercept.obj.material.Ks
        
        #Ley de cuadrados inversos
        # IF = Intensity/R^2
        #R es la distancia del punto intercepto a la luz punto
        if R!=0:
            intensity /= R**2
        
        intensity = max(0,min(1,intensity))

        diffuseColor = [(i*intensity) for i in self.color]
        
        return diffuseColor
    
    def getSpecularColor(self, intercept, viewPos):
        dir = mt.subtract_arrays(self.point,intercept.point)
        R = mt.calcular_norma(dir)
        dir = mt.divide_array_scalar(dir,R)
        
        reflect = reflectVector(intercept.normal,dir)
        
        viewDir = mt.subtract_arrays(viewPos,intercept.point)
        viewDir = mt.normalizar_vector(viewDir)
        
        specIntensity = max(0,mt.producto_punto(viewDir,reflect))**intercept.obj.material.spec
        specIntensity *= intercept.obj.material.Ks
        specIntensity *= self.intensity
        
        if R!=0:
            specIntensity /= R**2
        
        specIntensity = max(0,min(1,specIntensity))
        
        specColor = [(i*specIntensity) for i in self.color]
        
        return specColor