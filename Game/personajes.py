# -*- coding: utf-8 -*-

import pygame, sys, os
from pygame.locals import *
from escena import *
from miSprite import *
from gestorRecursos import *

# -------------------------------------------------
# -------------------------------------------------
# Constantes
# -------------------------------------------------
# -------------------------------------------------

#Tipo Personaje
PLAYER = 0
EPIRATA1 = 1

# Movimientos
QUIETO = 0
IZQUIERDA = 1
DERECHA = 2
ARRIBA = 3
ABAJO = 4
ATAQUE1 = 5

#Posturas
P_QUIETO = 0
P_ANDANDO = 1
P_SALTANDO = 2
P_ATACANDO1 = 3
P_MURIENDO = 4

# Velocidades de los distintos personajes
VELOCIDAD_JUGADOR = 0.3 # Pixeles por milisegundo
VELOCIDAD_SALTO_JUGADOR = 0.3 # Pixeles por milisegundo
RETARDO_ANIMACION_JUGADOR = 1 # updates que durará cada imagen del personaje
							  # debería de ser un valor distinto para cada postura

VELOCIDAD_EPIRATA = 0.12 # Pixeles por milisegundo
VELOCIDAD_SALTO_EPIRATA = 0.27 # Pixeles por milisegundo
RETARDO_ANIMACION_EPIRATA = 1 # updates que durará cada imagen del personaje
							 # debería de ser un valor distinto para cada postura
# El Sniper camina un poco más lento que el jugador, y salta menos

GRAVEDAD = 0.0003 # Píxeles / ms2

# -------------------------------------------------
# -------------------------------------------------
# Clases de los objetos del juego
# -------------------------------------------------
# -------------------------------------------------


# -------------------------------------------------




# -------------------------------------------------
# Clases Personaje

