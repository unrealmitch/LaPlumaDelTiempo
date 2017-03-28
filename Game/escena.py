# -*- encoding: utf-8 -*-


ALTO_PANTALLA = 600
ANCHO_PANTALLA = int((ALTO_PANTALLA*4)/3)
#ANCHO_PANTALLA = 1000

ESCALA = ALTO_PANTALLA / 800.

# -------------------------------------------------
# Clase Escena con lo metodos abstractos

class Escena:

    def __init__(self, director):
        self.director = director

    def update(self, *args):
        raise NotImplemented("Tiene que implementar el metodo update.")

    def eventos(self, *args):
        raise NotImplemented("Tiene que implementar el metodo eventos.")

    def dibujar(self, pantalla):
        raise NotImplemented("Tiene que implementar el metodo dibujar.")
