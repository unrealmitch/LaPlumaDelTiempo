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

# La animacion del fuego
class AnimacionFuego(Animacion):
	def __init__(self):
		pyganim.PygAnimation.__init__(self,[
										('imagenes/flame_a_0001.png', 0.1),
										('imagenes/flame_a_0002.png', 0.1),
										('imagenes/flame_a_0003.png', 0.1),
										('imagenes/flame_a_0004.png', 0.1),
										('imagenes/flame_a_0005.png', 0.1),
										('imagenes/flame_a_0006.png', 0.1)])

# La animacion del rayo
class AnimacionRayo(Animacion):
	def __init__(self):
		pyganim.PygAnimation.__init__(self,[
										('imagenes/bolt_strike_0001.png', 0.1),
										('imagenes/bolt_strike_0002.png', 0.1),
										('imagenes/bolt_strike_0003.png', 0.1),
										('imagenes/bolt_strike_0004.png', 0.1),
										('imagenes/bolt_strike_0005.png', 0.1),
										('imagenes/bolt_strike_0006.png', 0.1),
										('imagenes/bolt_strike_0007.png', 0.1),
										('imagenes/bolt_strike_0008.png', 0.1),
										('imagenes/bolt_strike_0009.png', 0.1),
										('imagenes/bolt_strike_0010.png', 0.1)])

# La animacion del humo
class AnimacionHumo(Animacion):
	def __init__(self):
		pyganim.PygAnimation.__init__(self,[
										('imagenes/smoke_puff_0001.png', 0.1),
										('imagenes/smoke_puff_0002.png', 0.1),
										('imagenes/smoke_puff_0003.png', 0.1),
										('imagenes/smoke_puff_0004.png', 0.1),
										('imagenes/smoke_puff_0005.png', 0.1),
										('imagenes/smoke_puff_0006.png', 0.1),
										('imagenes/smoke_puff_0007.png', 0.1),
										('imagenes/smoke_puff_0008.png', 0.2),
										('imagenes/smoke_puff_0009.png', 0.2),
										('imagenes/smoke_puff_0010.png', 0.2)])

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