# -*- encoding: utf-8 -*-

# Modulos
import pygame
import sys
#import escena
from escena import *
from pygame.locals import *


class Director():

    def __init__(self):
        # Inicializamos la pantalla y el modo grafico
        #self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), pygame.FULLSCREEN, 32)
        self.screen = pygame.display.set_mode((ANCHO_PANTALLA, ALTO_PANTALLA), 0, 32)
        
        pygame.mixer.pre_init(44100, 16, 2, 4096)
        pygame.mixer.init()
        pygame.display.set_caption("La pluma del tiempo...")

        # Pila de escenas
        self.pila = []
        # Flag que nos indica cuando quieren salir de la escena
        self.salir_escena = False
        # Reloj
        self.reloj = pygame.time.Clock()

        #self.screen.fill((0,0,0))
        #tipoLetra = pygame.font.SysFont('arial', 48)
        #texto = tipoLetra.render('#Loading mision 1...', True, (255,255,255), (0,0,0))
        #self.screen.blit(texto, (ANCHO_PANTALLA/2-200,ALTO_PANTALLA/2-50,300,300))
        #pygame.display.flip()


    def bucle(self, escena):

        self.salir_escena = False

        # Eliminamos todos los eventos producidos antes de entrar en el bucle
        pygame.event.clear()
        
        # El bucle del juego, las acciones que se realicen se harán en cada escena
        while not self.salir_escena:

            # Sincronizar el juego a 60 fps
            tiempo_pasado = self.reloj.tick(60)
            
            # Pasamos los eventos a la escena
            escena.eventos(pygame.event.get())

            # Actualiza la escena
            escena.update(tiempo_pasado)

            # Se dibuja en pantalla
            escena.dibujar(self.screen)
            pygame.display.flip()


    def ejecutar(self):

        # Mientras haya escenas en la pila, ejecutaremos la de arriba
        while (len(self.pila)>0):

            # Se coge la escena a ejecutar como la que este en la cima de la pila
            escena = self.pila[len(self.pila)-1]

            # Ejecutamos el bucle de eventos hasta que termine la escena
            self.bucle(escena)


    def salirEscena(self):
        # Indicamos en el flag que se quiere salir de la escena
        self.salir_escena = True
        # Eliminamos la escena actual de la pila (si la hay)
        if (len(self.pila)>0):
            self.pila.pop()

    def salirPrograma(self):
        # Vaciamos la lista de escenas pendientes
        self.pila = []
        self.salir_escena = True

    def cambiarEscena(self, escena):
        self.salirEscena()
        # Ponemos la escena pasada en la cima de la pila
        self.pila.append(escena)

    def apilarEscena(self, escena):
        self.salir_escena = True
        # Ponemos la escena pasada en la cima de la pila
        #  (por encima de la actual)
        self.pila.append(escena)

