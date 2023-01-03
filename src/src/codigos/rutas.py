import pandas as pd
from flask import render_template, request, url_for, redirect, flash, abort
from codigos import app, mail
from flask_mail import Message
import os as os
from sys import path
global bandera 
bandera = [0]
@app.route('/')
@app.route('/inicio')
def inicio():
    
    print("inicio")
    return render_template("inicio.html", title='Inicio', segment='Inicio')

@app.route('/prueba', methods=['GET','POST'])
def prueba():
    
    if request.method == 'POST':
        print("prueba")
        botones = str(request.form.get('botones'))

        if botones == "prueba_instantanea":     # codigo de las pruebas instantanias
            print("Se seleciono el boton de: ", botones)

            data_name = str(request.form.get('data_name'))
            data_correo = str(request.form.get('data_correo'))
            
            x1 = []
            x2 = []
            lista = []
            lista_tem = []
            bandera = [1]
            dato_1 = int(request.form.get('dato_1'))
            dato_2 = int(request.form.get('dato_2'))
            dato_3 = int(request.form.get('dato_3'))
            

            print("El correo es: ", data_name)
            print("El correo es: ", data_correo)
            print("El Angulo minimo es: ", dato_1)
            print("El Angulo maximo es: ", dato_2)
            print("El Turbiedad es: ", dato_3)
            print("Boton: ", botones)

            x1 = []
            x2 = []
            x3 = []
            name = []
            correo = []
            lista = []
            lista_tem = []

            import pandas as pd

            x1.append(dato_1)
            x2.append(dato_2)
            x3.append(dato_3)
            name.append(data_name)
            correo.append(data_correo)


            lista.extend(x1)
            lista.extend(x2)
            lista.extend(x3)
            lista.extend(bandera)

            lista_tem.extend(x1)
            lista_tem.extend(x2)
            lista_tem.extend(x3)
            lista_tem.extend(name)
            lista_tem.extend(correo)

            #print(lista)

            df = pd.DataFrame(lista)
            df_tem = pd.DataFrame(lista_tem)

            df.to_csv("temp.csv",index=False)
            df_tem.to_csv("temp2.csv",index=False)
            df.to_csv("/home/pablotrujillo/catkin_ws_final/src/temp.csv",index=False)
            df_tem.to_csv("/home/pablotrujillo/catkin_ws_final/src/temp2.csv",index=False)
            import time as time
            #time.sleep(10)

            lista[3] = 0
            df = pd.DataFrame(lista)
            df.to_csv("temp.csv",index=False)
            df.to_csv("/home/pablotrujillo/catkin_ws_final/src/temp.csv",index=False)
            


            msg = Message('Variables de tu prueba.',
                          sender='noreply@demo.com',
                          recipients=[data_correo])

            msg.body = "Hola "+ str(data_name) +", tus variables son las siguientes: \n" + "Angulo minimo: " + str(dato_1) + "\nAngulo maximo: " + str(dato_2)+ "\nTurbiedad: " + str(dato_3)
            
            with open("../data/Datos_2022-10-19 10_13_56.990890.csv", encoding="utf8") as fp:
                msg.attach("Base de datos.csv", "Base de datos/csv", fp.read())

            with app.open_resource("../../data/imageen.png") as fp:
                msg.attach("imagen.png", "imagen/png", fp.read())

            #mail.send(msg)

            info= "Datos recibidos y correo enviado"

        if botones == "prueba_video":   # codigo que se comunica con la raspberry
            print("Se seleciono el boton de: ", botones)

            info= "Boton de raspberry"

        return render_template("prueba.html", info=info, title='Prueba', segment='Prueba')

    return render_template("prueba.html", title='Prueba', segment='Prueba')