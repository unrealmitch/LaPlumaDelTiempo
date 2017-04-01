# -*- encoding: utf-8 -*-

import pyglet
import random
from escena import *
from escenaCarga import EscenaCarga
from escenaAnim2 import EscenaAnimacion2



# -------------------------------------------------
# Clase para las animaciones que solo ocurriran una vez
#  (sin bucles)

class EscenaAnimacion1(EscenaPyglet, pyglet.window.Window):

    def __init__(self,director):
        # Constructores de las clases padres
        EscenaPyglet.__init__(self, director)
        pyglet.window.Window.__init__(self, ANCHO_PANTALLA, ALTO_PANTALLA)

        # La imagen de fondo
        self.imagen = pyglet.image.load('images/pasillo2.jpg')
        self.imagen = pyglet.sprite.Sprite(self.imagen)
        self.imagen.scale = float(ANCHO_PANTALLA) / self.imagen.width



        # Las animaciones que habra en esta escena
        # No se crean aqui las animaciones en si, porque se empiezan a reproducir cuando se crean
        # Lo que se hace es cargar los frames de disco para que cuando se creen ya esten en memoria

        # Creamos el batch de las animaciones
        self.batch = pyglet.graphics.Batch()
        # Y los grupos para ponerlas por pantalla
        self.grupoDetras =  pyglet.graphics.OrderedGroup(0)
        self.grupoMedio =   pyglet.graphics.OrderedGroup(1)
        self.grupoDelante = pyglet.graphics.OrderedGroup(2)



        # La animacion de texto
        self.animacionTextoFrames = [
            pyglet.image.AnimationFrame(pyglet.image.load('images/menu_animacion1/texto1.png'), 7.5),
            pyglet.image.AnimationFrame(pyglet.image.load('images/menu_animacion1/texto2.png'), 2.5),
            pyglet.image.AnimationFrame(pyglet.image.load('images/menu_animacion1/texto3.png'), 10.5),
            pyglet.image.AnimationFrame(pyglet.image.load('images/menu_animacion1/texto4.png'), 18.5),
            pyglet.image.AnimationFrame(pyglet.image.load('images/menu_animacion1/texto5.png'), 7.5),
            ]

        # Por ahora no creamos la animacion, porque se empezaria a reproducir,
        #  solo cargamos los frames de disco
        # Esta animacion aparecera en el segundo determinado
        pyglet.clock.schedule_once(self.aparecerTexto, 1)


        self.animacionPrincipalFrames = [pyglet.image.AnimationFrame(pyglet.image.load('images/dibujo1.png'),47)]
        
        pyglet.clock.schedule_once(self.aparecerPrincipal, 1)

        self.animacionProfesoraFrames = [pyglet.image.AnimationFrame(pyglet.image.load('images/profesora.png'),31)]
        
        pyglet.clock.schedule_once(self.aparecerProfesora, 9)




    # El metodo para eliminar una animacion determinada
    def eliminarAnimacion(self, tiempo, animacion):
        animacion.delete()


    # Metodo para hacer aparecer los bocadillos de texto en pantalla
    def aparecerTexto(self, tiempo):
        animacionTexto = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionTextoFrames), batch=self.batch, group=self.grupoDelante)
        animacionTexto.scale = 0.8
        animacionTexto.set_position(215,50)
        # Programamos que se elimine la animacion cuando termine
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionTexto.image.get_duration(), animacionTexto)

     # Metodo para hacer aparecer la animacion del protagonista en pantalla
    def aparecerPrincipal(self, tiempo):
        animacionPrincipal = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionPrincipalFrames), batch=self.batch, group=self.grupoMedio)
        animacionPrincipal.scale = 0.4
        animacionPrincipal.set_position(10,10)
        # Programamos que se elimine la animacion cuando termine
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionPrincipal.image.get_duration(), animacionPrincipal)


     # Metodo para hacer aparecer la animacion de la profesora en pantalla
    def aparecerProfesora(self, tiempo):
        animacionProfesora = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionProfesoraFrames), batch=self.batch, group=self.grupoMedio)
        animacionProfesora.scale = 0.4
        animacionProfesora.set_position(750,10)
        # Programamos que se elimine la animacion cuando termine
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionProfesora.image.get_duration(), animacionProfesora)
    
    # El evento relativo a la pulsacion de una tecla
    def on_key_press(self, symbol, modifiers):
        # Si se pulsa Escape, se sale del programa
        if symbol == pyglet.window.key.ESCAPE:
            self.terminarEscena()



    # El evento que se ejecuta cada vez que hay que dibujar la pantalla
    def on_draw(self):
        # Si la ventana esta visible
        if self.visible:
            # Borramos lo que hay en pantalla
            self.clear()
            # Dibujamos la imagen
            if self.imagen!=None:
                self.imagen.draw()
            # Y, para cada animacion, la dibujamos
            # Para hacer esto, le decimos al batch que se dibuje
            self.batch.draw()


    # Si intentan cerrar esta ventana, saldremos de la escena
    def on_close(self):
        self.terminarEscena()

    # El evento relativo al clic del raton
    def on_mouse_press(self, x, y, button, modifiers):
        # Si se pulsa el boton izquierdo
        if (pyglet.window.mouse.LEFT == button):
            self.terminarEscena()
        return




    def terminarEscena(self):
        # Creamos la nueva escena
        escena = EscenaAnimacion2(self.director)
        # Y cambiamos la actual por la nueva
        self.director.cambiarEscena(escena)

