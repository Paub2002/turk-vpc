# si no chuta, pot caler instalar:
# pip install pyserial

import serial
import serial.tools.list_ports
import sympy as sp   # library for symbolic calculation
import numpy as np
from sympy import *
import math
import time
class Kine2:
    def calcAngle(self, reqcos):
        res1 = math.atan2(math.sqrt(1-math.pow(reqcos,
        2)), reqcos)
        res2 = math.atan2(math.sqrt(1-math.pow(reqcos,
        2))*(-1), reqcos)
        return (res1, res2)

    def inputCalc(self):
        px = float(input("px:"))
        py = float(input("py:"))
        l1 = float(input("l1:"))
        l2 = float(input("l2:"))
        ctheta2 = (px**2 + py**2 - l1**2 - l2**2) / (2 *
        l1 * l2)
        stheta2 = math.sqrt(1-math.pow(ctheta2, 2))
        ctheta1 = (px * (l1 + l2 * ctheta2) + py * l2 *
        stheta2) / (px**2 + py**2)
        theta1a, theta1b = self.calcAngle(ctheta1)
        theta2a, theta2b = self.calcAngle(ctheta2)
        print("theta1: {} and {}".format(math.degrees(theta1a),math.degrees(theta1b)))
        print("theta2: {} and {}".format(math.degrees(theta2a),math.degrees(theta2b)))
#kine2 = Kine2()
#kine2.inputCalc()


s = serial.Serial()
s.baundrate = 96000

# choose port
ports = serial.tools.list_ports.comports()

s.port = "COM3"

# start communication
s.open()

"""if ports:
    print("Ports serial disponibles:")
    for port in ports:
        print(f"- {port.device}: {port.description}")
else:
    print("No s'han trobat ports serial disponibles.")

s.port = "COM3"

# start communication
s.open()
while True:
    command = "1234"
    s.write(command.encode('utf-8'))
    break
        


s.close()"""

def movement(command):
    print("Command: ", command)

    s.write(command.encode('utf-8'))

    s.close()
    time.sleep(10)
