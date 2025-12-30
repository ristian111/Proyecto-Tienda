from flask import Flask
from routes import cargarRutas
from flask_mysqldb import MySQL
from config import Config
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)
app.mysql = mysql
bcrypt = Bcrypt(app)
app.bcrypt = bcrypt

cargarRutas(app)
app.run(debug=True, port=5000)