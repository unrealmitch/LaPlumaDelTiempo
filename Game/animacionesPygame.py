# -*- encoding: utf-8 -*-

import pyganim

# Extendemos la clase animacion de PygAnimation para darle posicion
class Animacion(pyganim.PygAnimation):
	def __init__(self, *args):
		pyganim.PygAnimation.__init__(self, args)
		# Posicion que tendra esta animacion
		self.posicionx = 0
		self.posiciony = 0
		
	def mover(self, distanciax, distanciay):
		self.posicionx += distanciax
		self.posiciony += distanciay

	def dibujar(self, pantalla):
		self.blit(pantalla, (self.posicionx, self.posiciony))

# Las distintas animaciones que tendremos

class AnimacionOlas(Animacion):
	def __init__(self):
		array_animation = []
		for i in range(1,48):
			array_animation.append(('animations/pirata_waves/frame (' + str(i) + ').gif', 0.1))

		pyganim.PygAnimation.__init__(self,array_animation)

class AnimacionLava(Animacion):
	def __init__(self):
		array_animation = []
		for i in range(1,9):
			array_animation.append(('animations/dino_lava/frame (' + str(i) + ').png', 0.1))

		pyganim.PygAnimation.__init__(self,array_animation)

class AnimacionMenuPirata(Animacion):
	def __init__(self):
		array_animation = []
		for i in range(1,25):
			array_animation.append(('animations/menu_pirata/frame (' + str(i) + ').png', 0.1))

		pyganim.PygAnimation.__init__(self,array_animation)

class AnimacionMenuDino(Animacion):
	def __init__(self):
		array_animation = []
		for i in range(1,25):
			array_animation.append(('animations/menu_dino/frame (' + str(i) + ').png', 0.1))

		pyganim.PygAnimation.__init__(self,array_animation)

class AnimacionMenuPirataArcade(Animacion):
	def __init__(self):
		array_animation = []
		for i in range(1,25):
			array_animation.append(('animations/menu_pirata_arcade/frame (' + str(i) + ').png', 0.1))

		pyganim.PygAnimation.__init__(self,array_animation)