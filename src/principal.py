import pandas as pd
import time as time 
import numpy as np
#from sklearn.metrics import mean_squared_error
import math
import os
import sys
#import now
from datetime import datetime
#Codigos locales
import datos as dl4

global ruta_datos
#Ruta del espacio de trabajo de ROS
ruta_datos = "/home/pablotrujillo/catkin_ws_final/src"
def control():
    #Llamamos a Callback desde datos
    dl4.listener()

def filtrado():
    #Se filttran los 2 archivos de datos de control para hacer uno nuevo
    df1 = pd.read_csv("control_int.csv")
    df2 = pd.read_csv("control_range.csv")
    df_f= pd.DataFrame() 
    df_f = df_f.T
    df_f = pd.concat([df1,df2], axis = 1,ignore_index=True)
    df_f.to_csv(ruta_datos + "/control_filtrado.csv",index=False)

def nombre():
    #Se define el nombre que tendra el archivo generado
    global fecha
    global name
    fecha = str(datetime.today())
    name = "Datos_"+ fecha + ".csv"
    return name

def pruebas():

    #Concatena archivos de excel y define nombres de las columnas
    #archivo base, si ya existe un archvio de control no se modifica
    df_base = pd.read_csv("control_filtrado.csv")
    #Archivos de la nueva medicion
    df1 = pd.read_csv("prueba_int.csv")
    df2 = pd.read_csv("prueba_range.csv")

    #print(df1,df2)
    global df
    df = pd.DataFrame() 
    df = df.T

    df = pd.concat([df1,df2], axis = 1,ignore_index=True)
    #Modificar el nombre del alchivo csv cuando se haga una nueva prueba
    df.to_csv(ruta_datos+ "/control_filtrado.csv",index=False)
    #Renombramos las columnas
    df = pd.concat([df_base,df], axis = 1,ignore_index=True)
    df=df.rename(columns={df.columns[0]:"Intensidad_base"})
    df=df.rename(columns={df.columns[1]:"Rango_base"})
    df=df.rename(columns={df.columns[2]:"Intensidad_prueba"})
    df=df.rename(columns={df.columns[3]:"Rango_prueba"})

def excel():
    #Generamos archivo csv temporal para los calculos estadisticos en el archivo de graficas
    print("Generando Archivos Excel")
    df_final = df.to_csv(ruta_datos+"/df_graficas.csv",index=False)
    #df_final = df.to_csv("/home/pablotrujillo/ros_catkin_ws/src/laser/src/"+name,index=False)
    print("Nombre de archivo excel:",name)
    
#Archivo main donde se hacen los llamados de los distintos archivos python
def __main__():
    #llamada para recolectar datos del LiDAR y generar archivos
    control()
    #Comprobacion de si existe el archivo de control, si existe, genera el archivo de la prueba
    name_control = ruta_datos+"/control_int.csv"
    comprobacio_control = os.path.isfile(name_control)
    print("Existen los archivos de control:",comprobacio_control)

    if comprobacio_control == True:

        filtrado()

    name_prueba = ruta_datos+ "/prueba_int.csv"
    comprobacio_prueba = os.path.isfile(name_prueba)
    print("Existen los archivos de prueba:",comprobacio_prueba)
    control()
    #comprueba si el archivo de prueba fue generado para realizar el procesamiento grafico, estadistico
    #Y el correspondiente envio del correo electronico.
    if comprobacio_prueba == True:
        import graficas as gf4
        import correo as mail4

        filtrado()
        nombre()
        pruebas()
        excel()
        gf4.graficas()
        mail4.mail()

#__main__()