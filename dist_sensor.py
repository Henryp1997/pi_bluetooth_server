from gpiozero import DistanceSensor
import time

sensor = DistanceSensor(echo=17, trigger=27, threshold_distance=0.5, max_distance=2)

def measure_distance():
    return sensor.distance
