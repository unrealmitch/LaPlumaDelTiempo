# -*- encoding: utf-8 -*-

import pygame
from pygame.locals import *
from escena import *
from gestorRecursos import *
from escenaCarga import EscenaCarga
from animacionesPygame import *
from escenaAnim1 import EscenaAnimacion1

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
        if fase == 0:
            self.animPortal = AnimacionMenuDino()
            self.animPortal.posicionx = 0.75*ANCHO_PANTALLA
            self.animPortal.posiciony = 0.1*ALTO_PANTALLA
            pyganim.PygAnimation.scale(self.animPortal, (int(400*ESCALA*0.7), int(400*ESCALA*0.7)))
            self.sound_bso = GestorRecursos.CargarSonido('dino_bso_jp.ogg')
            self.lvl = 'DINOS_LVL'
        else:
            self.animPortal = AnimacionMenuPirata()
            self.animPortal.posicionx = 0.75*ANCHO_PANTALLA
            self.animPortal.posiciony = 0.5*ALTO_PANTALLA
            pyganim.PygAnimation.scale(self.animPortal, (int(400*ESCALA*0.7), int(400*ESCALA*0.7)))
            self.sound_bso = GestorRecursos.CargarSonido('pirata_bso_pc.ogg')
            self.lvl = 'PIRATAS_LVL'

        self.block = imagen = GestorRecursos.CargarImagen("pirate_block.png", -1)
        self.block = pygame.transform.scale(self.block, (int(400*ESCALA*0.7), int(400*ESCALA*0.7)))

        self.animPortal.pause()
        self.channel_bso = self.sound_bso.play(-1)
        self.channel_bso.set_volume(0)

        ElementoGUI.__init__(self, pantalla, (400*ESCALA,400*ESCALA) )

    def dibujar(self, pantalla):

        if(self.fase == 1 and GestorRecursos.getConfigParam('DINOS_LVL') == 0):
            pantalla.blit(self.block, (0.75*ANCHO_PANTALLA, 0.5*ALTO_PANTALLA))
        else:
            self.animPortal.dibujar(pantalla)
            lvl = GestorRecursos.getConfigParam(self.lvl)
            text = "Nivel: " + str(lvl)
            texto = pygame.font.SysFont('arial', 20).render(text, True, (0,238,255))
            rect = texto.get_rect()
            rect.center = (ANCHO_PANTALLA/1.4, self.animPortal.posiciony + 105)
            pantalla.blit(texto, rect)

    def accion(self):
        self.pantalla.menu.ejecutarJuego(self.fase)

    def posicionEnElemento(self, posicion):
        (posicionx, posiciony) = posicion
        if(posicionx > self.animPortal.posicionx and posicionx < self.animPortal.posicionx + 400*ESCALA and posiciony> self.animPortal.posiciony and posiciony < self.animPortal.posiciony + 400*ESCALA):
            return True
        else:
            return False

    def focus(self,over):
        if over and not (self.fase == 1 and GestorRecursos.getConfigParam('DINOS_LVL') == 0 ):
            self.animPortal.play()
            if self.channel_bso.get_busy() == False: self.channel_bso = self.sound_bso.play(-1)
            self.channel_bso.set_volume(0.75)
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
        # Animacion
        animDino = Portal(self, 0)
        self.elementosGUI.append(animDino)

        animPirata = Portal(self, 1)
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
        self.channel_bso.set_volume(0.4)
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
        self.channel_bso.set_volume(0.4)

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
                escena = EscenaAnimacion1(self.director)
        else:
                escena = EscenaCarga(self.director, fase)
        #escena = EscenaCarga(self.director, fase)
        self.director.apilarEscena(escena)

    def mostrarPantallaInicial(self):
        self.pantallaActual = 0

    # def mostrarPantallaConfiguracion(self):
    #    self.pantallaActual = ...
