# Setup para, obviamente, crear el entorno virtual y descargar las dependencias.
# ¿Quien es diego sniper?
# Los prints estan en ingles culpa de las convenciones convenciosas.
# OJO, esto SOLO se usa si vas a correr el programa SIN docker.

import subprocess
import sys
import os


# Instalar dependencias
def install_requirements():
    print("Installing requirements from requirements.txt...")
    if not os.path.exists("requirements.txt"):
        print("Error: requirements.txt not found in the current directory.")
        return
        
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", "-r", "requirements.txt"])
        print("Requirements installed successfully.\n")
    except subprocess.CalledProcessError as e:
        print(f"Failed to install requirements: {e}")
        sys.exit(1)

def setup_database():
    print("Setting up the database configuration...")
    
    # Si no encuentra un .env, crea uno basico en base a la informacion de aqui abajo.
    if not os.path.exists(".env"):
        print("Creating default .env file based on typical config...")
        with open(".env", "w") as f:
            f.write("MYSQL_HOST=localhost\n")
            f.write("MYSQL_USER=root\n")
            f.write("MYSQL_PASSWORD=\n")
            f.write("MYSQL_DATABASE=tienda_db\n")
            f.write("MYSQL_PORT=3306\n")
            f.write("API_KEY=your_api_key_here\n")
            f.write("FRONTEND_URL=http://localhost:3000\n")
            f.write("SECRET_KEY=your_secret_key_here\n")
        print(".env created with default settings. Please review and update it as needed.\n")
    else:
        print(".env file already exists.\n")

    try:
        from dotenv import load_dotenv
        import mysql.connector

        load_dotenv()
        
        db_host = os.getenv("MYSQL_HOST", "localhost")
        db_user = os.getenv("MYSQL_USER", "root")
        db_password = os.getenv("MYSQL_PASSWORD", "")
        db_name = os.getenv("MYSQL_DATABASE", "tienda_db")
        db_port = int(os.getenv("MYSQL_PORT", 3306))
        
        print(f"Connecting to MySQL on {db_host}:{db_port} as user '{db_user}'...")
        connection = mysql.connector.connect(
            host=db_host,
            user=db_user,
            password=db_password,
            port=db_port
        )
        cursor = connection.cursor()
        
        cursor.execute(f"CREATE DATABASE IF NOT EXISTS `{db_name}`;")
        print(f"Database '{db_name}' is ready.\n")
        
        cursor.close()
        connection.close()
        
    except ImportError as e:
        print(f"Warning: A required module is missing ({e}). Skipping python DB connection test.")
        print("Since you are using Docker, `docker-compose up` will automatically create the database.")
    except Exception as e:
        print(f"Warning: Could not connect to MySQL to verify database: {e}")
        print("If you are using Docker, remember to start it first with `make up`.")

if __name__ == '__main__':
    install_requirements()
    setup_database()
    print("Setup finished! You can now start your Docker containers with: make up")
