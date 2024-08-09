from socket import socket, AF_BLUETOOTH, SOCK_STREAM, BTPROTO_RFCOMM
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys, threading, time

# global variables
x_array = []
y_array = []
refresh_rate = 200 # Hz

def read_sensor():
    while True:
        if event.is_set():
            # stop the thread
            break

        # buffer size in bytes is 1024, encoding scheme is utf-8
        data = server.recv(1024).decode("utf-8")
        try:
            data = float(data.split("\n")[0])
            y_array.append(data)
            x_array.append(dt.datetime.now().strftime('%H:%M:%S.%f'))
        except Exception as e:
            print(e)

        time.sleep(1/refresh_rate)

def animate(i, x_array, y_array, ax, data_max_size):
    # limit size of data
    x_array = x_array[-1 * data_max_size:]
    y_array = y_array[-1 * data_max_size:]

    # draw x and y lists
    ax.clear()
    ax.plot(x_array, y_array)

    # format plot (remove ticks and tick values for now)
    plt.xticks([], [])
    plt.yticks([], [])
    plt.ylabel('Sensor data')

if __name__ == "__main__":
    # connect to bluetooth server
    pizero_mac = "B8:27:EB:A5:86:BC"

    server = socket(AF_BLUETOOTH, SOCK_STREAM, BTPROTO_RFCOMM)

    # connect to raspberry pi
    try:
        # default port from BlueDot server is 1
        server.connect((pizero_mac, 1))
    except TimeoutError:
        print("Bluetooth server not available")
        sys.exit()

    # server script is set to begin sending data only when
    # a message has been received from this end
    server.send(("").encode("utf-8"))

    # start sensor reading thread
    thread = threading.Thread(target=read_sensor)
    thread.start()
    event = threading.Event() # used to stop thread

    # create figure for plotting
    fig = plt.figure()
    ax = fig.add_subplot(1, 1, 1)

    # Set up plot to call animate() function periodically
    ani = animation.FuncAnimation(fig, animate, fargs=(x_array, y_array, ax, 100), interval=1/refresh_rate)
    plt.show()

    # close thread
    event.set()
    thread.join()
