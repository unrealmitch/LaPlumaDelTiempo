import pygame

from miSprite import *
from pygame.locals import *

class Gui(MiSprite):

	def __init__(self, vidas=6, tipo=1):
		# Primero invocamos al constructor de la clase padre
		MiSprite.__init__(self)

		self.vida = vidas
		self.tipo = tipo

		self.velocidad = 1
		self.salto = 1
		self.ataque = 1

		if tipo == 0:
			self.hoja = GestorRecursos.CargarImagen("gui_lifebar.png",-1)
			self.hoja = self.hoja.convert_alpha()
			datos = GestorRecursos.CargarArchivoCoordenadas("gui_lifebar.txt")
			datos = datos.split()

			cont = 0
			
			self.coordenadasHoja = [];
			self.coordenadasHoja.append([])
			tmp = self.coordenadasHoja[0]
			for postura in range(1, 7+1):
				tmp.append(pygame.Rect((int(int(datos[cont])*ESCALA), int(int(datos[cont+1])*ESCALA)), (int(int(datos[cont+2])*ESCALA), int(int(datos[cont+3])*ESCALA))))
				cont += 4

			# El rectangulo del Sprite
			self.rect = pygame.Rect(0,20,self.coordenadasHoja[0][6][2],self.coordenadasHoja[0][6][3])

			self.image = self.hoja.subsurface(self.coordenadasHoja[0][6])
			x,y=self.image.get_size()
			self.image = pygame.transform.scale(self.image,(int(x*0.7), int(y*0.7)))
		else:
			self.corazon = GestorRecursos.CargarImagen("gui_corazon.png",-1)
			self.death =  GestorRecursos.CargarImagen("gui_death.png",-1)
			x,y=self.corazon.get_size()

			self.corazon = pygame.transform.scale(self.corazon,(int(x*0.3*ESCALA), int(y*0.3*ESCALA)))
			self.death = pygame.transform.scale(self.death,(int(x*0.3*ESCALA), int(y*0.3*ESCALA)))
			self.rect = self.corazon.get_rect()

			self.espada = GestorRecursos.CargarImagen("gui_espada.png",-1)
			self.botas = GestorRecursos.CargarImagen("gui_botas.png",-1)
			self.muelle = GestorRecursos.CargarImagen("gui_muelle.png",-1)



	def actualizarVida(self, vida):

		if self.tipo == 0:
			if vida > 6: vida = 6
			self.rect = pygame.Rect(0,20,self.coordenadasHoja[0][vida][2],self.coordenadasHoja[0][vida][3])
			self.image = self.hoja.subsurface(self.coordenadasHoja[0][vida])
			x,y=self.image.get_size()
			self.image = pygame.transform.scale(self.image,(int(x*0.7), int(y*0.7)))
		else:
			self.vida = vida

	def actualizarPsj(self, personaje):
		self.velocidad = int(personaje.velocidadCarrera*100-24)
		self.salto = int(personaje.velocidadSalto*100-29)
		self.ataque = personaje.ataque

	def draw(self,pantalla):
		if self.tipo == 0:
			MiSprite.draw(self, pantalla)
		else:
			if self.vida == 0:
				pantalla.blit(self.death, (30*ESCALA, ALTO_PANTALLA*0.9))
			else:
				for i in range(self.vida):
					pantalla.blit(self.corazon, (30*ESCALA + (self.rect.width+15*ESCALA)*i,ALTO_PANTALLA*0.9))

				pantalla.blit(self.espada, (0, 20))
				pantalla.blit(self.botas, (20, 70))
				pantalla.blit(self.muelle, (20, 135))

				tipoLetra = GestorRecursos.CargarFuente('menu_font_space_age.ttf', 50)
				texto1 = tipoLetra.render(str(self.ataque), True, (255,255,255))
				texto2 = tipoLetra.render(str(self.velocidad), True, (255,255,255))
				texto3 = tipoLetra.render(str(self.salto), True, (255,255,255))

				pantalla.blit(texto1, (120, 20))
				pantalla.blit(texto2, (120, 80))
				pantalla.blit(texto3, (120, 150))




