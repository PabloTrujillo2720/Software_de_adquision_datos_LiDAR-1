# ROS_TO_EXCEL

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

Se utilizaron 3 algoritmos en python para realizar el procesamiento, donde se enumeran como paso 1, paso 2 y paso 3.

Dicho orden tiene como intencion generar 2 archivos de excel en el paso 1 y unirlo en el paso 2, donde el paso 3 se trata de un archivo que realiza cientos calculos estadisticos y combinacion de mas datos de requerirse.

### Aclaraciones Algoritmos

Uno de los parametros relevantes sobre el algoritmo es que se parte de realizar 200 recopilaciones de datos proporcionados por el sensor laser, apartir de ahí dichos datos se promedian para sacar un solo valor en la nube de puntos que genera, esto se hace con el objetivo de filtrar de una forma practica sichos datos, mientras que los algoritmos siguientes son de procesado y filtrado, se tiene un ejemplo de la primera seccion del algoritmo:

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
                df_range = pd. DataFrame(promedio_ran)
                df_range.to_csv("/home/pablotrujillo/ros_catkin_ws/src/laser/datos_excel/datos_ran1.csv",index=False)  

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









































### Autores:

**Universidad de Ibagué** - **Ingeniería Electrónica** - **Semestre de Paz y Region**
-   [Luis E Peña](mailto:luis.pena@unibague.edu.co) - _Director_
-   [Harold F Murcia](http://haroldmurcia.com/) - _Co-Director_
-   [Laura Valentina Ruiz Gonzalez](mailto:2420161037@estudiantesunibague.edu.co)
-   [Pablo German Trujillo Martinez](mailto:2420171041@estudiantesunibague.edu.co)



