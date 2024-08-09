from PyQt6 import QtWidgets, QtCore
import pyqtgraph as pg
from random import randint

dummy_data = [0, 0, 0, 0, 0, 0.0, 0.6931471805599453, 1.0986122886681098, 1.3862943611198906, 1.6094379124341003, 1.6094379124341003, 1.6094379124341003, 1.3862943611198906, 1.0986122886681098, 0.6931471805599453, 0.0, 0, 0, 0, 0, 0, -5, 5, 15, 25, 35, 25, 15, 5, -5, -15, -12, -9, -6, -3, 0, 0, 0, 0, 0, 0, 0.0, 1.3862943611198906, 2.1972245773362196, 2.772588722239781, 3.2188758248682006, 3.2188758248682006, 3.2188758248682006, 3.2188758248682006, 3.2188758248682006, 3.2188758248682006, 2.772588722239781, 2.1972245773362196, 1.3862943611198906, 0.0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]

class MainWindow(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.plot_graph = pg.PlotWidget()
        self.setCentralWidget(self.plot_graph)
        self.plot_graph.setBackground("w")

        # graph styling
        self.plot_graph.setTitle("Sensor data")
        self.plot_graph.setLabel("left", "Sensor data")
        self.plot_graph.setLabel("bottom", "Time")
        self.plot_graph.showGrid(x=True, y=True)
        pen = pg.mkPen(color=(255, 0, 0), width=5)
        
        # data to be plotted
        self.time = list(range(100))
        self.sensor_data = [0 for i in range(100)]

        # line reference
        self.line = self.plot_graph.plot(
            self.time,
            self.sensor_data,
            name="Sensor",
            pen=pen,
        )

        # add a timer to simulate new sensor measurements
        self.timer = QtCore.QTimer()
        self.timer.setInterval(15)
        self.timer.timeout.connect(self.update_plot)
        self.timer.start()

        self.data_index = 0

    def update_plot(self):
        self.time = self.time[1:]
        self.time.append(self.time[-1] + 1)

        self.sensor_data = self.sensor_data[1:]

        self.sensor_data.append(dummy_data[self.data_index % 75])
        self.data_index += 1
        # self.sensor_data.append(randint(20, 40))

        # limit size of lists
        # self.time = self.time[-100:]
        # self.sensor_data = self.sensor_data[-100:]

        self.line.setData(self.time, self.sensor_data)

app = QtWidgets.QApplication([])
main = MainWindow()
main.setWindowTitle("Real-time sensor data")
main.show()
app.exec()