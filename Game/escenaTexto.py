# -*- coding: utf-8 -*-

import random,math
import pygame, escena
from escena import *
from personajes import *
from escenario import *
from pygame.locals import *
from animacionesPygame import *
from piratas import Piratas
from dinosaurios import Dinosaurios
from piratas_arcade import Piratas_Arcade
from gestorRecursos import *
from escenaCarga import EscenaCarga

# -------------------------------------------------
# Clase EscenaCarga

class EscenaTexto(EscenaPygame):
    def __init__(self, director, fase, numEscena):
    	self.fase = fase
    	self.numEscena = numEscena
        EscenaPygame.__init__(self, director)
        if numEscena==1:
        	self.imagen = GestorRecursos.CargarImagen('menu_animacion4/dialogo1.png')
        elif numEscena==2:
        	self.imagen = GestorRecursos.CargarImagen('menu_animacion4/dialogo2.png')
        elif numEscena==3:
        	self.imagen = GestorRecursos.CargarImagen('menu_animacion4/dialogo3.png')
        elif numEscena==4:
        	self.imagen = GestorRecursos.CargarImagen('menu_animacion4/dialogo4.png')
        elif numEscena==5:
        	self.imagen = GestorRecursos.CargarImagen('menu_animacion4/dialogo5.png')
        elif numEscena==6:
        	self.imagen = GestorRecursos.CargarImagen('menu_animacion4/dialogo6.png')
        elif numEscena==7:
        	self.imagen = GestorRecursos.CargarImagen('menu_animacion4/dialogo7.png')
        elif numEscena==8:
        	self.imagen = GestorRecursos.CargarImagen('menu_animacion4/dialogo8.png')
        elif numEscena==9:
        	self.imagen = GestorRecursos.CargarImagen('menu_animacion4/dialogo9.png')
        elif numEscena==10:
        	self.imagen = GestorRecursos.CargarImagen('menu_animacion4/dialogo10.png')
        elif numEscena==11:
        	self.imagen = GestorRecursos.CargarImagen('menu_animacion4/dialogo11.png')
        elif numEscena==12:
        	self.imagen = GestorRecursos.CargarImagen('menu_animacion4/dialogo12.png')
        elif numEscena==13:
        	self.imagen = GestorRecursos.CargarImagen('menu_animacion4/dialogo13.png')
        elif numEscena==14:
        	self.imagen = GestorRecursos.CargarImagen('menu_animacion4/dialogo14.png')
        elif numEscena==15:
        	self.imagen = GestorRecursos.CargarImagen('menu_animacion4/dialogo15.png')
        elif numEscena==16:
        	self.imagen = GestorRecursos.CargarImagen('menu_animacion4/dialogo16.png')
        elif numEscena==17:
        	self.imagen = GestorRecursos.CargarImagen('menu_animacion4/dialogo17.png')
        elif numEscena==18:
        	self.imagen = GestorRecursos.CargarImagen('menu_animacion4/final.jpg')
        self.imagen = pygame.transform.scale(self.imagen, (ANCHO_PANTALLA, ALTO_PANTALLA))
        
    def update(self, tiempo):
        return

    def dibujar(self, pantalla):
        # Dibujamos primero la imagen de fondo
        pantalla.blit(self.imagen, self.imagen.get_rect())
        
    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == KEYDOWN and evento.key == K_SPACE:
            	#escena = EscenaTexto(self.director, self.fase, numEscena)
                #escena = EscenaCarga(self.director, self.fase)
                if self.numEscena ==13 :
                	escena = EscenaCarga(self.director, 0)
                	self.director.cambiarEscena(escena)
                elif self.numEscena == 14:
                	escena = EscenaCarga(self.director, 1)
                	self.director.cambiarEscena(escena)
                else:
                	self.director.salirEscena()
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

