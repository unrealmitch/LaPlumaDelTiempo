# -*- coding: utf-8 -*-

import pygame, escena
from escena import *
from personajes import *
from pygame.locals import *
import random,math


# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

# Los bordes de la pantalla para hacer scroll horizontal
MINIMO_X_JUGADOR = ANCHO_PANTALLA  / 4
MAXIMO_X_JUGADOR = ANCHO_PANTALLA - MINIMO_X_JUGADOR

# -------------------------------------------------
# Clase Fase

class Fase(Escena):
	def __init__(self, director):

		# Habria que pasarle como parámetro el número de fase, a partir del cual se cargue
		#   - Nombre del archivo con el decorado
		#   - Posiciones de las plataformas
		#   - Posiciones de los enemigos
		#   - Posiciones de inicio de los jugadores
		#  etc.
		# Y cargar esa configuracion del archivo en lugar de ponerla a mano, como aqui abajo
		# De esta forma, se podrian tener muchas fases distintas con esta clase

		# Primero invocamos al constructor de la clase padre
		Escena.__init__(self, director)

		fH = ALTO_PANTALLA/800.	#!Factor de escala Y, para posicionar bien en este eje si se escala el decorado

		# Creamos el decorado y el fondo
		self.decorado = Decorado()
		self.sea = Sea()

		# Que parte del decorado estamos visualizando
		self.scrollx = 0
		self.scrolly = 0.
		self.scrolly_speed = 0.01	#!Velocidad scroll Vertial

		# Creamos los sprites de los jugadores
		self.jugador1 = Jugador()
		self.grupoJugadores = pygame.sprite.Group( self.jugador1 )

		# Ponemos a los jugadores en sus posiciones iniciales
		self.jugador1.establecerPosicion((300, fH*555))

		#! Creamos las plataformas del decorado cargando un fichero de configuracióm
		file_plataformas = GestorRecursos.CargarMapaPlataformas("plat-piratas.txt")
		plataformas = []
		self.grupoPlataformas = pygame.sprite.Group()

		for elem in file_plataformas:
			self.grupoPlataformas.add(Plataforma(pygame.Rect(elem[0], fH*elem[1], elem[2], elem[3])))

		# Y los enemigos que tendran en este decorado
		#enemigo1 = Sniper()
		#enemigo1.establecerPosicion((1000, 418))

		# Creamos un grupo con los enemigos
		#self.grupoEnemigos = pygame.sprite.Group( enemigo1 )

		self.barcobg1 = BarcoBg(100,275)

		self.grupoEscenario = pygame.sprite.Group(self.barcobg1)
		# Creamos un grupo con los Sprites que se mueven
		#  En este caso, solo los personajes, pero podría haber más (proyectiles, etc.)
		self.grupoSpritesDinamicos = pygame.sprite.Group( self.jugador1 )
		self.grupoSpritesDinamicos.add()
		# Creamos otro grupo con todos los Sprites
		self.grupoSprites = pygame.sprite.Group( self.jugador1 )
		self.grupoSprites.add(self.grupoPlataformas)

	# Devuelve True o False según se ha tenido que desplazar el scroll
	def actualizarScrollOrdenados(self, jugador):
		# Si el jugador de la izquierda se encuentra más allá del borde izquierdo
		if (jugador.rect.left<MINIMO_X_JUGADOR):
			desplazamiento = MINIMO_X_JUGADOR - jugador.rect.left

			# Si el escenario ya está a la izquierda del todo, no lo movemos mas
			if self.scrollx <= 0:
				self.scrollx = 0

				# En su lugar, colocamos al jugador que esté más a la izquierda a la izquierda de todo
				jugador.establecerPosicion((MINIMO_X_JUGADOR, jugador.posicion[1]))
				return False; # No se ha actualizado el scroll
			else:
				# Calculamos el nivel de scroll actual: el anterior - desplazamiento
				#  (desplazamos a la izquierda)
				self.scrollx = self.scrollx - desplazamiento;

				return True; # Se ha actualizado el scroll

		# Si el jugador de la derecha se encuentra más allá del borde derecho
		if (jugador.rect.right>MAXIMO_X_JUGADOR):

			# Se calcula cuantos pixeles esta fuera del borde
			desplazamiento = jugador.rect.right - MAXIMO_X_JUGADOR

			# Si el escenario ya está a la derecha del todo, no lo movemos mas
			if self.scrollx + ANCHO_PANTALLA >= self.decorado.rect.right:
				self.scrollx = self.decorado.rect.right - ANCHO_PANTALLA

				# En su lugar, colocamos al jugador que esté más a la derecha a la derecha de todo
				jugador.establecerPosicion((self.scrollx+MAXIMO_X_JUGADOR-jugador.rect.width, jugador.posicion[1]))

				return False; # No se ha actualizado el scroll

			else:

				# Calculamos el nivel de scroll actual: el anterior + desplazamiento
				#  (desplazamos a la derecha)
				self.scrollx = self.scrollx + desplazamiento;

				return True; # Se ha actualizado el scroll

		# Si ambos jugadores están entre los dos límites de la pantalla, no se hace nada
		return False;


	def actualizarScroll(self, jugador):
		if (self.scrolly > 1 or self.scrolly < 0):
			self.scrolly_speed = -self.scrolly_speed

		self.scrolly += self.scrolly_speed
		actual_scrolly = math.sin(self.scrolly) * 30
		# Se ordenan los jugadores según el eje x, y se mira si hay que actualizar el scroll
		cambioScroll = self.actualizarScrollOrdenados(jugador)

		for sprite in iter(self.grupoSprites):
			sprite.establecerPosicionPantalla((self.scrollx, actual_scrolly))

		# Si se cambio el scroll, se desplazan todos los Sprites y el decorado
		if cambioScroll:
			# Actualizamos la posición en pantalla de todos los Sprites según el scroll actual
			for sprite in iter(self.grupoSprites):
				sprite.establecerPosicionPantalla((self.scrollx, actual_scrolly))

			# Ademas, actualizamos el decorado para que se muestre una parte distinta
			self.sea.update(self.scrollx/2.562)

		self.decorado.update(self.scrollx,actual_scrolly)

	# Se actualiza el decorado, realizando las siguientes acciones:
	#  Se indica para los personajes no jugadores qué movimiento desean realizar según su IA
	#  Se mueven los sprites dinámicos, todos a la vez
	#  Se comprueba si hay colision entre algun jugador y algun enemigo
	#  Se comprueba si algún jugador ha salido de la pantalla, y se actualiza el scroll en consecuencia
	#     Actualizar el scroll implica tener que desplazar todos los sprites por pantalla
	#  Se actualiza la posicion del sol y el color del cielo
	def update(self, tiempo):
		# Primero, se indican las acciones que van a hacer los enemigos segun como esten los jugadores
		#for enemigo in iter(self.grupoEnemigos):
		#    enemigo.mover_cpu(self.jugador1, self.jugador2)
		# Esta operación es aplicable también a cualquier Sprite que tenga algún tipo de IA
		# En el caso de los jugadores, esto ya se ha realizado

		# Actualizamos los Sprites dinamicos
		# De esta forma, se simula que cambian todos a la vez
		# Esta operación de update ya comprueba que los movimientos sean correctos
		#  y, si lo son, realiza el movimiento de los Sprites
		self.grupoSpritesDinamicos.update(self.grupoPlataformas, tiempo)
		# Dentro del update ya se comprueba que todos los movimientos son válidos
		#  (que no choque con paredes, etc.)

		# Los Sprites que no se mueven no hace falta actualizarlos,
		#  si se actualiza el scroll, sus posiciones en pantalla se actualizan más abajo
		# En cambio, sí haría falta actualizar los Sprites que no se mueven pero que tienen que
		#  mostrar alguna animación

		# Comprobamos si hay colision entre algun jugador y algun enemigo
		# Se comprueba la colision entre ambos grupos
		# Si la hay, indicamos que se ha finalizado la fase
		#if pygame.sprite.groupcollide(self.grupoJugadores, self.grupoEnemigos, False, False)!={}:
			# Se le dice al director que salga de esta escena y ejecute la siguiente en la pila
		#    self.director.salirEscena()

		# Actualizamos el scroll
		self.actualizarScroll(self.jugador1)
  
		# Actualizamos el fondo:
		#  la posicion del sol y el color del cielo
		self.barcobg1.update(tiempo, self.scrollx/2.562)
		
	def dibujar(self, pantalla):
		# Ponemos primero el fondo
		# Despues, las animaciones que haya detras
		#for animacion in self.animacionesDetras:
		#    animacion.dibujar(pantalla)
		# Después el decorado
		self.sea.dibujar(pantalla)
		self.barcobg1.draw(pantalla)
		self.decorado.dibujar(pantalla)
		# Luego los Sprites
		self.grupoSprites.draw(pantalla)

		for elem in self.grupoPlataformas.sprites():
			elem.draw(pantalla)
		# Y por ultimo, dibujamos las animaciones por encima del decorado
		#for animacion in self.animacionesDelante:
		#    animacion.dibujar(pantalla)


	def eventos(self, lista_eventos):
		# Miramos a ver si hay algun evento de salir del programa
		for evento in lista_eventos:
			# Si se quiere salir, se le indica al director
			if evento.type == pygame.QUIT:
				self.director.salirPrograma()

		# Indicamos la acción a realizar segun la tecla pulsada para cada jugador
		teclasPulsadas = pygame.key.get_pressed()
		self.jugador1.mover(teclasPulsadas, K_UP, K_DOWN, K_LEFT, K_RIGHT)

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
# Clase BarcoBg

