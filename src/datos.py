#Importamps las librerias necesarias
import glob
from operator import index
from re import X
from statistics import median_high
from sys import api_version
from matplotlib.pyplot import axis
from numpy import append, column_stack
import pandas as pd
import rospy
from sensor_msgs.msg import LaserScan
import numpy as np
import time as time 
from pathlib import Path
import os
import nodo_sonar as nsonar
#Definimos variables de conteo y banderas
N = 100 # numero de escaneos a promediar
counter=0
counter1 = 0
FLAG_first_time=0
FLAG_first_time1=0
n_points=0
n_points1=0


def callback(data):
    #Definimos variables y rutas de carpetas
    global ruta_datos
    ruta_datos = "/home/pablotrujillo/catkin_ws_final/src/pagina/src"
    global N
    global counter
    global counter1
    global FLAG_first_time
    global FLAG_first_time1
    global n_points
    global n_points1
    global M_ranges
    global M_intensities
    global bandera1
    min_angle= data.angle_min
    max_angle= data.angle_max
    bandera1 = 0

    #Se leé el archivo temporal donde se almacenan los datos recibidos de medicion
    df = pd.read_csv("temp.csv")
    angulo_min_ingresado = int(df.loc[0][0])
    angulo = angulo_min_ingresado
    #Como el sensor LiDAR toma un total de 381 puntos en 190°, se toma que cada haz de luz tiene 
    #un cambio en el angulo de barrido de 0.5°
    punto = int(angulo*2)
    angulo_max_ingresado = int(df.iloc[1][0])
    #Se guardan los valores recibidos del LiDAR
    ranges = data.ranges
    intensities = data.intensities
    #se definen vectores vacios de intensidad y rango 
    #donde se guardaran los intervalos de valores tomados del LiDAR 
    intensidades = []
    rangos = []   
    inicio_for = angulo*2
    final_for = angulo_max_ingresado*2
    for i in range(inicio_for,final_for):
        angulo = angulo + 0.5
        intensidades.append(intensities[punto])
        rangos.append(ranges[punto])
        punto = punto + 1
    #Se guardan los valores de rangos luego de haberlos promediado 100 veces (Variable N, linea 30)
    ranges_np = np.array(rangos)
    if FLAG_first_time==0:
        n_points=len(rangos)
        FLAG_first_time=1
        M_ranges=np.empty([n_points,N])
    else:
        if counter<N:
            M_ranges[:,counter]=ranges_np
            counter=counter+1
        else:
            #Se genera archivo csv de control de los datos de rango
            "Archivo de control: Toma de datos base del lugar de experimentacion"
            print("Acumulando Datos:")
            promedio_ran = np.average(M_ranges, axis=1)
            df_range = pd.DataFrame(promedio_ran)
            #Se confirma si el archivo de control existe
            name_range = ruta_datos+"/control_range.csv"
            comprobacion_range = os.path.isfile(name_range)
            #Si el archivo de control existe genera el archivo de prueba

            if comprobacion_range == True:
                print("Creando archico de prueba rango")
                df_range.to_csv(ruta_datos+"/prueba_range.csv",index=False) 
            else:
                print("Creando archivo de control rango")
                df_range.to_csv(ruta_datos+"/control_range.csv",index=False) 
                
    #Se guardan los valores de intensidades luego de haberlos promediado 100 veces (Variable N, linea 30)
    intensities_np = np.array(intensidades)
    if FLAG_first_time1==0:
        n_points1=len(intensidades)
        FLAG_first_time1=1
        M_intensities=np.empty([n_points1,N])
    
    else:
        if counter1<N:
            M_intensities[:,counter1]=intensities_np
            counter1=counter1+1
        else:

            promedio_int = np.average(M_intensities, axis=1)
            df_int = pd.DataFrame(promedio_int)
            #Se confirma si el archivo de control existe
            name_int = ruta_datos+"/control_int.csv"
            comprobacio_int = os.path.isfile(name_int)

            if comprobacio_int == True:
                #Si el archivo de control existe genera el archivo de prueba
                print("Creando archico de prueba intensidad")
                df_int.to_csv(ruta_datos+"/prueba_int.csv",index=False) 
                
            else:
                #Si el archivo de control no existe genera el archivo de prueba
                print("Creando archivo de control intensidad")
                df_int.to_csv(ruta_datos+"/control_int.csv",index=False) 

def listener():
    #Nodo de ROS que recibe los datos del sensor LiDAR
    rospy.init_node('ROS_to_EXCEL', anonymous=True)
    rospy.Subscriber('/scan', LaserScan, callback)
    time.sleep(2.2)
    nsonar.listener_sonar()


if __name__ == '__main__':
    listener()
