# si no chuta, pot caldre instalar:
#   > pip install pyserial

import serial
import serial.tools.list_ports

class SerialCom:
    def __init__(self):
        self._s = serial.Serial()

    def startSerial(self):
        self._s.baudrate = 9600
        self._s.port = "COM3"
        self._s.open()

    def writeSerial(self, command):
        self._s.write(command.encode('utf-8'))

    def endSerial(self):
        self._s.close()