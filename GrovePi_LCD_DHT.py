from grove_rgb_lcd import *
import time
import pymysql
import sys
import math
import grovepi  # Asegúrate de importar explícitamente grovepi en Python 3.5

# Configuración del sensor DHT
dht_sensor_port = 7
dht_sensor_type = 0

# Conexión a la base de datos
try:
    conn = pymysql.connect(
        host="localhost",
        user="sensoruser",
        password="1234",
        database="sensores"
    )
    cursor = conn.cursor()
except pymysql.MySQLError as e:
    print("Error conectando a la base de datos: {}".format(e))
    sys.exit(1)

# Configura el color inicial de la pantalla
setRGB(0, 255, 0)

# Bucle principal
while True:
    try:
        # Leer temperatura y humedad del sensor
        [temp, hum] = grovepi.dht(dht_sensor_port, dht_sensor_type)

        print("Temp =", temp, "°C / Humedad =", hum, "%")

        # Verifica si las lecturas son válidas
        if math.isnan(temp) or math.isnan(hum):
            raise TypeError("Error: Valor NaN")

        # Mostrar en pantalla LCD
        setText_norefresh("Temp: {}C\nHum: {}%".format(temp, hum))

        # Insertar en base de datos
        cursor.execute(
            "INSERT INTO lecturas (temperatura, humedad) VALUES (%s, %s)",
            (temp, hum)
        )
        conn.commit()

        time.sleep(5)

    except (IOError, TypeError) as e:
        print("Error de lectura:", e)
        time.sleep(2)

    except pymysql.MySQLError as e:
        print("Error en base de datos: {}".format(e))
        time.sleep(2)
        
