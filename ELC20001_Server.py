import socket
import sys
import threading
import numpy as np
import pandas as pd
from datetime import datetime
import tkinter as tk
from tkinter import ttk
import csv
import openpyxl
from datetime import datetime
current_date_and_time = datetime.now()

print("The current date and time is", current_date_and_time)
LARGEFONT = ("Verdana",35)

# IP address and port to listen on
server_ip = "192.168.183.252"
server_port = 1234

# Create a TCP socket
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Bind the socket to the IP address and port
server_socket.bind((server_ip, server_port))

# Listen for incoming connections
server_socket.listen(2)  # Allowing up to 2 clients

print("Water level monitoring server is listening at {}:{}".format(server_ip, server_port))
print()

# Empty dictionary to store water level values for each client
water_level_values = {}



def send_message(client_socket, message):
    client_socket.send(message.encode())


def button1_clicked(client_socket):
    message = 1
    send_message(client_socket, str(message))


def button2_clicked(client_socket):
    message = 0
    send_message(client_socket, str(message))

def handle_client(client_socket, client_address):
    # Create an empty list to store water level values for this client
    water_level_values[client_address] = []

    try:
        while True:
            # Receive data from the client

            data = client_socket.recv(1024).decode()
            if data == "HIGH water level from client 1":
                # Close the client socket
                window = tk.Tk()
                window.title("Message Sender")

                message_label = ttk.Label(window, text= data, font=LARGEFONT)
                message_label.pack(pady=10)

                    # Create Button 1
                button1 = tk.Button(window, text="Client 1", command=lambda: button1_clicked(client_socket))
                button1.pack(pady=10)

                    # Create Button 2
                button2 = tk.Button(window, text="Client 2", command=lambda: button2_clicked(client_socket))
                button2.pack(pady=10)

                    # Start the Tkinter event loop
                window.mainloop() 
            if data == "HIGH water level from client 2":
                # Close the client socket
                window = tk.Tk()
                window.title("Message Sender")

                message_label = ttk.Label(window, text= data, font=LARGEFONT)
                message_label.pack(pady=10)

                    # Create Button 1
                button1 = tk.Button(window, text="Client 1", command=lambda: button1_clicked(client_socket))
                button1.pack(pady=10)

                    # Create Button 2
                button2 = tk.Button(window, text="Client 2", command=lambda: button2_clicked(client_socket))
                button2.pack(pady=10)

                    # Start the Tkinter event loop
                window.mainloop()     

                

            with open("ressult.txt", "a") as f:
                f.write(str(current_date_and_time)+"\n")
                f.write(str(client_address) + "\n")
                f.write(data + "\n")    
 
            
            

             
            if not data:
                break  # Break the loop if no data is received

            # Print the received data
            print("Received data from client {}: {}".format(client_address, data))

            # Append the received data to the water level values list for this client
            water_level_values[client_address].append(data)

                   # Set the window title




    except Exception as e:
        print("Error handling client {}: {}".format(client_address, str(e)))

    finally:
        client_socket.close()
        print("Client disconnected:", client_address)



try:
    while True:
        # Accept a client connection
        client_socket, client_address = server_socket.accept()
        print("Client connected:", client_address)

        # Start a new thread to handle the client
        client_thread = threading.Thread(target=handle_client, args=(client_socket, client_address))
        client_thread.start()
                # Create the main window
        
        
 

        

except KeyboardInterrupt:
    # Close the server socket on keyboard interrupt
    server_socket.close()

    

    

    