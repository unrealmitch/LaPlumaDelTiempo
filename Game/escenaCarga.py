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

# -------------------------------------------------
# Clase EscenaCarga

class EscenaCarga(EscenaPygame):
    def __init__(self, director, fase):
        EscenaPygame.__init__(self, director)
        self.tipoLetra = GestorRecursos.CargarFuente('menu_font_space_age.ttf', 40)
        self.fase = fase;

        if(self.fase == 1):
            recursos = "piratas.conf"
            title = '#Loading mision 2: PIRATAS'
        else:
            recursos = "dinosaurios.conf"
            title = '#Loading mision 1: DINOSAURIOS'

        self.texto = self.tipoLetra.render(title, True, (0,238,255), (0,0,0))
        self.rect = self.texto.get_rect()
        self.rect.center = (ANCHO_PANTALLA/2, ALTO_PANTALLA/2)

        self.tipoLetra2 = GestorRecursos.CargarFuente('menu_font_space_age.ttf', 18)
        self.texto2 = self.tipoLetra2.render("!Localiza y acaba con el hombre misterioso!", True, (0,175,200), (0,0,0))
        self.rect2 = self.texto2.get_rect()
        self.rect2.center = (ANCHO_PANTALLA/2, ALTO_PANTALLA/1.5)
        
        recursos = os.path.join('others', recursos)
        self.conf_file = open(recursos, "r")
        self.conf_lines = self.conf_file.readlines ()
        self.it = iter (self.conf_lines)
        

    def update(self, tiempo):
        # Carga los elementos de la fase uno a uno en cada iteracion del bucle 
        # de eventos
        try:
            i = next(self.it, None)
            i = i[0:len(i)-1] # Quita el \n del final de las cadenas
            GestorRecursos.CargarImagenAlpha(i)
        except TypeError:
            # Entra después de cargar todas las lineas del iterador. No se puede
            # hacer len() de un tipo None. Ahora carga la escena del juego.
            
            if(self.fase == 1):
                escenaPiratas = Piratas(self.director)
                self.director.cambiarEscena(escenaPiratas)
            else:
                escenaDinosauros= Dinosaurios(self.director)
                self.director.cambiarEscena(escenaDinosauros)
            return

    def dibujar(self, pantalla):
        # Mostrar mensaje de espera
        pantalla.fill((0,0,0))
        pantalla.blit(self.texto, self.rect)
        pantalla.blit(self.texto2, self.rect2)

    def eventos(self, lista_eventos):
        for evento in lista_eventos:
            if evento.type == KEYDOWN and evento.key == K_ESCAPE:
                self.director.salirPrograma()
            if evento.type == pygame.QUIT:
                self.director.salirPrograma()

