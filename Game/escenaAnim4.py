# -*- encoding: utf-8 -*-

import pyglet
import random
from escena import *





# -------------------------------------------------
# Clase para las animaciones que solo ocurriran una vez
#  (sin bucles)

class Animacion(pyglet.window.Window):

    def __init__(self):
        # Constructores de la clase padre
        pyglet.window.Window.__init__(self, ANCHO_PANTALLA, ALTO_PANTALLA)

        # La imagen de fondo
        self.imagen = pyglet.image.load('images/VeilRoom.jpg')
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
            pyglet.image.AnimationFrame(pyglet.image.load('images/menu_animacion1/texto13.png'), 12.5),
            ]
        # El ultimo frame se pone con una duracion de None, porque el humo no se reproduce en bucle,
        #  sino solo una vez
        # Por ahora no creamos la animacion, porque se empezaria a reproducir,
        #  solo cargamos los frames de disco
        # Esta animacion aparecera en el segundo determinado
        pyglet.clock.schedule_once(self.aparecerTexto, 1)


        self.animacionPrincipalFrames = [pyglet.image.AnimationFrame(pyglet.image.load('images/dibujo1.png'),13)]
        
        pyglet.clock.schedule_once(self.aparecerPrincipal, 1)

        self.animacionLiderFrames = [pyglet.image.AnimationFrame(pyglet.image.load('images/lider.png'),14)]
        
        pyglet.clock.schedule_once(self.aparecerLider, 1)




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

     # Metodo para hacer aparecer la animacion del protagonista
    def aparecerPrincipal(self, tiempo):
        animacionPrincipal = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionPrincipalFrames), batch=self.batch, group=self.grupoMedio)
        animacionPrincipal.scale = 0.4
        animacionPrincipal.set_position(10,10)
        # Programamos que se elimine la animacion cuando termine
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionPrincipal.image.get_duration(), animacionPrincipal)


     # Metodo para hacer aparecer la animacion del lider
    def aparecerLider(self, tiempo):
        animacionLider = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionLiderFrames), batch=self.batch, group=self.grupoMedio)
        animacionLider.scale = 0.4
        animacionLider.set_position(750,10)
        # Programamos que se elimine la animacion cuando termine
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionLider.image.get_duration(), animacionLider)
    
    # El evento relativo a la pulsacion de una tecla
    def on_key_press(self, symbol, modifiers):
        # Si se pulsa Escape, se sale de la animacion
        self.close()


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


    # El evento relativo al clic del raton
    def on_mouse_press(self, x, y, button, modifiers):
        # Si se pulsa el boton izquierdo
        if (pyglet.window.mouse.LEFT == button):
            self.close()






if __name__ == '__main__':

    animacion = Animacion()

    # Ejecutamos la aplicacion de pyglet
    pyglet.app.run()

