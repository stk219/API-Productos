import os
import sys
from flask import Flask, request, jsonify,Response
from flask_sqlalchemy import SQLAlchemy
from config import config
from collections import OrderedDict
import json
from flask_cors import CORS


# Asegurarse de que src esté en el path para importar la configuración
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), 'src')))

# Inicialización de la app y la configuración
app = Flask(__name__)
CORS(app)
app.config.from_object(config['development'])

# Inicialización de la base de datos
db = SQLAlchemy(app)

# Definición del modelo Producto (compatible con Supabase/PostgreSQL)
class Producto(db.Model):
    __tablename__ = 'productos'

    id_prod = db.Column(db.Integer, primary_key=True)
    nombre = db.Column(db.String(100), nullable=False)
    cantidad = db.Column(db.Integer, nullable=False)
    precio = db.Column(db.Float, nullable=False)
    imagen = db.Column(db.String(100), nullable=False)


# Listar productos
@app.route('/productos', methods=['GET'])
def listar_productos():
    try:
        productos = Producto.query.all()
        lista = [
            OrderedDict([
                ('id_prod', p.id_prod),
                ('nombre', p.nombre),
                ('cantidad', p.cantidad),
                ('precio', p.precio),
                ('imagen', p.imagen)
            ]) for p in productos
        ]
        return Response(json.dumps(lista), mimetype='application/json')
    except Exception as ex:
        return jsonify({'mensaje': f"Error al listar productos: {str(ex)}"}), 500

# Ver un producto por ID
@app.route('/productos/<int:id_prod>', methods=['GET'])
def ver_producto(id_prod):
    try:
        producto = Producto.query.get(id_prod)
        if producto:
            datos = OrderedDict([
                ('id_prod', producto.id_prod),
                ('nombre', producto.nombre),
                ('cantidad', producto.cantidad),
                ('precio', producto.precio),
                ('imagen', producto.imagen)    
            ])
            return Response(json.dumps(datos), mimetype='application/json')
        else:
            return jsonify({'mensaje': "Producto no encontrado"}), 404
    except Exception as ex:
        return jsonify({'mensaje': "Error", 'detalles': str(ex)}), 500

# Crear nuevo producto
@app.route('/productos', methods=['POST'])
def registrar_producto():
    try:
        data = request.get_json()
        producto = Producto(
            nombre=data['nombre'],
            cantidad=data['cantidad'],
            precio=data['precio'],
            imagen=data['imagen']
        )
        db.session.add(producto)
        db.session.commit()
        return jsonify({'mensaje': "Producto registrado correctamente"})
    except Exception as ex:
        return jsonify({'mensaje': "Error al registrar producto", 'detalle': str(ex)}), 500

# Actualizar un producto
@app.route('/productos/<int:id_prod>', methods=['PUT'])
def actualizar_producto(id_prod):
    try:
        data = request.get_json()
        producto = Producto.query.get(id_prod)

        if not producto:
            return jsonify({'mensaje': "Producto no encontrado"}), 404

        required_fields = ['nombre', 'cantidad', 'precio']
        missing_fields = [f for f in required_fields if f not in data]
        if missing_fields:
            return jsonify({'mensaje': "Campos faltantes", 'detalles': f"Faltan: {', '.join(missing_fields)}"}), 400

        producto.nombre = data['nombre']
        producto.cantidad = data['cantidad']
        producto.precio = data['precio']
        producto.imagen = data['imagen']
        db.session.commit()

        return jsonify({'mensaje': "Producto actualizado correctamente"})
    except Exception as ex:
        return jsonify({'mensaje': "Error al actualizar producto", 'detalle': str(ex)}), 500

# Eliminar un producto
@app.route('/productos/<int:id_prod>', methods=['DELETE'])
def eliminar_producto(id_prod):
    try:
        producto = Producto.query.get(id_prod)
        if producto:
            db.session.delete(producto)
            db.session.commit()
            return jsonify({'mensaje': f"Producto con ID {id_prod} eliminado"})
        else:
            return jsonify({'mensaje': "Producto no encontrado"}), 404
    except Exception as ex:
        return jsonify({'mensaje': "Error al eliminar producto", 'detalle': str(ex)}), 500

# Inicialización
if __name__ == '__main__':
    port = int(os.environ.get("PORT", 5000))

    with app.app_context():
        db.create_all()

    app.run(host='0.0.0.0', port=port, debug=True)
