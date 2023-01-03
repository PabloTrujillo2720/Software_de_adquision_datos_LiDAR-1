# Software de aquision de datos LiDAR

Se utilizo un sensor laser de tecnologia LiDAR de referencia SICK_lms_500-20000 PRO, para que por medio de python se obtuvieran los datos que el sensor envia, siendo procesado atravez de ROS (Robot Operating System) en la version Noetic en ubuntu 20.04, acompañado de una camara de video y un sensor de ultrasonido, con el objetivo de realizar procesamiento y analisis estadisticos en un archivo de excel a los datos proporcionados por los distintos sensores, enfocado a la experimentacion en cuerpos de agua.

# El repositorio contiene:
- Algoritmo fuente 
  - Scripts de desarrollo (Python3)

# Requisitos de hardware
- Computador con sistema operativo ubuntu 20.04

# Requisitos de software
-   Python 3.8 :
    - Pandas
    - Numpy
    - matplotlib

## Instalacion ROS Noetic

Se procede a seguir el paso a paso que se ejemplifica en wiki de ROS.

    http://wiki.ros.org/noetic

## Clonacion de repositorio LiDAR SICK

Para poder trabajar con los sensores LiDAR de SICK, se clono el repositorio, utilizando el siguiente comando en el terminal de ubuntu:

    git clone https://github.com/SICKAG/sick_scan

## Instalación de librerías 
Como se muestra a continuación son las librerías que se utilizó para la elaboración del algoritmo

    import numpy as np
    import pandas as pd
    from matplotlib.pyplot import axis
    
Ahora se mostrará como se hace la instalación de las librerías

### Instalar Pandas

Primero, asegúrese de tener Python3.8, luego se ejecuta el comando:

    $ pip install Pandas
  
### Instalar Numpy

Seguidamente, instalar la librería numpy con el siguiente comando:

    $ pip install numpy
    
    
Para las demás librerías se realiza el mismo proceso de instalación como lo son: 

    - matplotlib
    - rospy

    $ pip install (librería a instalar)
    
## Algoritmos

Se utilizaron 5 algoritmos en python para realizar el procesamiento, donde el orden de desarrollo es:

1. datos.py
  - Nodo recolector de los datos provenientes del sensor LiDAR.
2. principal.py
  - Archivo principal donde se hacen filtrados de los datos y los respectivos llamados de los otros archivos.
3. graficas.py
  - Archivo donde se generan el analisis estadistico de los datos y las graficas de la prueba efectuada.
4. correo.py
  - Archivo donde se gestiona el envio de variables estadisticas, imagenes y datos en bruto.
5. lanzador.py
  - Archivo que sirve como actuador para cuando se recibe un ingreso de datos proveniente de la interfaz grafica.

## Interfaz grafica

Se realizo una interfaz grafica diseña apartir del framework "Flask" donde se recibiran los parametros de medicion que el usuario ingrese, junto al envio de un mensaje al correo electronico ingresado con los datos en bruto de la medicion en un archvio csv, un grafico de la medicion de prueba realizada junto a los datos estadisticos de la prueba.

La interfaz grafica se compone de 2 archivos en lenguaje python, 1 archvio css y 3 archvios html

### Aclaraciones Algoritmos

Uno de los parametros relevantes sobre el algoritmo es que se parte de realizar 100 recopilaciones de datos proporcionados por el sensor laser, apartir de ahí dichos datos se promedian para sacar un solo valor en la nube de puntos que genera, esto se hace con el objetivo de filtrar de una forma practica sichos datos, mientras que los algoritmos siguientes son de procesado y filtrado, se tiene un ejemplo de la primera seccion del algoritmo:

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
      ruta_datos = "/home/pablotrujillo/catkin_ws_final/src"
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

  
### Autores:

**Universidad de Ibagué** - **Ingeniería Electrónica** - **Semestre de Paz y Region**
-   [Luis E Peña](mailto:luis.pena@unibague.edu.co) - _Director_
-   [Harold F Murcia](http://haroldmurcia.com/) - _Co-Director_
-   [Laura Valentina Ruiz Gonzalez](mailto:2420161037@estudiantesunibague.edu.co)
-   [Pablo German Trujillo Martinez](mailto:2420171041@estudiantesunibague.edu.co)