#class Personaje(pygame.sprite.Sprite):
class Personaje(MiSprite):
	"Cualquier personaje del juego"

	# Parametros pasados al constructor de esta clase:
	#  Archivo con la hoja de Sprites
	#  Archivo con las coordenadoas dentro de la hoja
	#  Numero de imagenes en cada postura
	#  Velocidad de caminar y de salto
	#  Retardo para mostrar la animacion del personaje
	def __init__(self, tipo, archivoImagen, archivoCoordenadas, numImagenes, velocidadCarrera, velocidadSalto, retardoAnimacion, delayAtaque, vida):

		# Primero invocamos al constructor de la clase padre
		MiSprite.__init__(self);

		self.tipo = tipo
		# Se carga la hoja
		self.hoja = GestorRecursos.CargarImagen(archivoImagen,-1)
		self.hoja = self.hoja.convert_alpha()
		# El movimiento que esta realizando
		self.movimiento = QUIETO
		self.movimientos = {IZQUIERDA:False,DERECHA:False,ARRIBA:False,ABAJO:False,ATAQUE1:False}
		self.posturas = {P_QUIETO: True, P_ANDANDO: False, P_SALTANDO: False, P_ATACANDO1: False, P_MURIENDO:False}
		# Lado hacia el que esta mirando
		self.mirando = DERECHA

		#Ataques
		self.vida = vida
		self.ataque_clock = 0
		self.ataque_retardo = delayAtaque

		self.invulnerable_clock = 0
		self.invulnerable_delay = 400

		# Leemos las coordenadas de un archivo de texto
		datos = GestorRecursos.CargarArchivoCoordenadas(archivoCoordenadas)
		datos = datos.split()
		self.numPostura = 1;
		self.numImagenPostura = 0;
		cont = 0;
		self.coordenadasHoja = [];
		for linea in range(0, len(numImagenes)):
			self.coordenadasHoja.append([])
			tmp = self.coordenadasHoja[linea]
			for postura in range(1, numImagenes[linea]+1):
				tmp.append(pygame.Rect((int(int(datos[cont])*ESCALA), int(int(datos[cont+1])*ESCALA)), (int(int(datos[cont+2])*ESCALA), int(int(datos[cont+3])*ESCALA))))
				cont += 4

		# El retardo a la hora de cambiar la imagen del Sprite (para que no se mueva demasiado rápido)
		self.retardoMovimiento = 0;

		# En que postura esta inicialmente
		self.numPostura = QUIETO

		# El rectangulo del Sprite
		self.rect = pygame.Rect(100,100,self.coordenadasHoja[self.numPostura][self.numImagenPostura][2],self.coordenadasHoja[self.numPostura][self.numImagenPostura][3])

		# Las velocidades de caminar y salto
		self.velocidadCarrera = velocidadCarrera 
		self.velocidadSalto = velocidadSalto

		# El retardo en la animacion del personaje (podria y deberia ser distinto para cada postura)
		self.retardoAnimacion = retardoAnimacion

		# Y actualizamos la postura del Sprite inicial, llamando al metodo correspondiente
		self.actualizarPostura()


	# Metodo base para realizar el movimiento: simplemente se le indica cual va a hacer, y lo almacena,
	# Solo actualizamos los dados en los argumentos, los otros quedan igual.
	def mover(self, movimientos):
		for key,value in movimientos.items():
			self.movimientos[key] = value

	#Pone todo a false y luego cambia
	def mover_wreset(self, movimientos):
		temp = {IZQUIERDA:False,DERECHA:False,ARRIBA:False,ABAJO:False,ATAQUE1:False}

		for key,value in movimientos.items():
			temp[key] = value

		self.movimientos = temp

	def actualizarPostura(self, is_enemy=False):
		self.retardoMovimiento -= 1
		# Miramos si ha pasado el retardo para dibujar una nueva postura
		if (self.retardoMovimiento < 0):
			self.retardoMovimiento = self.retardoAnimacion
			# Si ha pasado, actualizamos la postura
			self.numImagenPostura += 1
			if self.numImagenPostura >= len(self.coordenadasHoja[self.numPostura]):
				if self.numPostura == P_ATACANDO1: self.posturas[P_ATACANDO1] = False
				if self.numPostura == P_MURIENDO:
					self.numImagenPostura -= 1
					self.kill()
				else:
					self.numImagenPostura = 0;
			if self.numImagenPostura < 0:
				self.numImagenPostura = len(self.coordenadasHoja[self.numPostura])-1

			self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])

			if (self.tipo == PLAYER):
				if  self.mirando != IZQUIERDA:
					self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
				elif self.mirando != DERECHA:
					self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)
			else:
				if  self.mirando != DERECHA:
					self.image = self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura])
				elif self.mirando != IZQUIERDA:
					self.image = pygame.transform.flip(self.hoja.subsurface(self.coordenadasHoja[self.numPostura][self.numImagenPostura]), 1, 0)

	def actualizarVida(self):
		time = pygame.time.get_ticks()
		if(time > self.invulnerable_clock + self.invulnerable_delay):
			self.invulnerable_clock = time
			if (self.vida == 1):
				self.vida = 0
				self.posturas[P_MURIENDO] = True
				self.numPostura = P_MURIENDO
				self.numImagenPostura = 0
			elif(self.vida>0):
				self.vida-=1

		return self.vida

	def update(self, grupoPlataformas, tiempo):
		if(tiempo > 1000): return	#Fix para cuando un fotograma consume mucho tiempo, normalmente al inicio de la escena, se descarte, ya que haría movimientos incosistentes dado la larga duración que se aplicaría a los movimientos

		# Si no tenemos vida, no podemos realziar movimientos
		if self.vida <= 0:
			self.mover_wreset({})

		# Si caemos, morimos
		if self.rect.top > ALTO_PANTALLA:
			self.vida = 0 
			self.kill()

		# Las velocidades a las que iba hasta este momento
		(velocidadx, velocidady) = self.velocidad

		# Si vamos a la izquierda o a la derecha        
		if (self.movimientos[IZQUIERDA] != self.movimientos[DERECHA]):	#XOR! No se mueve si se pulsa izq y der
			# Esta mirando hacia ese lado
			if self.movimientos[IZQUIERDA]:
				self.mirando = IZQUIERDA
				velocidadx = -self.velocidadCarrera
			else: 
				self.mirando = DERECHA
				velocidadx = self.velocidadCarrera

			self.posturas[P_ANDANDO] = True
		else:
			self.posturas[P_ANDANDO] = False
			velocidadx = 0

		plataformas = pygame.sprite.spritecollide(self, grupoPlataformas, False)
		#COLISIONES
		floor_detected = None

		for plataforma in plataformas:
			if(plataforma.tipo != 1):
				if( (self.rect.bottom-3) < plataforma.rect.bottom): #Sobre una plataforma
					if(self.rect.centerx + 10 > plataforma.rect.left and self.rect.centerx - 10 < plataforma.rect.right): #Plataforma sobre la que estamos
						self.posturas[P_SALTANDO] = False 	#Dejamos de saltar solo si estáos cayendo
						if(floor_detected == None or floor_detected.rect.left > plataforma.rect.left):
							floor_detected = plataforma
							if (plataforma.tipo == 0): #Suelo
									self.establecerPosicion((self.posicion[0], plataforma.posicion[1]-plataforma.rect.height+1))							
							else:	#Rampa
								percent_ramp = (float(self.rect.centerx) - float(plataforma.rect.left))/float(plataforma.rect.width);
								if percent_ramp < 0: 
									percent_ramp = 0
								elif percent_ramp > 1:
									percent_ramp = 1

								if(plataforma.tipo == 2):
									new_y = plataforma.rect.bottom - float(percent_ramp)*plataforma.rect.height
								else:
									new_y = plataforma.rect.top + float(percent_ramp)*plataforma.rect.height
								self.establecerPosicion((self.posicion[0], (new_y)))

			elif(self.rect.bottom > plataforma.rect.top + 15 and plataforma.tipo == 1): #Paredes [No atravesarlas]
				if( self.mirando == DERECHA and self.rect.right > plataforma.rect.left and self.rect.left < plataforma.rect.left): velocidadx = 0
				elif( self.mirando == IZQUIERDA and self.rect.left < plataforma.rect.right and self.rect.right > plataforma.rect.right): velocidadx = 0

		if floor_detected == None : self.posturas[P_SALTANDO] = True
		
		# Si queremos saltar
		if self.movimientos[ARRIBA]:
			# La postura actual sera estar saltando
			if not self.posturas[P_SALTANDO] : velocidady = -self.velocidadSalto
			self.posturas[P_SALTANDO] = True
			# Le imprimimos una velocidad en el eje y

		if self.posturas[P_SALTANDO]:
			velocidady += GRAVEDAD * float(tiempo) 
		else: 
			velocidady = 0

		# Si queremos atacar [Tenemos que comprobar que queremos atacar, pero también que ya no estemos atacando y que haya pasado el retardo desde el último ataque realizado]
		if self.movimientos[ATAQUE1] and not self.posturas[P_ATACANDO1]:
			time = pygame.time.get_ticks()
			if (time > self.ataque_clock + self.ataque_retardo):
				self.ataque_clock = time
				self.posturas[P_ATACANDO1] = True
				self.retardoMovimiento = -1
				self.numImagenPostura = 0

		self.numPostura = QUIETO
		for postura,value in self.posturas.items():
			if value: self.numPostura = postura

		if self.numPostura == QUIETO: 
			self.numPostura = QUIETO

		#velocidady = 0
		# Actualizamos la imagen a mostrar
		self.actualizarPostura()

		# Aplicamos la velocidad en cada eje      
		self.velocidad = (velocidadx, velocidady)

		# Y llamamos al método de la superclase para que, según la velocidad y el tiempo
		#  calcule la nueva posición del Sprite

		MiSprite.update(self, tiempo)

		return

