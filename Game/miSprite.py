import pygame, escena
from pygame.locals import *
from gestorRecursos import *

# -------------------------------------------------
# Clase MiSprite
class MiSprite(pygame.sprite.Sprite):
	"Los Sprites que tendra este juego"
	def __init__(self):
		pygame.sprite.Sprite.__init__(self)
		self.posicion = (0, 0)
		self.velocidad = (0, 0)
		self.scroll   = (0, 0)

	def establecerPosicion(self, posicion):
		self.posicion = posicion
		self.rect.left = int(self.posicion[0] - self.scroll[0]*ESCALA)
		self.rect.bottom = int(self.posicion[1]- self.scroll[1]*ESCALA)

	def establecerPosicionPantalla(self, scrollDecorado):
		self.scroll = (int(scrollDecorado[0]), int(scrollDecorado[1]*ESCALA));
		(scrollx, scrolly) = self.scroll;
		(posx, posy) = self.posicion;
		self.rect.left = int(posx - scrollx*ESCALA);
		self.rect.bottom = int(posy - scrolly*ESCALA);

	def incrementarPosicion(self, incremento):
		(posx, posy) = self.posicion
		(incrementox, incrementoy) = incremento
		self.establecerPosicion((posx+incrementox, posy+incrementoy))

	def update(self, tiempo):
		incrementox = self.velocidad[0]*ESCALA*tiempo
		incrementoy = self.velocidad[1]*ESCALA*tiempo
		self.incrementarPosicion((incrementox, incrementoy))


	def draw(self, pantalla):
		pantalla.blit(self.image, self.rect)


# -------------------------------------------------
# Clase autonomeSprite: Sprite with autonome movement and scale
# [move/scale]: [startX,startY,endX,endY,speedX,speedY]
class autonomeSprite(pygame.sprite.Sprite):
	def __init__(self,file,move,scale=(1,1,1,1,0,0),scrollspeed=(1.,1.)):
		pygame.sprite.Sprite.__init__(self)
		self.file = GestorRecursos.CargarImagenAlpha(file, -1)

		self.posicion = (move[0]*ESCALA, move[1]*ESCALA)
		self.pos_max = (move[2]*ESCALA, move[3]*ESCALA)
		self.pos_speed = (move[4]*ESCALA, move[5]*ESCALA)

		self.scale = (scale[0], scale[1])
		self.scale_max = (scale[2], scale[3])
		self.scale_speed = (scale[4], scale[5])

		self.scroll = (0,0)
		self.scrollspeed = (scrollspeed[0]*ESCALA, scrollspeed[1]*ESCALA)
		self.autoscale()
		self.establecerPosicion()

	def autoscale(self):
		dimensions = self.file.get_size()
		self.image = pygame.transform.scale(self.file,(int(dimensions[0]*self.scale[0]), int(dimensions[1]*self.scale[1])))
		self.rect = self.image.get_rect()

	def update(self,tiempo):
		posx = self.posicion[0] + self.pos_speed[0] * tiempo if self.posicion[0] < self.pos_max[0] else self.posicion[0]
		posy = self.posicion[1] + self.pos_speed[1] * tiempo if self.posicion[1] < self.pos_max[1] else self.posicion[1]

		self.posicion = (posx,posy)
		self.establecerPosicion()

		
		scalex = self.scale[0] + self.scale_speed[0] * tiempo if self.scale[0] < self.scale_max[0] else self.scale[0]
		scaley = self.scale[1] + self.scale_speed[1] * tiempo if self.scale[1] < self.scale_max[1] else self.scale[1]
		self.scale = (scalex,scaley)
		self.autoscale()

	def establecerPosicion(self):
		self.rect.left = self.posicion[0] - self.scroll[0]
		self.rect.top = self.posicion[1] - self.scroll[1]

	def establecerPosicionPantalla(self, scrollDecorado):
		self.scroll = scrollDecorado;
		(scrollx, scrolly) = self.scroll;
		(posx, posy) = self.posicion;
		self.rect.left = int(posx - scrollx*self.scrollspeed[0]);
		self.rect.top = int(posy - scrolly*self.scrollspeed[1]);

	def draw(self, pantalla):
		pantalla.blit(self.image, self.rect)

