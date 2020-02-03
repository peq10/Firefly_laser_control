#Import serial control module
#read the docs at https://pyserial.readthedocs.io/en/latest/shortintro.html
import serial
import time

#initialise a serial port (name of port, baud rate). The name will likely be different on your computer
ser = serial.Serial('/dev/ttyACM0',9600)

#read initial serial message
answer = ser.readline()
print(answer.decode('utf-8'))


#turn LED off and on in infinite loop
LED_status = 1
while True:
    LED_status = int(not LED_status)
    command = str(LED_status)
    print(f'Sent: {command}')
    ser.write(command.encode('utf-8'))
    response = ser.readline()
    print(f'Response: {response.decode("utf-8")}')
    time.sleep(1)