# -------------------------------------------------
# Clase Jugador

class Jugador(Personaje):
	"Cualquier personaje del juego"
	def __init__(self):
		# Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
		Personaje.__init__(self,PLAYER,'pirata_Player_v3.png','pirata_Player_v3.txt', [6, 7, 5, 7, 6], VELOCIDAD_JUGADOR, VELOCIDAD_SALTO_JUGADOR, RETARDO_ANIMACION_JUGADOR, 1000, 6);

	def mover(self, teclasPulsadas, teclasConfig):
		#Miramos si la tecla para cada movimiento esta pulsada o no
		movimientos = {}
		for key,value in teclasConfig.items():
			movimientos.update({key: teclasPulsadas[value]})

		Personaje.mover(self,movimientos)

	def avanzar(self):
		for key,value in self.movimientos.items():
			value = False

		self.movimientos[DERECHA] = True


# -------------------------------------------------
# Clase NoJugador 

class NoJugador(Personaje):
	"El resto de personajes no jugadores"
	def __init__(self,tipo, archivoImagen, archivoCoordenadas, numImagenes, velocidad, velocidadSalto, retardoAnimacion, delayAtaque, vidas):
		# Primero invocamos al constructor de la clase padre con los parametros pasados
		Personaje.__init__(self,tipo, archivoImagen, archivoCoordenadas, numImagenes, velocidad, velocidadSalto, retardoAnimacion, delayAtaque, vidas);

	# Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
	# La implementacion por defecto, este metodo deberia de ser implementado en las clases inferiores
	#  mostrando la personalidad de cada enemigo
	def mover_cpu(self, jugador1, jugador2):
		# Por defecto un enemigo no hace nada
		#  (se podria programar, por ejemplo, que disparase al jugador por defecto)
		return

# -------------------------------------------------
# Clase Pirata

class Pirata(NoJugador):
	"El enemigo 'Pirata'"
	def __init__(self):
		# Invocamos al constructor de la clase padre con la configuracion de este personaje concreto
		NoJugador.__init__(self,EPIRATA1,'Pirate.gif','pirate.txt', [4, 6, 5, 4, 6], VELOCIDAD_EPIRATA, VELOCIDAD_SALTO_EPIRATA, RETARDO_ANIMACION_EPIRATA, 3000, 3);
	
	# Aqui vendria la implementacion de la IA segun las posiciones de los jugadores
	# La implementacion de la inteligencia segun este personaje particular

	def mover_cpu(self, jugador1):
		# Movemos solo a los enemigos que esten en la pantalla
		if self.rect.left>0 and self.rect.right<ANCHO_PANTALLA and self.rect.bottom>0 and self.rect.top<ALTO_PANTALLA:

			# Y nos movemos andando hacia el protagonista, si estamos muy cerca atacamos
			if jugador1.rect.right-5<self.rect.left:
				Personaje.mover_wreset(self,{IZQUIERDA:True})
			elif(jugador1.rect.left-5>self.rect.right):
				Personaje.mover_wreset(self,{DERECHA:True})
			else:
				Personaje.mover_wreset(self,{ATAQUE1:True})

			# Si está por encima el prota, saltamos
			if (jugador1.rect.bottom < self.rect.top): Personaje.mover(self,{ARRIBA:True})

		# Si este personaje no esta en pantalla, no hara nada
		else:
			Personaje.mover_wreset(self,{})
