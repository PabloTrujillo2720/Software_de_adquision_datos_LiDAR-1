#Importamps las librerias necesarias
import glob
from std_msgs.msg import String
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
#Definimos variables de conteo y banderas
N = 100 # numero de escaneos a promediar
counter=0
counter1 = 0
FLAG_first_time=0
FLAG_first_time1=0
n_points=0
n_points1=0
ruta_datos = "/home/pablotrujillo/catkin_ws_final/src"
global data_sonar
def callback_sonar(data):

    #print(type(data))

    data_sonar = data
    lista_sonar = []
    lista_sonar.append(data_sonar)

    df_sonar = pd.DataFrame(lista_sonar)
    df_sonar.to_csv(ruta_datos+"/temp_sonar.csv",index=False) 
    #print(lista_sonar + "(mm)")
    #return(data_sonar)
    rospy.signal_shutdown("MORE THAN {} GRIPPER TIMEOUTS")


def listener_sonar():
    #Nodo de ROS que recibe los datos del sensor LiDAR
    rospy.init_node('ROS_to_EXCEL', anonymous=True) #El nodo de ros queda igual para sacar + de un topico 
    rospy.Subscriber('/sonar_dist', String , callback_sonar) #topico del sonar
    rospy.spin()


#if __name__ == '__main__':
    #listener_sonar()
