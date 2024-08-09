from bluedot.btcomm import BluetoothServer
import time
from signal import pause
from datetime import datetime
from dist_sensor import measure_distance

# flag to control when data transfer starts
# a message must be sent to change this value to 1
server_init = 0

def data_received(data):
    """ echo back sent message or start data transfer """
    global server_init
    if server_init == 0:
        server.send("Data transfer initiated\n")
        server_init = 1
    else:
        server.send(f"Received - {data}")

def client_connected():
    print("Client connected")

def client_disconnected():
    print("Client disconnected")

print("Initialising server")
server = BluetoothServer(
    data_received,
    auto_start = False,
    when_client_connects = client_connected,
    when_client_disconnects = client_disconnected
)

print("Starting server")
server.start()
print(server.server_address)
print("Waiting for connection - open serial monitor app")

# check server alive
while server_init == 0:
    time.sleep(1)

# continuously send data to phone
try:
    while True:
        distance = measure_distance()
        server.send(f"{distance}\n")
        freq = 200
        time.sleep(1/freq)
except KeyboardInterrupt:
    print("\nStopping bluetooth server")
    server.send("Stopping bluetooth server")
    server.stop()

server.stop()
