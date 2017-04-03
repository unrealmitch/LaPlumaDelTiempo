# -*- encoding: utf-8 -*-

import pygame
from pygame.locals import *
from escena import *
from gestorRecursos import *
from escenaCarga import EscenaCarga
from animacionesPygame import *
from escenaAnim1 import EscenaAnimacion1
from escenaTexto import EscenaTexto
from escenaHistoria import EscenaHistoria


# -------------------------------------------------
# Clase abstracta ElementoGUI

class ElementoGUI:
	def __init__(self, pantalla, rectangulo):
		self.pantalla = pantalla
		self.rect = rectangulo

	def establecerPosicion(self, posicion):
		(posicionx, posiciony) = posicion
		self.rect.left = posicionx
		self.rect.bottom = posiciony

	def posicionEnElemento(self, posicion):
		(posicionx, posiciony) = posicion
		if (posicionx>=self.rect.left) and (posicionx<=self.rect.right) and (posiciony>=self.rect.top) and (posiciony<=self.rect.bottom):
			return True
		else:
			return False

	def focus(self,over):
		''

	def dibujar(self):
		raise NotImplemented("Tiene que implementar el metodo dibujar.")
	def accion(self):
		raise NotImplemented("Tiene que implementar el metodo accion.")

class Portal(ElementoGUI):
	def __init__(self, pantalla, fase):
		self.fase = fase

		self.block = imagen = GestorRecursos.CargarImagen("pirate_block.png", -1)
		self.block = pygame.transform.scale(self.block, (int(400*ESCALA*0.7), int(400*ESCALA*0.7)))

		if fase == 0:
			self.animPortal = AnimacionMenuDino()
			self.animPortal.posicionx = 0.75*ANCHO_PANTALLA
			self.animPortal.posiciony = 0.1*ALTO_PANTALLA
			pyganim.PygAnimation.scale(self.animPortal, (int(400*ESCALA*0.7), int(400*ESCALA*0.7)))
			self.sound_bso = GestorRecursos.CargarSonido('dino_bso_jp.ogg')
			self.lvl = 'DINOS_LVL'
		elif fase == 1:
			self.animPortal = AnimacionMenuPirata()
			self.animPortal.posicionx = 0.75*ANCHO_PANTALLA
			self.animPortal.posiciony = 0.5*ALTO_PANTALLA
			pyganim.PygAnimation.scale(self.animPortal, (int(400*ESCALA*0.7), int(400*ESCALA*0.7)))
			self.sound_bso = GestorRecursos.CargarSonido('pirata_bso_pc.ogg')
			self.lvl = 'PIRATAS_LVL'
		elif fase == 2:
			self.animPortal = AnimacionMenuPirataArcade()
			self.animPortal.posicionx = 0.4*ANCHO_PANTALLA
			self.animPortal.posiciony = 0.3*ALTO_PANTALLA
			pyganim.PygAnimation.scale(self.animPortal, (int(400*ESCALA*0.7), int(400*ESCALA*0.7)))
			self.sound_bso = GestorRecursos.CargarSonido('arcade_menu.ogg')
			self.lvl = 'PIRATAS_ARCADE'



		self.animPortal.pause()
		self.channel_bso = self.sound_bso.play(-1)
		self.channel_bso.set_volume(0)

		ElementoGUI.__init__(self, pantalla, (400*ESCALA,400*ESCALA) )

	def dibujar(self, pantalla):

		if(self.fase == 2 and not self.available(1)): return
		
		if(not self.available()):
			pantalla.blit(self.block, (self.animPortal.posicionx, self.animPortal.posiciony))
		else:
			self.animPortal.dibujar(pantalla)
			lvl = GestorRecursos.getConfigParam(self.lvl)

			if self.fase < 2:
				text = "Nivel: " + str(lvl)
				texto = pygame.font.SysFont('arial', 20).render(text, True, (0,238,255))
				rect = texto.get_rect()
				rect.center = (ANCHO_PANTALLA/1.4, self.animPortal.posiciony + 105)
				pantalla.blit(texto, rect)
			else:
				text = "Max Time: " + str(lvl)
				texto = pygame.font.SysFont('arial', 20).render(text, True, (0,238,255))
				rect = texto.get_rect()
				rect.center = (ANCHO_PANTALLA/2-5, self.animPortal.posiciony + 220)
				pantalla.blit(texto, rect)

				text = "S:" + str(GestorRecursos.getConfigParam('PIRATAS_ARCADE_score')) +" R: " + str(GestorRecursos.getConfigParam('PIRATAS_ARCADE_round'))
				texto = pygame.font.SysFont('arial', 20).render(text, True, (0,200,255))
				rect = texto.get_rect()
				rect.center = (ANCHO_PANTALLA/2-5, self.animPortal.posiciony + 240)
				pantalla.blit(texto, rect)




	def available(self, fase = -1):
		if fase == -1: fase = self.fase
		if (fase == 1 and GestorRecursos.getConfigParam('DINOS_LVL') < 1) or (fase == 2 and GestorRecursos.getConfigParam('PIRATAS_LVL') < 2):
			return False
		else:
			return True

	def accion(self):
		if(self.available()):
			self.pantalla.menu.ejecutarJuego(self.fase)

	def posicionEnElemento(self, posicion):
		(posicionx, posiciony) = posicion
		if(posicionx > self.animPortal.posicionx and posicionx < self.animPortal.posicionx + 400*ESCALA and posiciony> self.animPortal.posiciony and posiciony < self.animPortal.posiciony + 400*ESCALA):
			return True
		else:
			return False

	def focus(self,over):
		if over and self.available():
			self.animPortal.play()
			if self.channel_bso.get_busy() == False: self.channel_bso = self.sound_bso.play(-1)
			self.channel_bso.set_volume(1)
			return True
		else:
			self.animPortal.pause()
			self.channel_bso.set_volume(0)
			return False

