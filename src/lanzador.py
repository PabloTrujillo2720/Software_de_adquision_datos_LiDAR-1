import pandas as pd 
import time as time

valor1 = 0
"""df = pd.read_csv("temp.csv")

valor1 = int(df.iloc[2])

print(valor1)"""

def lanzador_numero(): 

    if valor1 == 0:

        print("No ha entrado")
        time.sleep(3)
    
    if valor1 == 1:

        import principal

        principal.__main__()


def lanzador_archivo():

    import os as os 
    from os import remove
    import time as time
    ruta = "/home/pablotrujillo/catkin_ws_final/src"
    while True:
        bandera_lanzador = ruta+"/temp.csv"
        comprobacio_lanzador = os.path.isfile(bandera_lanzador)
        print("Existen los archivos de control:",comprobacio_lanzador)

        if comprobacio_lanzador == True:
            import principal
            import datos_sonar
            print("Entrando a principal-----------")
            datos_sonar.listener_sonar()
            #time.sleep(3)
            principal.__main__()
            print("Saliendo a principal-----------")
            #time.sleep(5)
            print("existe.... Eliminando")
            #time.sleep(3)
            remove("temp.csv")
            print("archivo eliminado")
            

        if comprobacio_lanzador == False:
            
            print("Esperando archivo temp.csv...")
            time.sleep(5)

lanzador_archivo()


