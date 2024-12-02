#from flask import Flask, request, jsonify
#from flask_sqlalchemy import SQLAlchemy
#from dotenv import load_dotenv
#import os

# Cargar variables de entorno
#load_dotenv()

#app = Flask(__name__)

# Configuración para conectarse a la base de datos
#app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URL')
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

from flask import Flask, jsonify
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)

# Configuración de la base de datos
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root:19590102Ferari@104.248.127.43:3309/estudiantes'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

# Modelo Estudiante
class Estudiante(db.Model):
    __tablename__ = 'estudiante'
    
    no_control = db.Column(db.String(20), primary_key=True)  # Clave primaria
    nombre = db.Column(db.String(100), nullable=False)
    ap_paterno = db.Column(db.String(100), nullable=False)
    ap_materno = db.Column(db.String(100), nullable=False)
    semestre = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"<Estudiante {self.no_control}>"

# Rutas
@app.route('/estudiantes', methods=['GET'])
def obtener_estudiantes():
    try:
        estudiantes = Estudiante.query.all()
        resultado = [
            {
                "no_control": estudiante.no_control,
                "nombre": estudiante.nombre,
                "ap_paterno": estudiante.ap_paterno,
                "ap_materno": estudiante.ap_materno,
                "semestre": estudiante.semestre
            } 
            for estudiante in estudiantes
        ]
        return jsonify(resultado), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Inicializar la base de datos usando el evento got_first_request
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