class BarcoBg(MiSprite):
	def __init__(self,x,y):
		MiSprite.__init__(self)
		self.imagen = GestorRecursos.CargarImagen('pirate-ship1.png', -1)
		self.image = self.imagen
		#self.image = pygame.transform.scale(self.image,(150,150))
		self.size = self.image.get_size()
		self.rect = self.image.get_rect()
		self.rect.left = x
		self.rect.top = y
		self.scrollx = 0
		self.scrolly = 10

	def update(self,tiempo, scrollx):
		'''
		self.scrollx += 0.8
		self.scrolly += 0.001
		self.rect.left = self.scrollx - scrollx
		self.rect.top = 0
		size = int(self.scrolly*50)
		self.image = pygame.transform.scale(self.imagen,(size,size))
		'''
		self.scrollx += 0.8
		self.scrolly += 0.01
		self.rect.left = self.scrollx - scrollx
		self.rect.top = 275 + self.scrolly/10
		size = int(self.scrolly*self.scrolly)
		self.image = pygame.transform.scale(self.imagen,(size,size))

	def draw(self, pantalla):
		pantalla.blit(self.image, self.rect)

# -------------------------------------------------
# Clase Sea
class Sea:
	def __init__(self):
		self.imagen = GestorRecursos.CargarImagen('Fondo.png')
		self.imagen = pygame.transform.scale(self.imagen, (2798, ALTO_PANTALLA))

		self.rect = self.imagen.get_rect()
		self.rect.bottom = ALTO_PANTALLA

		# La subimagen que estamos viendo
		self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
		self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto


	def update(self, scrollx):
		self.rectSubimagen.left = scrollx

	def dibujar(self, pantalla):
		pantalla.blit(self.imagen, self.rect, self.rectSubimagen)
		

# Clase Decorado

class Decorado:
	def __init__(self):
		self.imagen = GestorRecursos.CargarImagen('barco.png', -1)
		self.imagen = pygame.transform.scale(self.imagen, (7168, ALTO_PANTALLA))

		self.rect = self.imagen.get_rect()
		self.rect.bottom = ALTO_PANTALLA

		# La subimagen que estamos viendo
		self.rectSubimagen = pygame.Rect(0, 0, ANCHO_PANTALLA, ALTO_PANTALLA)
		self.rectSubimagen.left = 0 # El scroll horizontal empieza en la posicion 0 por defecto
		self.rectSubimagen.top = 0

	def update(self, scrollx,scrolly=0):
		self.rectSubimagen.left = scrollx
		self.rectSubimagen.top = scrolly

	def dibujar(self, pantalla):
		pantalla.blit(self.imagen, self.rect, self.rectSubimagen)