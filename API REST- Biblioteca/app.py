from flask import Flask, jsonify, request, Response, render_template
from helpers import NOMBRE_TABLA_LIBROS, NOMBRE_TABLA_AUTORES, NOMBRE_TABLA_EDITORES, NOMBRE_TABLA_ESCRITO_POR
from helpers import existeTabla, crearTablaLibro, crearTablaAutor, crearTablaEditor, crearTablaEscritoPor, selectTablaLibro, selectTablaAutor, selectTablaEditor, selectTablaEscritoPor, insertTablaLibro, insertTablaAutor, insertTablaEditor, insertTablaEscritoPor, eliminarTablaLibro, eliminarTablaAutor, eliminarTablaEditor, eliminarTablaEscritoPor, verificarNumero, verificarEntradas, actualizarTablaLibro, actualizarTablaEscritoPor, actualizarTablaEditor, actualizarTablaAutor

# Creación del objeto app y configuración del ordenamiento de claves en JSON
app = Flask(__name__)
app.json.sort_keys = False

# ======================================= RUTA PARA INTERFAZ =======================================

@app.route('/api')
def home():
    return render_template("index.html")

# ======================================= RUTAS PARA LIBROS =======================================

@app.route('/libros', methods = ['GET', 'POST'])
def librosSingular():
    try:
        if not existeTabla(NOMBRE_TABLA_LIBROS):
            if request.method == 'GET':
                return jsonify({"Error": "No existen registros de libros (Crear con POST)"}), 404
            elif request.method == 'POST':
                crearTablaLibro()
                return jsonify({"Mensaje": "Tabla de libros creada exitosamente"}), 201
        if request.method == 'GET':
            return jsonify(selectTablaLibro()), 200
        elif request.method == 'POST':
            solicitud = request.get_json()
            resultado = verificarEntradas(solicitud, False)
            if resultado is not None:
                return jsonify(resultado), 400
            idCreado = insertTablaLibro(solicitud["isbn"], solicitud["titulo"], solicitud["editor_id"], solicitud["formato"], solicitud["paginas"], solicitud["año"])
            return jsonify({"Mensaje": f"Libro creado con ID #{idCreado}"}), 201
    except Exception as e:
        return jsonify({"Error": f"Error interno del servidor: {str(e)}"}), 500
    

# metodo GET por ID
@app.route('/libros/<int:id>', methods = ['GET'])
def libroPorID(id):
    try:
        if not existeTabla(NOMBRE_TABLA_LIBROS):
            return jsonify({"Error": "No existen registros de libros"}), 404
        if request.method == 'GET':
            libros = selectTablaLibro()
            for libro in libros:
                if libro["id"] == id:
                    return jsonify(libro), 200
            return jsonify({"Error": f"No existe un libro con ID #{id}"}), 404
    except Exception as e:
        return jsonify({"Error": f"Error interno del servidor: {str(e)}"}), 500
        
# metodo PUT por ID
@app.route('/libros/<int:id>', methods = ['PUT'])
def actualizarLibro(id):
    try:
        if not existeTabla(NOMBRE_TABLA_LIBROS):
            return jsonify({"Error": "No existen registros de libros"}), 404
        if request.method == 'PUT':
            solicitud = request.get_json()
            resultado = verificarEntradas(solicitud, False)
            if resultado is not None:
                return jsonify(resultado), 400
            libroActualizado = actualizarTablaLibro(id, solicitud["isbn"], solicitud["titulo"], solicitud["editor_id"], solicitud["formato"], solicitud["paginas"], solicitud["año"])
            if libroActualizado:
                return jsonify({"Mensaje": f"Libro con ID #{id} actualizado exitosamente"}), 200
            else:
                return jsonify({"Error": f"No existe un libro con ID #{id}"}), 404
    except Exception as e:
        return jsonify({"Error": f"Error interno del servidor: {str(e)}"}), 500

# metodo DELETE por ID
@app.route('/libros/<int:id>', methods = ['DELETE'])
def eliminarLibro(id):
    try:
        if not existeTabla(NOMBRE_TABLA_LIBROS):
            return jsonify({"Error": "No existen registros de libros"}), 404
        if request.method == 'DELETE':
            libroEliminado = eliminarTablaLibro(id)
            if libroEliminado:
                return jsonify({"Mensaje": f"Libro con ID #{id} eliminado exitosamente"}), 200
            else:
                return jsonify({"Error": f"No existe un libro con ID #{id}"}), 404
    except Exception as e:
        return jsonify({"Error": f"Error interno del servidor: {str(e)}"}), 500

# ======================================= RUTAS PARA AUTORES =======================================

