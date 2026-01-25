from flask import Flask
from routes.v1 import cargarRutas_v1
from flask_mysqldb import MySQL
from config import Config
from flask_cors import CORS 
from flask_bcrypt import Bcrypt

app = Flask(__name__)
app.config.from_object(Config)
mysql = MySQL(app)
app.mysql = mysql
CORS(app,
     resources={
         r"/miproyecto/*": {
             "origins": {Config.FRONTEND_URL},
             "methods": ["GET", "POST", "PUT", "DELETE"],
             "allow_headers": {"Content-Type", "Authorization"}
         }
     })
bcrypt = Bcrypt(app)
app.bcrypt = bcrypt 

cargarRutas_v1(app)
app.run(debug=True, port=5000)