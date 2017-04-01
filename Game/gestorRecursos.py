# -*- coding: utf-8 -*-

import pygame, sys, os
import json
from escena import *
from pygame.locals import *


# -------------------------------------------------
# Clase GestorRecursos

# En este caso se implementa como una clase vacía, solo con métodos de clase
class GestorRecursos(object):
	recursos = {}
	config = {'ARRIBA': K_UP, 'ABAJO': K_DOWN, 'IZQUIERDA': K_LEFT, 'DERECHA': K_RIGHT, 'ATAQUE1': K_SPACE, 'SOUND': 100, 'DINOS_LVL': 0, 'PIRATAS_LVL': 0, 'RATIO': (16,9), 'RES': 600}

	@classmethod
	def CargarImagen(cls, nombre, colorkey=None):
		# Si el nombre de archivo está entre los recursos ya cargados
		if nombre in cls.recursos:
			# Se devuelve ese recurso
			return cls.recursos[nombre]
		# Si no ha sido cargado anteriormente
		else:
			# Se carga la imagen indicando la carpeta en la que está
			fullname = os.path.join('images', nombre)
			try:
				imagen = pygame.image.load(fullname)
			except pygame.error, message:
				print 'Cannot load image:', fullname
				raise SystemExit, message
			imagen = imagen.convert()
			if colorkey is not None:
				if colorkey is -1:
					colorkey = imagen.get_at((0,0))
				imagen.set_colorkey(colorkey, RLEACCEL)
			# Se almacena
			imagen = pygame.transform.scale(imagen, (int(imagen.get_size()[0]*ESCALA), int(imagen.get_size()[1]*ESCALA)))
			cls.recursos[nombre] = imagen
			# Se devuelve
			return imagen
			
	@classmethod
	def CargarImagenAlpha(cls, nombre, colorkey=None):
		# Si el nombre de archivo está entre los recursos ya cargados
		if nombre in cls.recursos:
			# Se devuelve ese recurso
			return cls.recursos[nombre]
		# Si no ha sido cargado anteriormente
		else:
			# Se carga la imagen indicando la carpeta en la que está
			fullname = os.path.join('images', nombre)
			try:
				imagen = pygame.image.load(fullname)
			except pygame.error, message:
				print 'Cannot load image:', fullname
				raise SystemExit, message	
			if colorkey is not None:
				if colorkey is -2:
					imagen = imagen.convert_alpha()
				else:
					imagen.convert()
					if colorkey is -1:
						colorkey = imagen.get_at((0,0))
					imagen.set_colorkey(colorkey, RLEACCEL)
			# Se almacena
			imagen = pygame.transform.scale(imagen, (int(imagen.get_size()[0]*ESCALA), int(imagen.get_size()[1]*ESCALA)))
			cls.recursos[nombre] = imagen
			# Se devuelve
			return imagen

	@classmethod
	def CargarArchivoCoordenadas(cls, nombre):
		# Si el nombre de archivo está entre los recursos ya cargados
		if nombre in cls.recursos:
			# Se devuelve ese recurso
			return cls.recursos[nombre]
		# Si no ha sido cargado anteriormente
		else:
			# Se carga el recurso indicando el nombre de su carpeta
			fullname = os.path.join('images', nombre)
			pfile=open(fullname,'r')
			datos=pfile.read()
			pfile.close()
			# Se almacena
			cls.recursos[nombre] = datos
			# Se devuelve
			return datos

	@classmethod
	def CargarMapaPlataformas(cls, nombre):
		lista = []
		fullname = os.path.join('others', nombre)
		file=open(fullname,'r')
		
		while True: 
			linea = file.readline().split()
			if not linea:
				break
			if linea[0][0] == '#' or len(linea)<4:
				continue 
			try:
				linea = [int(i) for i in linea]
			except Exception:
				print('Mira el fichero, imbecil!')
				continue
			if len(linea) == 4:
				linea.append(0)
			lista.append(linea)
		file.close()
		return lista

	@classmethod
	def CargarSonido(cls, nombre):
		# Si el nombre de archivo está entre los recursos ya cargados
		if nombre in cls.recursos:
			# Se devuelve ese recurso
			return cls.recursos[nombre]
		# Si no ha sido cargado anteriormente
		else:
			# Se carga la imagen indicando la carpeta en la que está
			fullname = os.path.join('sound', nombre)
			try:
				sound = pygame.mixer.Sound(fullname)
			except pygame.error, message:
				print 'Cannot load image:', fullname
				raise SystemExit, message
			# Se almacena
			cls.recursos[nombre] = sound
			# Se devuelve
			return sound

	@classmethod
	def CargarFuente(cls, nombre, height):
		# Si el nombre de archivo está entre los recursos ya cargados
		if nombre in cls.recursos and height == cls.recursos[nombre].get_height():
			# Se devuelve ese recurso
                        return cls.recursos[nombre]
		# Si no ha sido cargado anteriormente
		else:
			# Se carga la imagen indicando la carpeta en la que está
			fullname = os.path.join('fonts', nombre)
			try:
				font = pygame.font.Font(fullname, height)
			except pygame.error, message:
				raise SystemExit, message
			# Se almacena
			cls.recursos[nombre] = font
			# Se devuelve
			return font

	@classmethod
	def CargarGif(cls, folder, frames, colorkey=None):
		# Si el nombre de archivo está entre los recursos ya cargados
		nombre = 'gif-' + folder
		if nombre in cls.recursos:
			# Se devuelve ese recurso
			return cls.recursos[nombre]
		# Si no ha sido cargado anteriormente
		else:
			# Se carga la imagen indicando la carpeta en la que está
			gif = []
			for i in range(frames):
				try:
					fullname = os.path.join(folder, 'frame (' + str(i+1) + ').jpg')
					imagen = pygame.image.load(fullname)
				except pygame.error, message:
					print 'Cannot load image:', fullname
					raise SystemExit, message
				imagen = imagen.convert()
				if colorkey is not None:
					if colorkey is -1:
						colorkey = imagen.get_at((0,0))
					imagen.set_colorkey(colorkey, RLEACCEL)
				imagen = pygame.transform.scale(imagen, 
                                    (int(imagen.get_size()[0]*ESCALA), 
                                    int(imagen.get_size()[1]*ESCALA)))
				gif.append(imagen)
				# Se almacena
			cls.recursos[folder] = gif
			# Se devuelve
			return gif

	@classmethod
	def LoadConfig(cls):
		fullname = os.path.join('others', 'game.conf')
		try:
			with open(fullname, 'r') as fp:
				cls.config = json.load(fp)
		except IOError, message:
				print 'Cannot load configuration file:', fullname, ' Creating default file config!'
				cls.SaveConfig()


	@classmethod
	def SaveConfig(cls):
		fullname = os.path.join('others', 'game.conf')
		try:
			with open(fullname, 'w') as fp:
				json.dump(cls.config, fp, sort_keys=True, indent=4)
		except IOError, message:
				print 'Cannot save configuration file:', fullname
				raise SystemExit, message
    
	@classmethod
	def getConfigParam(cls, param):
		return cls.config[param]

	@classmethod
	def setConfigParam(cls, param, value):
		cls.config[param] = value
		cls.SaveConfig()