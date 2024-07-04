# si no chuta, pot caler instalar:
# pip install pyserial

import serial
import serial.tools.list_ports

s = serial.Serial()
s.baundrate = 96000

# choose port
ports = serial.tools.list_ports.comports()

if ports:
    print("Ports serial disponibles:")
    for port in ports:
        print(f"- {port.device}: {port.description}")
else:
    print("No s'han trobat ports serial disponibles.")

s.port = input("Port: ")

# start communication
s.open()

while True:
    command = input()
    s.write(command.encode('utf-8'))
    if command == 'exit':
        s.close() # so important.
        exit()