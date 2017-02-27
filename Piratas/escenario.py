import pygame
from pygame.locals import *
from escena import *
from gestorRecursos import *
from miSprite import *
# -------------------------------------------------
# Clase Plataforma

#class Plataforma(pygame.sprite.Sprite):
class Plataforma(MiSprite):
	def __init__(self,rectangulo):
		# Primero invocamos al constructor de la clase padre
		MiSprite.__init__(self)
		# Rectangulo con las coordenadas en pantalla que ocupara
		self.rect = rectangulo
		# Y lo situamos de forma global en esas coordenadas
		self.establecerPosicion((self.rect.left, self.rect.bottom))
		# En el caso particular de este juego, las plataformas no se van a ver, asi que no se carga ninguna imagen
		self.image = pygame.Surface((0, 0))

	def draw(self, pantalla):
		#pantalla.blit(self.image, self.rect, (10,10))
		pygame.draw.rect(pantalla,(255,255,255), self.rect)


# -------------------------------------------------

class StaticScenario(pygame.sprite.Sprite):
	def __init__(self,file,scrollspeed=(1,1)):
		pygame.sprite.Sprite.__init__(self)
		self.image = GestorRecursos.CargarImagen(file,-1)
		self.image = pygame.transform.scale(self.image, (self.image.get_size()[0], ALTO_PANTALLA))

		self.rect = self.image.get_rect()
		self.rect.bottom = ALTO_PANTALLA
		self.rectSubimage = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
		self.rectSubimage.left = 0
		self.rectSubimage.top = 0
		self.scrollspeed = scrollspeed

	def update(self, tiempo):
		"Nothing"

	def establecerPosicionPantalla(self, scroll):
		self.rectSubimage.left = scroll[0] * self.scrollspeed[0]
		self.rectSubimage.top =  scroll[1] * self.scrollspeed[1]

	def draw(self, pantalla):
		pantalla.blit(self.image, self.rect, self.rectSubimage)

class DynamicScenario(pygame.sprite.Sprite):
	def __init__(self,folder,frames,delay,scrollspeed=(1,1)):
		pygame.sprite.Sprite.__init__(self)
		self.gif = GestorRecursos.CargarGif(folder,frames,-1)
		self.image = self.gif[0]
		self.image = pygame.transform.scale(self.image, (self.image.get_size()[0], ALTO_PANTALLA))

		self.rect = self.image.get_rect()
		self.rect.bottom = ALTO_PANTALLA
		self.rectSubimage = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
		self.rectSubimage.left = 0
		self.rectSubimage.top = 0
		self.scrollspeed = scrollspeed

		self.gif_frame_max = frames - 1
		self.gif_frame = 0
		self.gif_asc = True
		self.time_stop = 2000
		self.time = -self.time_stop

	def update(self, tiempo):
		self.time += tiempo
		if(self.time > 100):
			self.time = 0
			if(self.gif_asc):
				if(self.gif_frame < self.gif_frame_max):
					self.gif_frame += 1
				else:
					self.gif_asc = False
					self.time = -self.time_stop
			else:
				if(self.gif_frame > 0):
					self.gif_frame -= 1
				else:
					self.gif_asc = True
					self.time = -self.time_stop
			print(self.gif_frame)
			self.image = self.gif[self.gif_frame]



	def establecerPosicionPantalla(self, scroll):
		self.rectSubimage.left = scroll[0] * self.scrollspeed[0]
		self.rectSubimage.top =  scroll[1] * self.scrollspeed[1]

	def draw(self, pantalla):
		pantalla.blit(self.image, self.rect, self.rectSubimage)