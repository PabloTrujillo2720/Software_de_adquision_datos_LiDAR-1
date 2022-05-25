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

N = 200 # numero de escaneos a promediar
counter=0
counter1 = 0
FLAG_first_time=0
FLAG_first_time1=0
n_points=0
n_points1=0

def callback(data):
    global N
    global counter
    global counter1
    global FLAG_first_time
    global FLAG_first_time1
    global n_points
    global n_points1
    global M_ranges
    global M_intensities

    min_angle= data.angle_min
    max_angle= data.angle_max
    ranges = data.ranges
    intensities = data.intensities


    #Ciclo de los rangos:
    #print(dir(data))
    #print("typesssssssssssss",type(data.ranges))
    #print(dir(data.ranges))
    ranges_np = np.array(ranges)
    if FLAG_first_time==0:
        n_points=len(ranges)
        FLAG_first_time=1
        M_ranges=np.empty([n_points,N])
        #print("El escaneo tiene ", n_points, " puntos" )
    else:
        if counter<N:
            M_ranges[:,counter]=ranges_np
            counter=counter+1
        else:
            print("Datos Acumulados:")
            promedio_ran = np.average(M_ranges, axis=1)
            #print("Ranges",promedio)}
            df_range = pd. DataFrame(promedio_ran)
            #llevar_este al excel
            df_range.to_csv("/home/pablotrujillo/ros_catkin_ws/src/laser/datos_excel/datos_ran1.csv",index=False)  

    #Ciclo Intensidades
    #print(dir(data))
    #print("typesssssssssssss",type(data.intensities))
    #print(dir(data.intensities))
    intensities_np = np.array(intensities)
    if FLAG_first_time1==0:
        n_points1=len(intensities)
        FLAG_first_time1=1
        M_intensities=np.empty([n_points1,N])
        #print("El escaneo tiene ", n_points1, " puntos" )
    else:
        if counter1<N:
            M_intensities[:,counter1]=intensities_np
            counter1=counter1+1
        else:
            #print("Datos Acumulados:")
            promedio_int = np.average(M_intensities, axis=1)
            #print("Intensities",promedio1)

            #llevar_este al excel

            #df1 = type(promedio_int)
            df_int = pd.DataFrame(promedio_int)
            #df1 = pd.DataFrame("Intensidad:", promedio_int)

            df_int.to_csv("/home/pablotrujillo/ros_catkin_ws/src/laser/datos_excel/datos_int1.csv",index=False) 
    




def listener():

    # In ROS, nodes are uniquely named. If two nodes with the same
    # name are launched, the previous one is kicked off. The
    # anonymous=True flag means that rospy will choose a unique
    # name for our 'listener' node so that multiple listeners can
    # run simultaneously.
    rospy.init_node('ROS_to_EXCEL', anonymous=True)

    rospy.Subscriber('/scan', LaserScan, callback)

    # spin() simply keeps python from exiting until this node is stopped
    rospy.spin()

if _name_ == '_main_':
    listener()
