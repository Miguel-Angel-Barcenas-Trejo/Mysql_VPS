from flask import Flask, request, jsonify
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
@app.route('/estudiantes', methods=['GET', 'POST'])
def manejar_estudiantes():
    if request.method == 'GET':
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

    elif request.method == 'POST':
        try:
            datos = request.get_json()
            nuevo_estudiante = Estudiante(
                no_control=datos['no_control'],
                nombre=datos['nombre'],
                ap_paterno=datos['ap_paterno'],
                ap_materno=datos['ap_materno'],
                semestre=datos['semestre']
            )
            db.session.add(nuevo_estudiante)
            db.session.commit()
            return jsonify({"mensaje": "Estudiante agregado con éxito"}), 201
        except Exception as e:
            return jsonify({"error": str(e)}), 500


@app.route('/estudiantes/<string:no_control>', methods=['GET', 'PUT', 'PATCH', 'DELETE'])
def manejar_estudiante(no_control):
    estudiante = Estudiante.query.get(no_control)
    
    if not estudiante:
        return jsonify({"error": "Estudiante no encontrado"}), 404

    if request.method == 'GET':
        try:
            resultado = {
                "no_control": estudiante.no_control,
                "nombre": estudiante.nombre,
                "ap_paterno": estudiante.ap_paterno,
                "ap_materno": estudiante.ap_materno,
                "semestre": estudiante.semestre
            }
            return jsonify(resultado), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method in ['PUT', 'PATCH']:
        try:
            datos = request.get_json()
            if 'nombre' in datos:
                estudiante.nombre = datos['nombre']
            if 'ap_paterno' in datos:
                estudiante.ap_paterno = datos['ap_paterno']
            if 'ap_materno' in datos:
                estudiante.ap_materno = datos['ap_materno']
            if 'semestre' in datos:
                estudiante.semestre = datos['semestre']
            db.session.commit()
            return jsonify({"mensaje": "Estudiante actualizado con éxito"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

    elif request.method == 'DELETE':
        try:
            db.session.delete(estudiante)
            db.session.commit()
            return jsonify({"mensaje": "Estudiante eliminado con éxito"}), 200
        except Exception as e:
            return jsonify({"error": str(e)}), 500

# Inicializar la base de datos usando el evento got_first_request
with app.app_context():
    db.create_all()

if __name__ == '__main__':
    app.run(debug=True)
