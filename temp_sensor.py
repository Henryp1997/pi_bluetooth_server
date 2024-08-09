import time
import adafruit_dht
import board

temp_sensor_pin = board.D4
dht_device = adafruit_dht.DHT11(temp_sensor_pin)

def get_temp_humidity():
    try:
        temperature_c = dht_device.temperature

        humidity = dht_device.humidity

        return temperature_c, humidity
    except RuntimeError as err:
        temperature_c, humidity = None, None
        print(err.args[0])

    return temperature_c, humidity

if __name__ == "__main__":
    while True:
        try:
            t, h = get_temp_humidity()
        except:
            t, h = None, None
        print(t, h)
        time.sleep(2)
        
