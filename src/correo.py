# Importamos libreríasimport os
import smtplib
import mimetypes
import ssl 
import smtplib
import numpy as np
import pandas as pd

# Importamos los módulos necesarios

from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText
from email.mime.base import MIMEBase
from email import encoders
from datetime import datetime
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

    datos= pd.read_csv("df_graficas.csv",header=0)

    global intesidad_base
    global intesidad_prueba
    global rango_base
    global rango_prueba
    global X_control
    global Y_control
    global X_prueba
    global Y_prueba

    #Se guardan los valores de control y la prueba para analisis estadistico
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


def RMSE():


    global XRMSE
    global YRMSE
    global iRMSE
    global XNSE
    global YNSE
    global iNSE

    #Calculo valores RMSE
    XRMSE = root_mean_squared_error(X_control, X_prueba)
    YRMSE = root_mean_squared_error(Y_control, Y_prueba)
    iRMSE = root_mean_squared_error(intesidad_base,intesidad_prueba)

    #Calculo valores NSE
    XNSE= NSE_(X_control, X_prueba)
    YNSE= NSE_(Y_control, Y_prueba)
    iNSE= NSE_(intesidad_base, intesidad_prueba)
    
    return(XRMSE,YRMSE,iRMSE,XNSE,YNSE,iNSE)

##################################################################

def nombre():
    #Se define el nombre que se utilizara en los archivos
    global fecha
    global name
    global name_png
    fecha = str(datetime.today())
    name = "Datos_"+ fecha + ".csv"
    name_png = "Datos_"+fecha+ ".png"

def mail():
    global nombre1
    global ruta_datos
    global valor_rmse
    global correo1
    #calculo valores estadisticos
    nombre()
    graficas()
    #Calculo valores RMSE
    XRMSE = root_mean_squared_error(X_control, X_prueba)
    YRMSE = root_mean_squared_error(Y_control, Y_prueba)
    iRMSE = root_mean_squared_error(intesidad_base,intesidad_prueba)

    #Calculo valores NSE
    XNSE= NSE_(X_control, X_prueba)
    YNSE= NSE_(Y_control, Y_prueba)
    iNSE= NSE_(intesidad_base, intesidad_prueba)
    
    RMSE()

    #Lectura de archivo con valores temporales de la pagina web 
    df = pd.read_csv("temp2.csv")
    angulo_min_ingresado = str(df.loc[0][0])
    angulo = angulo_min_ingresado
    angulo_max_ingresado = str(df.loc[1][0])
    turbidez = str(df.loc[2][0])
    nombre1 = str(df.loc[3][0])
    correo1 = str(df.loc[4][0])
    valor_rmse = str(0.5)
    #Datos envio correo electronico y cuerpo del correo
    ruta_datos = "/home/pablotrujillo/catkin_ws_final/src"
    remitente = 'Pruebaslidar@gmail.com'
    email_contrasena = 'yubhynbcjkiduxeh'
    destinatarios = correo1
    asunto =  "Prueba"+" "+ name
    cuerpo = ('Hola'+' '+nombre1+" "+'tus variables son las siguientes:\n''Valor XRMSE:' + str(XRMSE) + '\n' +'Valor YRMSE:' + str(YRMSE) + '\n' + 'Valor iRMSE:' + str(iRMSE)
                                          + '\n' + 'Valor XNSE:' + str(XNSE) +'\n'+ 'Valor YNSE:' + str(YNSE) +'\n'+ 'Valor iNSE:' + str(iNSE)+'\n'+ "Angulo minimo:"+ " "+ angulo_min_ingresado + '\n'+ "Angulo maximo:"+ " "+ angulo_max_ingresado + '\n'+ "Turbidez:"+" "+ turbidez)         
    
    ruta_adjunto1 = ruta_datos + "/Temp_graficas.csv"
    ruta_adjunto2 = ruta_datos + "/Temp_graficas.png"
    nombre_adjunto1 = name
    nombre_adjunto2 = name_png
    # Creamos el objeto mensaje
    mensaje = MIMEMultipart()
    
    # Establecemos los atributos del mensaje
    mensaje['From'] = remitente
    mensaje['To'] = "".join(destinatarios)
    mensaje['Subject'] = asunto
    
    # Agregamos el cuerpo del mensaje como objeto MIME de tipo texto
    mensaje.attach(MIMEText(cuerpo, 'plain'))
    
    # Abrimos el archivo que vamos a adjuntar
    archivo_adjunto1 = open(ruta_adjunto1, 'rb')
    archivo_adjunto2 = open(ruta_adjunto2, 'rb')
    
    # Creamos un objeto MIME base
    adjunto_MIME1 = MIMEBase('application', 'octet-stream')
    adjunto_MIME2 = MIMEBase('application', 'octet-stream')
    # Y le cargamos el archivo adjunto
    adjunto_MIME1.set_payload((archivo_adjunto1).read())
    adjunto_MIME2.set_payload((archivo_adjunto2).read())
    # Codificamos el objeto en BASE64
    encoders.encode_base64(adjunto_MIME1)
    encoders.encode_base64(adjunto_MIME2)

    # Agregamos una cabecera al objeto
    adjunto_MIME1.add_header('Content-Disposition',"attachment; filename= %s" % nombre_adjunto1)
    adjunto_MIME2.add_header('Content-Disposition',"attachment; filename= %s" % nombre_adjunto2)
    # Y finalmente lo agregamos al mensaje
    mensaje.attach(adjunto_MIME1)
    mensaje.attach(adjunto_MIME2)

    
    # Creamos la conexión con el servidor
    sesion_smtp = smtplib.SMTP('smtp.gmail.com', 587)
    
    # Ciframos la conexión
    sesion_smtp.starttls()

    # Iniciamos sesión en el servidor
    sesion_smtp.login('pruebaslidar@gmail.com','yubhynbcjkiduxeh')

    # Convertimos el objeto mensaje a texto
    texto = mensaje.as_string()

    # Enviamos el mensaje
    sesion_smtp.sendmail(remitente, destinatarios, texto)

    # Cerramos la conexión
    sesion_smtp.quit()

    print("Mensaje enviado con exito")

