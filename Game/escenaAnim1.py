# -*- encoding: utf-8 -*-

import pyglet
import random
from escena import *
from escenaCarga import EscenaCarga
from escenaAnim3 import EscenaAnimacion3



# -------------------------------------------------
# Clase para las animaciones que solo ocurriran una vez
#  (sin bucles)

class EscenaAnimacion1(EscenaPyglet, pyglet.window.Window):

    def __init__(self,director):
        # Constructores de las clases padres
        EscenaPyglet.__init__(self, director)
        pyglet.window.Window.__init__(self, ANCHO_PANTALLA, ALTO_PANTALLA)

        # La imagen de fondo
        #self.imagen = pyglet.sprite.Sprite(self.imagen)
        #self.imagen.scale = float(ANCHO_PANTALLA) / self.imagen.width
        self.imagen = None
        
        # Las animaciones que habra en esta escena
        # No se crean aqui las animaciones en si, porque se empiezan a reproducir cuando se crean
        # Lo que se hace es cargar los frames de disco para que cuando se creen ya esten en memoria
        # Creamos el batch de las animaciones
        self.batch = pyglet.graphics.Batch()
        # Y los grupos para ponerlas por pantalla
        self.grupoDetras  = pyglet.graphics.OrderedGroup(0)
        self.grupoMedio   = pyglet.graphics.OrderedGroup(1)
        self.grupoDelante = pyglet.graphics.OrderedGroup(2)

        #
        # 
        # Primera animación
        
        # Animación fondo
        self.animacionFondoFrames1 = [
            # Parameters of an AnimationFrame
            # pyglet.image.AnimationFrame (image, number of seconds to display )
            pyglet.image.AnimationFrame(pyglet.image.load('images/pasillo2.jpg'), 47)]
        #  schedule_once method causes a function to be called once “n” seconds
        #  in the future
        pyglet.clock.schedule_once(self.aparecerFondo1, 1)
            
        # La animacion de texto
        self.animacionTextoFrames1 = [
            pyglet.image.AnimationFrame(pyglet.image.load('images/menu_animacion1/texto1.png'), 7.5),
            pyglet.image.AnimationFrame(pyglet.image.load('images/menu_animacion1/texto2.png'), 2.5),
            pyglet.image.AnimationFrame(pyglet.image.load('images/menu_animacion1/texto3.png'), 10.5),
            pyglet.image.AnimationFrame(pyglet.image.load('images/menu_animacion1/texto4.png'), 18.5),
            pyglet.image.AnimationFrame(pyglet.image.load('images/menu_animacion1/texto5.png'), 7.5),
            ]
        # Esta animacion aparecera en el segundo determinado
        pyglet.clock.schedule_once(self.aparecerTexto1, 1)

        # Animación Principal
        self.animacionPrincipalFrames = [pyglet.image.AnimationFrame(pyglet.image.load('images/dibujo1.png'),47)]
        pyglet.clock.schedule_once(self.aparecerPrincipal, 1)

        # Animación de la profesora
        self.animacionProfesoraFrames = [pyglet.image.AnimationFrame(pyglet.image.load('images/profesora.png'),31)]
        pyglet.clock.schedule_once(self.aparecerProfesora, 9)

        #
        #
        # Segunda animación

        self.animacionFondoFrames2 = [
            pyglet.image.AnimationFrame(pyglet.image.load('images/puerta.PNG'), 9)]
        pyglet.clock.schedule_once(self.aparecerFondo2, 48)
        
        # La animacion de texto 2
        self.animacionTextoFrames2 = [
            pyglet.image.AnimationFrame(pyglet.image.load('images/menu_animacion1/texto6.png'), 6.5),
            ]
        pyglet.clock.schedule_once(self.aparecerTexto2, 50)

        #
        #
        # Tercera animación        

        self.animacionFondoFrames3 = [
            pyglet.image.AnimationFrame(pyglet.image.load('images/VeilRoom.jpg'), 66)]
        pyglet.clock.schedule_once(self.aparecerFondo3, 56.5)

        # La animacion de texto 3
        self.animacionTextoFrames3 = [
            pyglet.image.AnimationFrame(pyglet.image.load('images/menu_animacion1/texto7.png'), 7.5),
            pyglet.image.AnimationFrame(pyglet.image.load('images/menu_animacion1/texto8.png'), 9.5),
            pyglet.image.AnimationFrame(pyglet.image.load('images/menu_animacion1/texto9.png'), 14.5),
            pyglet.image.AnimationFrame(pyglet.image.load('images/menu_animacion1/texto10.png'), 14.5),
            pyglet.image.AnimationFrame(pyglet.image.load('images/menu_animacion1/texto11.png'), 11.5),
            pyglet.image.AnimationFrame(pyglet.image.load('images/menu_animacion1/texto12.png'), 5.5),
            ]
        pyglet.clock.schedule_once(self.aparecerTexto3, 59)
        
        self.animacionPrincipalFrames3 = [pyglet.image.AnimationFrame(pyglet.image.load('images/dibujo1.png'),63)]
        pyglet.clock.schedule_once(self.aparecerPrincipal3, 59)

        self.animacionLiderFrames3 = [pyglet.image.AnimationFrame(pyglet.image.load('images/lider.png'),63)]
        pyglet.clock.schedule_once(self.aparecerLider3, 59)     

        pyglet.clock.schedule_once(self.terminarEscena, 122)

    #
    # 
    # Métodos para activar la primera animación            

    # Metodo para hacer aparecer los bocadillos de texto en pantalla
    def aparecerFondo1(self, tiempo):
        animacionFondo = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionFondoFrames1), batch=self.batch, group=self.grupoDetras)
        animacionFondo.scale = float(ANCHO_PANTALLA) / animacionFondo.width
        # Programamos que se elimine la animacion cuando termine
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionFondo.image.get_duration(), animacionFondo)

    def aparecerTexto1(self, tiempo):
        animacionTexto = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionTextoFrames1), batch=self.batch, group=self.grupoDelante)
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


    #
    # 
    # Métodos para activar la segunda animación

    def aparecerFondo2(self, tiempo):
        animacionFondo = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionFondoFrames2), batch=self.batch, group=self.grupoDetras)
        animacionFondo.scale = float(ANCHO_PANTALLA) / animacionFondo.width
        # Programamos que se elimine la animacion cuando termine
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionFondo.image.get_duration(), animacionFondo)

    def aparecerTexto2(self, tiempo):
        animacionTexto = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionTextoFrames2), batch=self.batch, group=self.grupoDelante)
        animacionTexto.scale = 0.8
        animacionTexto.set_position(215,50)
        # Programamos que se elimine la animacion cuando termine
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionTexto.image.get_duration(), animacionTexto)


    #
    # 
    # Métodos para activar la tercera animación

    def aparecerFondo3(self, tiempo):
        animacionFondo = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionFondoFrames3), batch=self.batch, group=self.grupoDetras)
        animacionFondo.scale = float(ANCHO_PANTALLA) / animacionFondo.width
        # Programamos que se elimine la animacion cuando termine
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionFondo.image.get_duration(), animacionFondo)

    def aparecerTexto3(self, tiempo):
        animacionTexto = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionTextoFrames3), batch=self.batch, group=self.grupoDelante)
        animacionTexto.scale = 0.8
        animacionTexto.set_position(215,50)
        # Programamos que se elimine la animacion cuando termine
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionTexto.image.get_duration(), animacionTexto)
        
    def aparecerPrincipal3(self, tiempo):
        animacionPrincipal = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionPrincipalFrames3), batch=self.batch, group=self.grupoMedio)
        animacionPrincipal.scale = 0.4
        animacionPrincipal.set_position(10,10)
        # Programamos que se elimine la animacion cuando termine
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionPrincipal.image.get_duration(), animacionPrincipal)

     # Metodo para hacer aparecer la animacion del lider
    def aparecerLider3(self, tiempo):
        animacionLider = pyglet.sprite.Sprite(pyglet.image.Animation(self.animacionLiderFrames3), batch=self.batch, group=self.grupoMedio)
        animacionLider.scale = 0.4
        animacionLider.set_position(750,10)
        # Programamos que se elimine la animacion cuando termine
        pyglet.clock.schedule_once(self.eliminarAnimacion, animacionLider.image.get_duration(), animacionLider)        

        
    #
    # 
    # Eventos
    
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


    #
    # 
    # Métodos propios de la clase
    
    # El metodo para eliminar una animacion determinada
    def eliminarAnimacion(self, tiempo, animacion):
        animacion.delete()

    def terminarEscena(self, tiempo):
        # Creamos la nueva escena
        escena = EscenaCarga(self.director, 0)
        # Y cambiamos la actual por la nueva
        self.director.cambiarEscena(escena)