# metodo GET para obtener todos los autores
@app.route('/autores', methods = ['GET', 'POST'])
def autores():
    try:
        if not existeTabla(NOMBRE_TABLA_AUTORES):
            if request.method == 'GET':
                return jsonify({"Error": "No existen registros de autores"}), 404
            elif request.method == 'POST':
                crearTablaAutor()
                return jsonify({"Mensaje": "Tabla de autores creada exitosamente"}), 201
        if request.method == 'GET':
            return jsonify(selectTablaAutor()), 200
        elif request.method == 'POST':
            solicitud = request.get_json()
            resultado = verificarEntradas(solicitud, False)
            if resultado is not None:
                return jsonify(resultado), 400
            idCreado = insertTablaAutor(solicitud["nombre"], solicitud["pais"], solicitud["año"])
            return jsonify({"Mensaje": f"Autor creado con ID #{idCreado}"}), 201
    except Exception as e:
        return jsonify({"Error": f"Error interno del servidor: {str(e)}"}), 500

# metodo GET por ID
@app.route('/autores/<int:id>', methods = ['GET'])
def autorPorID(id):
    try:
        if not existeTabla(NOMBRE_TABLA_AUTORES):
            return jsonify({"Error": "No existen registros de autores"}), 404
        autores = selectTablaAutor()
        for autor in autores:
            if autor["id"] == id:
                return jsonify(autor), 200
        return jsonify({"Error": f"No existe un autor con ID #{id}"}), 404
    except Exception as e:
        return jsonify({"Error": f"Error interno del servidor: {str(e)}"}), 500

# metodo PUT por ID
@app.route('/autores/<int:id>', methods = ['PUT'])
def actualizarAutor(id):
    try:
        if not existeTabla(NOMBRE_TABLA_AUTORES):
            return jsonify({"Error": "No existen registros de autores"}), 404
        solicitud = request.get_json()
        resultado = verificarEntradas(solicitud, False)
        if resultado is not None:
            return jsonify(resultado), 400
        autorActualizado = actualizarTablaAutor(id, solicitud["nombre"], solicitud["pais"], solicitud["año"])
        if autorActualizado:
            return jsonify({"Mensaje": f"Autor con ID #{id} actualizado exitosamente"}), 200
        else:
            return jsonify({"Error": f"No existe un autor con ID #{id}"}), 404
    except Exception as e:
        return jsonify({"Error": f"Error interno del servidor: {str(e)}"}), 500

# metodo DELETE por ID
@app.route('/autores/<int:id>', methods = ['DELETE'])
def eliminarAutor(id):
    try:
        if not existeTabla(NOMBRE_TABLA_AUTORES):
            return jsonify({"Error": "No existen registros de autores"}), 404
        autorEliminado = eliminarTablaAutor(id)
        if autorEliminado:
            return jsonify({"Mensaje": f"Autor con ID #{id} eliminado exitosamente"}), 200
        else:
            return jsonify({"Error": f"No existe un autor con ID #{id}"}), 404
    except Exception as e:
        return jsonify({"Error": f"Error interno del servidor: {str(e)}"}), 500

# ======================================= RUTAS PARA EDITORES =======================================

# metodo GET para obtener todos los editores
@app.route('/editores', methods = ['GET', 'POST'])
def editores():
    try:
        if not existeTabla(NOMBRE_TABLA_EDITORES):
            if request.method == 'GET':
                return jsonify({"Error": "No existen registros de editores"}), 404
            elif request.method == 'POST':
                crearTablaEditor()
                return jsonify({"Mensaje": "Tabla de editores creada exitosamente"}), 201
        if request.method == 'GET':
            return jsonify(selectTablaEditor()), 200
        elif request.method == 'POST':
            solicitud = request.get_json()
            resultado = verificarEntradas(solicitud, False)
            if resultado is not None:
                return jsonify(resultado), 400
            idCreado = insertTablaEditor(solicitud["nombre"])
            return jsonify({"Mensaje": f"Editor creado con ID #{idCreado}"}), 201
    except Exception as e:
        return jsonify({"Error": f"Error interno del servidor: {str(e)}"}), 500


# metodo GET por ID
@app.route('/editores/<int:id>', methods = ['GET'])
def editorPorID(id):
    try:
        if not existeTabla(NOMBRE_TABLA_EDITORES):
            return jsonify({"Error": "No existen registros de editores"}), 404
        editores = selectTablaEditor()
        for editor in editores:
            if editor["id"] == id:
                return jsonify(editor), 200
        return jsonify({"Error": f"No existe un editor con ID #{id}"}), 404
    except Exception as e:
        return jsonify({"Error": f"Error interno del servidor: {str(e)}"}), 500