# -------------------------------------------------
# Clase Boton y los distintos botones

class Boton(ElementoGUI):
	def __init__(self, pantalla, nombreImagen, posicion):
		# Se carga la imagen del boton
		self.imagen = GestorRecursos.CargarImagen(nombreImagen,-1)
		self.imagen = pygame.transform.scale(self.imagen, (20, 20))
		# Se llama al método de la clase padre con el rectángulo que ocupa el botón
		ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
		# Se coloca el rectangulo en su posicion
		self.establecerPosicion(posicion)
	def dibujar(self, pantalla):
		pantalla.blit(self.imagen, self.rect)

class BotonJugar(Boton):
	def __init__(self, pantalla):
		Boton.__init__(self, pantalla, 'menu_boton_comenzar.png', 
			(ANCHO_PANTALLA*0.5 ,ALTO_PANTALLA*0.90))
	def accion(self):
		self.pantalla.menu.ejecutarJuego(0)

class BotonSalir(Boton):
	def __init__(self, pantalla):
		Boton.__init__(self, pantalla, 'menu_boton_salir.png', 
			(ANCHO_PANTALLA*0.5-10,ALTO_PANTALLA*0.90))
	def accion(self):
		self.pantalla.menu.salirPrograma()

# -------------------------------------------------
# Clase TextoGUI y los distintos textos

class TextoGUI(ElementoGUI):
	def __init__(self, pantalla, fuente, color, texto, posicion):
		# Se crea la imagen del texto
		self.imagen = fuente.render(texto, True, color)
		# Se llama al método de la clase padre con el rectángulo que ocupa el texto
		ElementoGUI.__init__(self, pantalla, self.imagen.get_rect())
		# Se coloca el rectangulo en su posicion
		self.establecerPosicion(posicion)
		
	def dibujar(self, pantalla):
		pantalla.blit(self.imagen, self.rect)

# ¡Ojo con el tamaño de las fuentes! Casi con total seguridad internamente el
# tamaño se indexa comentando en 0, como los arrays.
# Una vez cargada la fuente, si se usa el método fuente.get_height() nos devuelve
# height-1 respento a los valores del constructor.
class TextoJugar(TextoGUI):
	def __init__(self, pantalla):
		fuente = GestorRecursos.CargarFuente('menu_font_space_age.ttf', 29)
		TextoGUI.__init__(self, pantalla, fuente, (0, 238, 255), 'Comenzar', 
			(ANCHO_PANTALLA*0.5, ALTO_PANTALLA*0.87))
	def accion(self):
		self.pantalla.menu.ejecutarJuego(0)

class TextoSalir(TextoGUI):
	def __init__(self, pantalla):
		# La fuente la debería cargar el estor de recursos
		fuente = GestorRecursos.CargarFuente('menu_font_space_age.ttf', 29-1)
		TextoGUI.__init__(self, pantalla, fuente, (0, 238, 255), 'Salir', 
			(100*ESCALA, ALTO_PANTALLA*0.86))
		self.rect.centerx = ANCHO_PANTALLA*0.5

	def accion(self):
		self.pantalla.menu.salirPrograma()
# -------------------------------------------------
# Clase PantallaGUI y las distintas pantallas

class PantallaGUI:
	def __init__(self, menu, nombreImagen):
		self.menu = menu
		# Se carga la imagen de fondo
		self.imagen = GestorRecursos.CargarImagen(nombreImagen)
		self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
		# Se tiene una lista de elementos GUI
		self.elementosGUI = []

	def eventos(self, lista_eventos):
		if self.menu.channel_bso.get_busy() == False: self.menu.channel_bso = self.menu.song.play(-1)
		for evento in lista_eventos:
			if evento.type == MOUSEMOTION:
				self.menu.unmute()
				mouse = pygame.mouse.get_pos()
				for elemento in self.elementosGUI:
					if elemento.focus(elemento.posicionEnElemento(mouse)): self.menu.mute()
			if evento.type == MOUSEBUTTONDOWN:
				self.elementoClic = None
				for elemento in self.elementosGUI:
					if elemento.posicionEnElemento(evento.pos):
						self.elementoClic = elemento
			if evento.type == MOUSEBUTTONUP:
				for elemento in self.elementosGUI:
					if elemento.posicionEnElemento(evento.pos):
						if (elemento == self.elementoClic):
							elemento.accion()

	def dibujar(self, pantalla):
		# Dibujamos primero la imagen de fondo
		pantalla.blit(self.imagen, self.imagen.get_rect())

		for elemento in self.elementosGUI:
			elemento.dibujar(pantalla)

