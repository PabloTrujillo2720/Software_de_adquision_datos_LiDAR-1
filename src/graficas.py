from itertools import count
from lib2to3.pgen2.pgen import DFAState
from operator import index
from re import A
import re
from readline import append_history_file
from turtle import clear
import pandas as pd
import matplotlib.pyplot as plt
import math 
import numpy as np 
import csv
from datetime import datetime

global ruta_datos
#Ruta del espacio de trabajo de ROS
ruta_datos = "/home/pablotrujillo/catkin_ws_final/src"

def root_mean_squared_error(x,y):
    n=len(x.T)
    error = x.T-y.T
    error_2 = np.power(error,2)
    MSE = np.sum(error_2)/n
    RMSE = np.sqrt(MSE)
    return RMSE


def NSE_(Xobs,Xsim):
    num = np.sum( np.power(Xobs-Xsim,2))
    den = np.sum( np.power(Xobs-np.mean(Xobs),2))
    NSE = 1 - (num/den)
    return NSE




def graficas():

    angulo_max = 55
    angulo_min = -55
    #Lectura de archivo Temporal
    datos= pd.read_csv("df_graficas.csv",header=0)

    global intesidad_base
    global intesidad_prueba
    global rango_base
    global rango_prueba
    global X_control
    global Y_control
    global X_prueba
    global Y_prueba
    #Se leen los datos de control y pruebas para calculos estadisticos
    intesidad_base = np.array(datos[["Intensidad_base"]]).T
    rango_base = np.array( datos[["Rango_base"]] ).T
    intesidad_prueba = np.array(datos[["Intensidad_prueba"]]).T
    rango_prueba = np.array(datos[["Rango_prueba"]]).T

    num_datos = len(datos [["Intensidad_base"]])
    angulo_barrido= angulo_max - angulo_min
    beta = np.linspace(angulo_min, angulo_max, num_datos)

    #Determinar Perfiles: X y Y
    X_control = rango_base*np.sin(beta*np.pi/180.0)
    Y_control = -rango_base*np.cos(beta*np.pi/180.0)

    X_prueba = rango_prueba*np.sin(beta*np.pi/180.0)
    Y_prueba = -rango_prueba*np.cos(beta*np.pi/180.0)

    #### Almacene los datos en EXCEL
    datos['X_control']=pd.DataFrame(X_control).T
    datos['Y_control']=pd.DataFrame(Y_control).T
    datos['X_prueba']=pd.DataFrame(X_prueba).T
    datos['Y_prueba']=pd.DataFrame(Y_prueba).T

    datos.to_csv(ruta_datos + "/df_graficas.csv", index=False)
    datos.to_csv(ruta_datos + "/Temp_graficas.csv", index=False)
    datos.to_csv(ruta_datos + name, index=False)
    #Configuracion de graficas y generacion de archivo .png
    plt.figure()
    plt.plot(X_control.T,Y_control.T,'.',label='Control')
    plt.plot(X_prueba.T,Y_prueba.T,'.',label='Prueba')
    plt.grid()
    plt.legend()
    plt.xlabel("X [m]")
    plt.ylabel("Y [m]")
    #solo tanque
    plt.xlim(-1.5, 0.8)#-2.5, 10
    plt.ylim(-1.8, -0.6)#-2.0, 0.5
    #toma entera
    #plt.xlim(-2.5, 10.0)#-2.5, 10
    #plt.ylim(-2.0, -0.5)#-2.0, 0.5
    plt.savefig("Temp_graficas"+".png", dpi=600)
    plt.savefig(name_png, dpi=600)
    #plt.show()

def nombre():
    #Nombre que se utilizara en los archivos 
    global fecha
    global name
    global name_png
    fecha = str(datetime.today())
    name = "Datos_"+ fecha + ".csv"
    name_png = "Datos_"+ fecha + ".png"

def RMSE():

    #Calculos RMSE
    XRMSE = root_mean_squared_error(X_control, X_prueba)
    YRMSE = root_mean_squared_error(Y_control, Y_prueba)
    iRMSE = root_mean_squared_error(intesidad_base,intesidad_prueba)

    #Calculos NSE
    XNSE= NSE_(X_control, X_prueba)
    YNSE= NSE_(Y_control, Y_prueba)
    iNSE= NSE_(intesidad_base, intesidad_prueba)

    return(XRMSE,YRMSE,iRMSE,XNSE,YNSE,iNSE)

nombre()
graficas()
RMSE()