# metodo PUT por ID
@app.route('/editores/<int:id>', methods = ['PUT'])
def actualizarEditor(id):
    try:
        if not existeTabla(NOMBRE_TABLA_EDITORES):
            return jsonify({"Error": "No existen registros de editores"}), 404
        solicitud = request.get_json()
        resultado = verificarEntradas(solicitud, False)
        if resultado is not None:
            return jsonify(resultado), 400
        editorActualizado = actualizarTablaEditor(id, solicitud["nombre"])
        if editorActualizado:
            return jsonify({"Mensaje": f"Editor con ID #{id} actualizado exitosamente"}), 200
        else:
            return jsonify({"Error": f"No existe un editor con ID #{id}"}), 404
    except Exception as e:
        return jsonify({"Error": f"Error interno del servidor: {str(e)}"}), 500

# metodo DELETE por ID
@app.route('/editores/<int:id>', methods = ['DELETE'])
def eliminarEditor(id):
    try:
        if not existeTabla(NOMBRE_TABLA_EDITORES):
            return jsonify({"Error": "No existen registros de editores"}), 404
        editorEliminado = eliminarTablaEditor(id)
        if editorEliminado:
            return jsonify({"Mensaje": f"Editor con ID #{id} eliminado exitosamente"}), 200
        else:
            return jsonify({"Error": f"No existe un editor con ID #{id}"}), 404
    except Exception as e:
        return jsonify({"Error": f"Error interno del servidor: {str(e)}"}), 500

# ======================================= RUTAS PARA ESCRITO_POR =======================================

@app.route('/escritos', methods = ['GET', 'POST'])
def escritos():
    try:
        if not existeTabla(NOMBRE_TABLA_ESCRITO_POR):
            if request.method == 'GET':
                return jsonify({"Error": "No existen registros de escritos"}), 404
            elif request.method == 'POST':
                crearTablaEscritoPor()
                return jsonify({"Mensaje": "Tabla de escritos creada exitosamente"}), 201
        if request.method == 'GET':
            return jsonify(selectTablaEscritoPor()), 200
        elif request.method == 'POST':
            solicitud = request.get_json()
            resultado = verificarEntradas(solicitud, False)
            if resultado is not None:
                return jsonify(resultado), 400
            insertTablaEscritoPor(solicitud["libro_id"], solicitud["autor_id"])
            return jsonify({"Mensaje": f"Relación creada entre libro #{solicitud['libro_id']} y autor #{solicitud['autor_id']}"}), 201
    except Exception as e:
        return jsonify({"Error": f"Error interno del servidor: {str(e)}"}), 500

# metodo PUT por IDs
@app.route('/escritos/<int:libro_id>/<int:autor_id>', methods = ['PUT'])
def actualizarEscrito(libro_id, autor_id):
    try:
        if not existeTabla(NOMBRE_TABLA_ESCRITO_POR):
            return jsonify({"Error": "No existen registros de escritos"}), 404
        solicitud = request.get_json()
        resultado = verificarEntradas(solicitud, False)
        if resultado is not None:
            return jsonify(resultado), 400
        escritoActualizado = actualizarTablaEscritoPor(libro_id, autor_id, solicitud["libro_id"], solicitud["autor_id"])
        if escritoActualizado:
            return jsonify({"Mensaje": f"Relación actualizada exitosamente"}), 200
        else:
            return jsonify({"Error": f"No existe la relación entre libro #{libro_id} y autor #{autor_id}"}), 404
    except Exception as e:
        return jsonify({"Error": f"Error interno del servidor: {str(e)}"}), 500

# metodo DELETE por IDs
@app.route('/escritos/<int:libro_id>/<int:autor_id>', methods = ['DELETE'])
def eliminarEscrito(libro_id, autor_id):
    try:
        if not existeTabla(NOMBRE_TABLA_ESCRITO_POR):
            return jsonify({"Error": "No existen registros de escritos"}), 404
        escritoEliminado = eliminarTablaEscritoPor(libro_id, autor_id)
        if escritoEliminado:
            return jsonify({"Mensaje": f"Relación eliminada exitosamente"}), 200
        else:
            return jsonify({"Error": f"No existe la relación entre libro #{libro_id} y autor #{autor_id}"}), 404
    except Exception as e:
        return jsonify({"Error": f"Error interno del servidor: {str(e)}"}), 500

# Método main
def main():
    app.run(debug = True)

@app.route("/")
def index():
    return render_template("index.html")

if __name__ == "__main__":
    main()