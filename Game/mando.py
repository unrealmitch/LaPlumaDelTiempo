import pygame
import sys

LINUX = 0
WINDOWS = 1

if sys.platform.startswith("lin"):
    platform_id = LINUX
elif sys.platform.startswith("win"):
    platform_id = WINDOWS

if platform_id == LINUX:
    A = 0
    B = 1
    X = 2
    Y = 3
    bump_izq = 4
    bump_der = 5
    BACK = 6
    START = 7
    # GUIDE = 8
    stick_izquierdoBTN = 9
    stick_derechoBTN = 10

    # Axes
    stick_izquierdoX = 0
    stick_izquierdoY = 1
    stick_derechoX = 3
    stick_derechoY = 4
    izquierda_gatillo = 2
    derecha_gatillo = 5

elif platform_id == WINDOWS:
    A = 0
    B = 1
    X = 2
    Y = 3
    bump_izq = 4
    bump_der = 5
    BACK = 6
    START = 7
    stick_izquierdoBTN = 8
    stick_derechoBTN = 9

    # Axes
    stick_izquierdoX = 0
    stick_izquierdoY = 1
    stick_derechoX = 4
    stick_derechoY = 3
    gatilloS = 2

class Mando:
    def __init__(self, id, deadzone = 0.15):
        self.joystick = pygame.joystick.Joystick(id)
        self.joystick.init()
        self.deadzone = deadzone

        self.izquierda_gatillo_used = False
        self.derecha_gatillo_used = False

    def get_id(self):
        return self.joystick.get_id()

    def deadzone_ajuste(self, value):
        if value > self.deadzone:
            return (value - self.deadzone) / (1 - self.deadzone)
        elif value < -self.deadzone:
            return (value + self.deadzone) / (1 - self.deadzone)
        else:
            return 0

    def get_buttons(self):
        if platform_id == LINUX:
            return (self.joystick.get_button(A),
                    self.joystick.get_button(B),
                    self.joystick.get_button(X),
                    self.joystick.get_button(Y),
                    self.joystick.get_button(bump_izq),
                    self.joystick.get_button(bump_der),
                    self.joystick.get_button(BACK),
                    self.joystick.get_button(START),
                    0, # Solo Windows
                    self.joystick.get_button(stick_izquierdoBTN),
                    self.joystick.get_button(stick_derechoBTN))

        elif platform_id == WINDOWS:
            return (self.joystick.get_button(A),
                    self.joystick.get_button(B),
                    self.joystick.get_button(X),
                    self.joystick.get_button(Y),
                    self.joystick.get_button(bump_izq),
                    self.joystick.get_button(bump_der),
                    self.joystick.get_button(BACK),
                    self.joystick.get_button(START),
                    self.joystick.get_button(stick_izquierdoBTN),
                    self.joystick.get_button(stick_derechoBTN))

    def get_stick_izquierdo(self):
        stick_izquierdox = self.deadzone_ajuste(self.joystick.get_axis(stick_izquierdoX))
        stick_izquierdoy = self.deadzone_ajuste(self.joystick.get_axis(stick_izquierdoY))

        return (stick_izquierdox, stick_izquierdoy)

    def get_stick_derecho(self):
        stick_derechox = self.deadzone_ajuste(self.joystick.get_axis(stick_derechoX))
        stick_derechoy = self.deadzone_ajuste(self.joystick.get_axis(stick_derechoY))

        return (stick_derechox, stick_derechoy)

    def get_gatillos(self):
        gatillo_axis = 0.0

        if platform_id == LINUX:
            izquierda = self.joystick.get_axis(izquierda_gatillo)
            derecha = self.joystick.get_axis(derecha_gatillo)

            if izquierda != 0:
                self.izquierda_gatillo_used = True
            if derecha != 0:
                self.derecha_gatillo_used = True

            if not self.izquierda_gatillo_used:
                izquierda = -1
            if not self.derecha_gatillo_used:
                derecha = -1

            gatillo_axis = (-1 * izquierda + derecha) / 2

        elif platform_id == WINDOWS:
            gatillo_axis = -1 * self.joystick.get_axis(gatilloS)

        return gatillo_axis

    def get_pad(self): 
        hat_x, hat_y = self.joystick.get_hat(0)

        arriba = int(hat_y == 1)
        derecha = int(hat_x == 1)
        abajo = int(hat_y == -1)
        izquierda = int(hat_x == -1)

        return arriba, derecha, abajo, izquierda