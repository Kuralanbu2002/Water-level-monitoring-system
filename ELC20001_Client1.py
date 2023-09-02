import socket
import RPi.GPIO as GPIO
import time

sensor = 7
buzzer = 23

# Set the GPIO mode
GPIO.setmode(GPIO.BOARD)
GPIO.setup(sensor, GPIO.IN)
GPIO.setup(buzzer, GPIO.OUT)
GPIO.output(buzzer, False)

# IP address and port of the server
server_ip = "192.168.43.252"
server_port = 1234

# Create a TCP socket
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect to the server
client_socket.connect((server_ip, server_port))

print("Water level monitoring client connected to {}:{}".format(server_ip, server_port))
print()

while True:
    if GPIO.input(sensor):
        data = "HIGH water level from client 1"
        print(data)
        client_socket.send(data.encode())
        break    
    else:
        GPIO.output(buzzer, False)
        data = "LOW water level\n"
        print(data)
        client_socket.send(data.encode())
        time.sleep(0.2)

# Receive user message from the server
while True:
    GPIO.output(buzzer, False)
    user_message = client_socket.recv(1024).decode()
    print(user_message)
    if (int(user_message) ==1 and int(GPIO.input(sensor)==1)):
        GPIO.output(buzzer,True)
        time.sleep(0.2)
    while(GPIO.input(sensor)):
        time.sleep(0.2)
        
    
        



time.sleep(0.2)
