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
global data
def callback_sonar(data):
    # Imprimimos los datos recibidos
    rospy.loginfo(data)
    X = []
    X.append(data)
    df = pd.DataFrame(X)
    print("Creando temp sonar")
    df.to_csv("/home/pablotrujillo/catkin_ws_final/src/pagina/src/temp_sonar.csv",index=False)
    rospy.signal_shutdown("MORE THAN {} GRIPPER TIMEOUTS")

def listener_sonar():
    rospy.init_node('ROS_to_EXCEL', anonymous=True)
    # Suscripción al tópico "/Sonar_dist"
    rospy.Subscriber("/sonar_dist", String , callback_sonar)
    # Esperamos un tiempo para recibir algunos mensajes
    time.sleep(1)

