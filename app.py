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
         r"/*": {
             "origins": "*",
             "methods": ["GET", "POST", "PUT", "DELETE"],
             "allow_headers": {"Content-Type", "Authorization"}
         }
     })
bcrypt = Bcrypt(app)
app.bcrypt = bcrypt 

cargarRutas_v1(app)
# Expone el puerto
if __name__ == '__main__':
    app.run(host="0.0.0.0", debug=True, port=5000)