class PantallaInicialGUI(PantallaGUI):
	def __init__(self, menu):
		PantallaGUI.__init__(self, menu, 'portada.jpg')
		# Creamos los botones y los metemos en la lista
		botonJugar = BotonJugar(self)
		botonSalir = BotonSalir(self)
		#self.elementosGUI.append(botonJugar)
		self.elementosGUI.append(botonSalir)
		# Creamos el texto y lo metemos en la lista
		textoJugar = TextoJugar(self)
		textoSalir = TextoSalir(self)
		#self.elementosGUI.append(textoJugar)
		self.elementosGUI.append(textoSalir)
		# Animacion Portales
		animDino = Portal(self, 0)
		self.elementosGUI.append(animDino)

		animPirata = Portal(self, 1)
		self.elementosGUI.append(animPirata)

		animPirata = Portal(self, 2)
		self.elementosGUI.append(animPirata)

# -------------------------------------------------
# Clase Menu, la escena en sí

class Menu(EscenaPygame):

	def __init__(self, director):
		# Llamamos al constructor de la clase padre
		EscenaPygame.__init__(self, director);
		# Creamos la lista de pantallas
		self.listaPantallas = []
		self.song = GestorRecursos.CargarSonido('menu_bso.ogg')
		self.channel_bso = self.song.play(-1)
		self.channel_bso.set_volume(0.3)
		# Creamos las pantallas que vamos a tener
		#   y las metemos en la lista
		self.listaPantallas.append(PantallaInicialGUI(self))
		# En que pantalla estamos actualmente
		self.mostrarPantallaInicial()

	def update(self, *args):
		return

	def mute (self):
		self.channel_bso.set_volume(0)

	def unmute(self):
		self.channel_bso.set_volume(0.3)

	def eventos(self, lista_eventos):
		# Se mira si se quiere salir de esta escena
		for evento in lista_eventos:
			# Si se quiere salir, se le indica al director
			if evento.type == KEYDOWN:
				if evento.key == K_ESCAPE:
					self.salirPrograma()
				if evento.key == K_F11:
					pygame.display.toggle_fullscreen()
			elif evento.type == pygame.QUIT:
				self.director.salirPrograma()

		# Se pasa la lista de eventos a la pantalla actual
		self.listaPantallas[self.pantallaActual].eventos(lista_eventos)

	def dibujar(self, pantalla):
		self.listaPantallas[self.pantallaActual].dibujar(pantalla)

	#--------------------------------------
	# Metodos propios del menu

	def salirPrograma(self):
		self.director.salirPrograma()

	def ejecutarJuego(self,fase):
		pygame.mixer.stop();

		if fase == 0:
			escena = EscenaCarga(self.director, fase)
			self.director.apilarEscena(escena)
			escena = EscenaHistoria(self.director, fase)
		elif fase == 1:
			escena = EscenaCarga(self.director, fase)
			self.director.apilarEscena(escena)
			escena = EscenaHistoria(self.director, fase)
		else:
			escena = EscenaCarga(self.director, fase)

		self.director.apilarEscena(escena)

	''' IMPLEMENTACION CON Pyglet
		if fase == 0 and GestorRecursos.getConfigParam('DINOS_LVL') == 0:
				escena = EscenaAnimacion1(self.director)
		#if fase == 0 and GestorRecursos.getConfigParam('DINOS_LVL') == 0:
	'''

	''' IMPLEMENTACION CON EscenaTexto
		ocultas = False
		if fase == 0 and GestorRecursos.getConfigParam('DINOS_LVL') < 10:
			i = 18
			ocultas = True
			while i >0:
			#escena = EscenaTexto(self.director, fase, 1)
				escena = EscenaTexto(self.director, fase, i)
				self.director.apilarEscena(escena)
				i-=1
		elif fase == 1 and GestorRecursos.getConfigParam('PIRATAS_LVL') == 0 and not ocultas:
			i = 18
			while i >14:
			#escena = EscenaTexto(self.director, fase, 1)
				escena = EscenaTexto(self.director, fase, i)
				self.director.apilarEscena(escena)
				i-=1
		else:
			escena = EscenaCarga(self.director, fase)
			#escena = EscenaCarga(self.director, fase)
			self.director.apilarEscena(escena)
	'''

	def mostrarPantallaInicial(self):
		self.pantallaActual = 0

	# def mostrarPantallaConfiguracion(self):
	#    self.pantallaActual = ...
