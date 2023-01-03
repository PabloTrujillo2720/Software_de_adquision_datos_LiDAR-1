from flask import Flask
from flask_mail import Mail

app = Flask(__name__)
app.config['MAIL_SERVER'] = 'smtp.googlemail.com'
app.config['MAIL_PORT'] = 587
app.config['MAIL_USE_TLS'] = True
app.config['MAIL_USERNAME'] = ('pruebaslidar@gmail.com')      #'correo'
app.config['MAIL_PASSWORD'] = ('yubhynbcjkiduxeh')        # 'contraseña'
mail = Mail(app)

from codigos import rutas