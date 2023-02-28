import pandas as pd 
import time as time

global bandera

def lanzador_archivo():

    import os as os 
    from os import remove
    import time as time
    ruta = "/home/pablotrujillo/catkin_ws_final/src/pagina/src"
    bandera = 1
    while bandera == 1:
        bandera_lanzador = ruta+"/temp.csv"
        comprobacio_lanzador = os.path.isfile(bandera_lanzador)
        print("Existen los archivos de control:",comprobacio_lanzador)

        if comprobacio_lanzador == True:
            from codigos import principal
            from codigos import datos
            from codigos import graficas
            from codigos import correo
            import principal
            print("Entrando a principal-----------")
            #time.sleep(3)
            principal.__main__()
            print("Saliendo a principal-----------")
            #time.sleep(5)
            print("existe.... Eliminando")
            #time.sleep(3)
            remove("temp.csv")
            print("archivo eliminado")

            os.system("python3 lanzador.py")

            bandera = 0

            time.sleep(2)

            
            

        if comprobacio_lanzador == False:
            
            print("Esperando archivo temp.csv...")
            time.sleep(5)

lanzador_archivo()
