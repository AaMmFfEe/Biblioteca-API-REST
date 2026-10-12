import json
import os
import sqlite3

# constantes para manejar la base de datos
BASE_DE_DATOS = 'libreria.db'

NOMBRE_TABLA_LIBROS = 'libro' 
NOMBRE_TABLA_AUTORES = 'autor'
NOMBRE_TABLA_EDITORES = 'editor'
NOMBRE_TABLA_ESCRITO_POR = 'escrito_por'

# llaves de las tablas
LLAVES_LIBRO = {
    'id': 'ID',
    'isbn': 'ISBN',
    'titulo': 'Titulo',
    'editor_id': 'Editor',
    'formato': 'Formato',
    'paginas': 'Paginas',
    'año': 'Fecha'
}

LLAVES_AUTOR = {
    'id': 'ID',
    'nombre': 'Nombre',
    'pais': 'Pais',
    'año': 'Año'
}

LLAVES_EDITOR = {
    'id': 'ID',
    'nombre': 'Nombre'
}

LLAVES_ESCRITO_POR = {
    'libro_id': 'ID_Libro',
    'autor_id': 'ID_Autor'
}

# conexion a la base de datos
def conexionDB():
    """
    Crea un objeto de conexión a la base de datos SQLite3
    
    :return: Conexión a la base de datos
    """
    
    return sqlite3.connect(BASE_DE_DATOS)

# verificar que existe la tabla
def existeTabla(nombreTabla):
    """
    Verifica si existe la tabla `producto` en la base de datos `inventario.db`
    :param nombreTabla: Nombre de la tabla cuya existencia se buscará

    :return: `True` si la tabla existe, `False` si no existe.
    """

    # Se crea una conexión a la base de datos
    # y se almacena su cursor en una variable.
    conn = conexionDB()
    cursor = conn.cursor()
    # Se ejecuta la consulta de selección para verificar la existencia
    # de la tabla producto base de datos
    tabla = cursor.execute(
        """
        SELECT name FROM sqlite_master WHERE type='table'
        AND name = ?;
        """, (nombreTabla,)).fetchone()
    # Se cierra la conexión y se devuelve True si la tabla existe.
    # De lo contrario, False.
    conn.close()
    return True if tabla is not None else False

# crear las tablas necesarias para la base de datos en caso de que no existan
def crearTablaLibro():
    """
    Crea la tabla 'libro' en la base de datos 'libreria.db'
    """
    
    conn = conexionDB()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS libro (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            isbn TEXT,
            titulo TEXT,
            editor_id INTEGER,
            formato TEXT,
            paginas INTEGER,
            año INTEGER,
            FOREIGN KEY (editor_id) REFERENCES editor(id) ON DELETE SET NULL
        );
        """
    )
    # Se confirman los cambios y se cierra la conexión.
    conn.commit()
    conn.close()
    
def crearTablaAutor():
    """
    Crea la tabla 'autor' en la base de datos 'libreria.db'
    """
    
    conn = conexionDB()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS autor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT,
            pais TEXT,
            año INTEGER
        );
        """
    )
    # Se confirman los cambios y se cierra la conexión.
    conn.commit()
    conn.close()

def crearTablaEditor():
    """
    Crea la tabla 'editor' en la base de datos 'libreria.db'
    """
    
    conn = conexionDB()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS editor (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT
        );
        """
    )
    # Se confirman los cambios y se cierra la conexión.
    conn.commit()
    conn.close()

def crearTablaEscritoPor():
    """
    Crea la tabla 'escrito_por' en la base de datos 'libreria.db'
    """
    
    conn = conexionDB()
    cursor = conn.cursor()
    
    cursor.execute(
        """
        CREATE TABLE IF NOT EXISTS escrito_por (
            libro_id INTEGER,
            autor_id INTEGER,
            PRIMARY KEY (libro_id, autor_id),
            FOREIGN KEY (autor_id) REFERENCES autor(id) ON DELETE SET NULL,
            FOREIGN KEY (libro_id) REFERENCES libro(id) ON DELETE SET NULL
        );
        """
    )
    # Se confirman los cambios y se cierra la conexión.
    conn.commit()
    conn.close()

# seleccionar las tablas para manipularlas
def selectTablaLibro():
    """
    Maneja la instrucción de selección de la tabla `libro` de la base de datos.

    :return: Lista de diccionarios donde cada diccionario corresponde a una fila de la tabla `libro`
    """
    # Se crea una conexión a la base de datos
    # y se almacena su cursor en una variable.
    conn = conexionDB()
    cursor = conn.cursor()
    # Se ejecuta la consulta de selección.
    cursor.execute(
        """
        SELECT
            id, 
            isbn,
            titulo,
            editor_id,
            formato,
            paginas,
            año
        FROM libro;
        """
    )
    # Se extraen las filas del cursor y se agregan
    # a una lista en forma de diccionarios.
    datos = cursor.fetchall()
    libros = []
    for fila in datos:
        libros.append({
            "id": fila[0],
            "isbn": fila[1],
            "titulo": fila[2],
            "editor_id": fila[3],
            "formato": fila[4],
            "paginas": fila[5],
            "año": fila[6]
        })
    # Se cierra la conexión y se devuelven la lista de filas.
    conn.close()
    return libros

def selectTablaAutor():
    """
    Maneja la instrucción de selección de la tabla `autor` de la base de datos.

    :return: Lista de diccionarios donde cada diccionario corresponde a una fila de la tabla `autor`
    """
    # Se crea una conexión a la base de datos
    # y se almacena su cursor en una variable.
    conn = conexionDB()
    cursor = conn.cursor()
    # Se ejecuta la consulta de selección.
    cursor.execute(
        """
        SELECT
            id, 
            nombre,
            pais,
            año
        FROM autor;
        """
    )
    # Se extraen las filas del cursor y se agregan
    # a una lista en forma de diccionarios.
    datos = cursor.fetchall()
    autores = []
    for fila in datos:
        autores.append({
            "id": fila[0],
            "nombre": fila[1],
            "pais": fila[2],
            "año": fila[3]
        })
    # Se cierra la conexión y se devuelven la lista de filas.
    conn.close()
    return autores

def selectTablaEditor():
    """
    Maneja la instrucción de selección de la tabla `editor` de la base de datos.

    :return: Lista de diccionarios donde cada diccionario corresponde a una fila de la tabla `editor`
    """
    # Se crea una conexión a la base de datos
    # y se almacena su cursor en una variable.
    conn = conexionDB()
    cursor = conn.cursor()
    # Se ejecuta la consulta de selección.
    cursor.execute(
        """
        SELECT
            id, 
            nombre
        FROM editor;
        """
    )
    # Se extraen las filas del cursor y se agregan
    # a una lista en forma de diccionarios.
    datos = cursor.fetchall()
    editores = []
    for fila in datos:
        editores.append({
            "id": fila[0],
            "nombre": fila[1]
        })
    # Se cierra la conexión y se devuelven la lista de filas.
    conn.close()
    return editores

def selectTablaEscritoPor():
    """
    Maneja la instrucción de selección de la tabla `escrito_por` de la base de datos.

    :return: Lista de diccionarios donde cada diccionario corresponde a una fila de la tabla `escrito_por`
    """
    # Se crea una conexión a la base de datos
    # y se almacena su cursor en una variable.
    conn = conexionDB()
    cursor = conn.cursor()
    # Se ejecuta la consulta de selección.
    cursor.execute(
        """
        SELECT
            libro_id,
            autor_id
        FROM escrito_por;
        """
    )
    # Se extraen las filas del cursor y se agregan
    # a una lista en forma de diccionarios.
    datos = cursor.fetchall()
    escritos = []
    for fila in datos:
        escritos.append({
            "libro_id": fila[0],
            "autor_id": fila[1]
        })
    # Se cierra la conexión y se devuelven la lista de filas.
    conn.close()
    return escritos

# insertar filas en las tablas
def insertTablaLibro(isbn, titulo, editor_id, formato, paginas, año):
    """
    Maneja la instrucción de inserción a la tabla `libro` de la base de datos.

    :param isbn: marcador del libro a registrar
    :param titulo: titulo del libro
    :param editor_id: llave fóranea que referencia a la tabla 'editor'
    :param formato: formato del libro
    :param paginas: valor númerico que indica la cantidad de páginas que tiene el libro
    :param año: valor número que indica el año de la fecha de la publicación del libro
    :return: ID correspondiente al producto recien creado.
    """
    # Se crea una conexión a la base de datos.
    conn = conexionDB()
    # Se ejecuta una consulta de inserción tomando los valores de los parámetros.
    cursor = conn.execute(
        """
        INSERT INTO libro(isbn, titulo, editor_id, formato, paginas, año)
        VALUES (?,?,?,?,?,?)
        """
        ,(isbn, titulo, editor_id, formato, paginas, año)
    )
    # Se obtiene el ID de la fila recién creada.
    idCreado = cursor.lastrowid
    # Se confirman los cambios y se cierra la conexión.
    conn.commit()
    conn.close()
    # Se regresa el ID de la fila creada.
    return idCreado

def insertTablaAutor(nombre, pais, año):
    """
    Maneja la instrucción de inserción a la tabla `autor` de la base de datos.

    :param nombre: nombre del autor
    :param pais: nombre del país del que proviene el autor
    :param año: valor númerico que indica el año en el que nació el autor
    :return: ID correspondiente al producto recien creado.
    """
    # Se crea una conexión a la base de datos.
    conn = conexionDB()
    # Se ejecuta una consulta de inserción tomando los valores de los parámetros.
    cursor = conn.execute(
        """
        INSERT INTO autor(nombre, pais, año)
        VALUES (?,?,?)
        """
        ,(nombre, pais, año)
    )
    # Se obtiene el ID de la fila recién creada.
    idCreado = cursor.lastrowid
    # Se confirman los cambios y se cierra la conexión.
    conn.commit()
    conn.close()
    # Se regresa el ID de la fila creada.
    return idCreado

def insertTablaEditor(nombre):
    """
    Maneja la instrucción de inserción a la tabla `editor` de la base de datos.

    :param nombre: nombre del editor
    :return: ID correspondiente al editor recien creado.
    """
    # Se crea una conexión a la base de datos.
    conn = conexionDB()
    # Se ejecuta una consulta de inserción tomando los valores de los parámetros.
    cursor = conn.execute(
        """
        INSERT INTO editor(nombre)
        VALUES (?)
        """
        ,(nombre,)
    )
    # Se obtiene el ID de la fila recién creada.
    idCreado = cursor.lastrowid
    # Se confirman los cambios y se cierra la conexión.
    conn.commit()
    conn.close()
    # Se regresa el ID de la fila creada.
    return idCreado


def insertTablaEscritoPor(libro_id, autor_id):
    """
    Maneja la instrucción de inserción a la tabla `escrito_por` de la base de datos.

    :param libro_id: ID del libro asociado.
    :param autor_id: ID del autor asociado.
    :return: `True` si el registro fue creado exitosamente.
    """
    conn = conexionDB()
    cursor = conn.execute(
        """
        INSERT INTO escrito_por(libro_id, autor_id)
        VALUES (?, ?)
        """
        ,(libro_id, autor_id)
    )
    conn.commit()
    conn.close()
    return True


def actualizarTablaLibro(id, isbn, titulo, editor_id, formato, paginas, año):
    """
    Actualiza una fila de la tabla `libro`.

    :param id: ID del libro a actualizar.
    :param isbn: ISBN del libro.
    :param titulo: Título del libro.
    :param editor_id: ID del editor asociado.
    :param formato: Formato del libro.
    :param paginas: Cantidad de páginas.
    :param año: Año de publicación.
    :return: `True` si el libro fue actualizado, `False` si no existía.
    """
    conn = conexionDB()
    cursor = conn.execute(
        """
        UPDATE libro
        SET isbn = ?, titulo = ?, editor_id = ?, formato = ?, paginas = ?, año = ?
        WHERE id = ?;
        """
        ,(isbn, titulo, editor_id, formato, paginas, año, id)
    )
    libroActualizado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return libroActualizado


def actualizarTablaAutor(id, nombre, pais, año):
    """
    Actualiza una fila de la tabla `autor`.

    :param id: ID del autor a actualizar.
    :param nombre: Nombre del autor.
    :param pais: País del autor.
    :param año: Año de nacimiento.
    :return: `True` si el autor fue actualizado, `False` si no existía.
    """
    conn = conexionDB()
    cursor = conn.execute(
        """
        UPDATE autor
        SET nombre = ?, pais = ?, año = ?
        WHERE id = ?;
        """
        ,(nombre, pais, año, id)
    )
    autorActualizado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return autorActualizado


def actualizarTablaEditor(id, nombre):
    """
    Actualiza una fila de la tabla `editor`.

    :param id: ID del editor a actualizar.
    :param nombre: Nombre del editor.
    :return: `True` si el editor fue actualizado, `False` si no existía.
    """
    conn = conexionDB()
    cursor = conn.execute(
        """
        UPDATE editor
        SET nombre = ?
        WHERE id = ?;
        """
        ,(nombre, id)
    )
    editorActualizado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return editorActualizado


def actualizarTablaEscritoPor(libro_id, autor_id, nuevo_libro_id, nuevo_autor_id):
    """
    Actualiza una fila de la tabla `escrito_por`.

    :param libro_id: ID del libro de la fila existente.
    :param autor_id: ID del autor de la fila existente.
    :param nuevo_libro_id: Nuevo ID del libro.
    :param nuevo_autor_id: Nuevo ID del autor.
    :return: `True` si el registro fue actualizado, `False` si no existía.
    """
    conn = conexionDB()
    cursor = conn.execute(
        """
        UPDATE escrito_por
        SET libro_id = ?, autor_id = ?
        WHERE libro_id = ? AND autor_id = ?;
        """
        ,(nuevo_libro_id, nuevo_autor_id, libro_id, autor_id)
    )
    escritoActualizado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return escritoActualizado

# eliminar datos de las tablas
def eliminarTablaLibro(id):
    """
    Maneja la instrucción de eliminación en la tabla `libro` de la base de datos.
    
    :param id: ID del libro a eliminar.
    :return: `True` si el producto fue eliminado exitosamente, `False` si el libro no existe.
    """
    # Se crea una conexión a la base de datos.
    conn = conexionDB()
    
    # Se ejecuta una consulta de eliminación utilizando el ID como parámetro.
    cursor = conn.execute(
        """
        DELETE FROM libro
        WHERE id = ?;
        """
        ,(id,)
    )
    # Se verifica si la fila fue eliminada exitosamente
    # (rowcount > 0 indica que se eliminó al menos una fila).
    libroEliminado = cursor.rowcount > 0
    
    # Se confirman los cambios y se cierra la conexión.
    conn.commit()
    conn.close()
    
    # Se regresa True si el libro fue eliminado, False de lo contrario.
    return libroEliminado

def eliminarTablaAutor(id):
    """
    Maneja la instrucción de eliminación en la tabla `autor` de la base de datos.
    
    :param id: ID del autor a eliminar.
    :return: `True` si el producto fue eliminado exitosamente, `False` si el autor no existe.
    """
    # Se crea una conexión a la base de datos.
    conn = conexionDB()
    
    # Se ejecuta una consulta de eliminación utilizando el ID como parámetro.
    cursor = conn.execute(
        """
        DELETE FROM autor
        WHERE id = ?;
        """
        ,(id,)
    )
    # Se verifica si la fila fue eliminada exitosamente
    # (rowcount > 0 indica que se eliminó al menos una fila).
    autorEliminado = cursor.rowcount > 0
    
    # Se confirman los cambios y se cierra la conexión.
    conn.commit()
    conn.close()
    
    # Se regresa True si el autor fue eliminado, False de lo contrario.
    return autorEliminado

def eliminarTablaEditor(id):
    """
    Maneja la instrucción de eliminación en la tabla `editor` de la base de datos.
    
    :param id: ID del editor a eliminar.
    :return: `True` si el producto fue eliminado exitosamente, `False` si el editor no existe.
    """
    # Se crea una conexión a la base de datos.
    conn = conexionDB()
    
    # Se ejecuta una consulta de eliminación utilizando el ID como parámetro.
    cursor = conn.execute(
        """
        DELETE FROM editor
        WHERE id = ?;
        """
        ,(id,)
    )
    # Se verifica si la fila fue eliminada exitosamente
    # (rowcount > 0 indica que se eliminó al menos una fila).
    editorEliminado = cursor.rowcount > 0
    
    # Se confirman los cambios y se cierra la conexión.
    conn.commit()
    conn.close()
    
    # Se regresa True si el editor fue eliminado, False de lo contrario.
    return editorEliminado


def eliminarTablaEscritoPor(libro_id, autor_id):
    """
    Maneja la instrucción de eliminación en la tabla `escrito_por` de la base de datos.
    
    :param libro_id: ID del libro asociado.
    :param autor_id: ID del autor asociado.
    :return: `True` si el registro fue eliminado exitosamente, `False` si no existía.
    """
    conn = conexionDB()
    cursor = conn.execute(
        """
        DELETE FROM escrito_por
        WHERE libro_id = ? AND autor_id = ?;
        """
        ,(libro_id, autor_id)
    )
    escritoEliminado = cursor.rowcount > 0
    conn.commit()
    conn.close()
    return escritoEliminado

# verificación básica de datos
def verificarLibro(diccionarioLibro, incluirID):
    """
    Verifica que un diccionario otorgado cuente con las claves esperadas
    de un libro de acuerdo a la especificación en este programa.

    :param diccionarioLibro: Diccionario de libro por analizar.
    :para incluirID: Valor booleano que indica si se eliminará la clave `id` del set de referencia.
    :return: El resultado de `verificarEntradas()` si el diccionario cumple con la estructura esperada por el programa, de lo contrario, un diccionario con un mensaje de error.
    """
    # Se crea un set de las claves del diccionario LLAVES_PRODUCTO
    # y otro set del diccionario correspondiente al libro por verificar.
    referencia = set(LLAVES_LIBRO)
    setDiccionario = set(diccionarioLibro)
    # Se elimina la ID para la verificación de solicitudes POST y PUT del usuario
    if not incluirID:
        referencia.remove("id")
    # Si las claves de ambos diccionarios coinciden, se pasa a la validación de entradas
    # numéricas
    if setDiccionario == referencia:
        return verificarEntradasLibro(diccionarioLibro)
    # Si las claves de ambos diccionarios no coinciden, se busca la clave que no se encuentra
    # en el diccionario otorgado por el usuario.
    else:
        if incluirID and "id" not in setDiccionario:
            return {"Error": "ID no incluída en la solicitud JSON"}
        # Se utiliza el display_name del diccionario LLAVES_PRODUCTO para expresar
        # el mensaje de forma más clara.
        for clave, display_name in LLAVES_LIBRO.items():
            if clave not in setDiccionario and clave != "id":
                return {"Error": f"{display_name} no incluído en la solicitud JSON"}
        # Si, en un caso inusual, no se encuentra una clave con la que asociar la falla, se 
        # imprime un mensaje de error genérico.
        return {"Error": "La estructura de la solicitud no coincide con la solicitud esperada"}

def verificarAutor(diccionarioAutor, incluirID):
    """
    Verifica que un diccionario otorgado cuente con las claves esperadas
    de un autor de acuerdo a la especificación en este programa.

    :param diccionarioAutor: Diccionario de autor por analizar.
    :para incluirID: Valor booleano que indica si se eliminará la clave `id` del set de referencia.
    :return: El resultado de `verificarEntradasAutor()` si el diccionario cumple con la estructura esperada por el programa, de lo contrario, un diccionario con un mensaje de error.
    """
    referencia = set(LLAVES_AUTOR)
    setDiccionario = set(diccionarioAutor)
    if not incluirID:
        referencia.remove("id")
    if setDiccionario == referencia:
        return verificarEntradasAutor(diccionarioAutor)
    else:
        if incluirID and "id" not in setDiccionario:
            return {"Error": "ID no incluída en la solicitud JSON"}
        for clave, display_name in LLAVES_AUTOR.items():
            if clave not in setDiccionario and clave != "id":
                return {"Error": f"{display_name} no incluído en la solicitud JSON"}
        return {"Error": "La estructura de la solicitud no coincide con la solicitud esperada"}

def verificarEntradasLibro(diccionarioLibro):
    """
    Verifica que las entradas numéricas de un diccionario correspondiente a un libro sean válidas

    :param diccionarioProducto: Diccionario de producto por analizar.
    :return: `None` si el diccionario cumple con la estructura esperada por el programa, de lo contrario, un diccionario con un mensaje de error.
    """
    # Se evalúan las diferentes condiciones que podrían causar problemas con la inserción a la base de datos:
    # precioMenudeo
    if not verificarNumero(diccionarioLibro["paginas"], min = 0, isFloat = True):
        return {"Error": "La cantidad de páginas debe ser mayor a 0."}
    elif not verificarNumero(diccionarioLibro["año"], min = 0, isFloat = True):
        return {"Error": "El año debe ser mayor a 0."}
    else:
        return None

def verificarEntradasAutor(diccionarioAutor):
    """
    Verifica que las entradas numéricas de un diccionario correspondiente a un autor sean válidas

    :param diccionarioAutor: Diccionario de autor por analizar.
    :return: `None` si el diccionario cumple con la estructura esperada por el programa, de lo contrario, un diccionario con un mensaje de error.
    """
    if not verificarNumero(diccionarioAutor["año"], min = 0, isFloat = True):
        return {"Error": "El año debe ser mayor a 0."}
    else:
        return None


def verificarEditor(diccionarioEditor, incluirID):
    """
    Verifica que un diccionario otorgado cuente con las claves esperadas
    de un editor de acuerdo a la especificación en este programa.
    """
    referencia = set(LLAVES_EDITOR)
    setDiccionario = set(diccionarioEditor)
    if not incluirID:
        referencia.remove("id")
    if setDiccionario == referencia:
        return None
    else:
        if incluirID and "id" not in setDiccionario:
            return {"Error": "ID no incluída en la solicitud JSON"}
        for clave, display_name in LLAVES_EDITOR.items():
            if clave not in setDiccionario and clave != "id":
                return {"Error": f"{display_name} no incluído en la solicitud JSON"}
        return {"Error": "La estructura de la solicitud no coincide con la solicitud esperada"}


def verificarEscritoPor(diccionarioEscrito, incluirID=False):
    """
    Verifica que un diccionario otorgado cuente con las claves esperadas
    de un registro de la relación escrito_por.
    """
    referencia = set(LLAVES_ESCRITO_POR)
    setDiccionario = set(diccionarioEscrito)
    if setDiccionario == referencia:
        return verificarEntradasEscritoPor(diccionarioEscrito)
    else:
        for clave, display_name in LLAVES_ESCRITO_POR.items():
            if clave not in setDiccionario:
                return {"Error": f"{display_name} no incluído en la solicitud JSON"}
        return {"Error": "La estructura de la solicitud no coincide con la solicitud esperada"}


def verificarEntradasEscritoPor(diccionarioEscrito):
    """
    Verifica que las entradas numéricas de un diccionario correspondiente a escrito_por sean válidas
    """
    if not verificarNumero(diccionarioEscrito["libro_id"], min=1, isFloat=False):
        return {"Error": "El libro_id debe ser un entero mayor o igual a 1."}
    elif not verificarNumero(diccionarioEscrito["autor_id"], min=1, isFloat=False):
        return {"Error": "El autor_id debe ser un entero mayor o igual a 1."}
    else:
        return None


def verificarEntradas(diccionario, incluirID):
    """
    Verifica un diccionario de entrada para libro, autor, editor o escrito_por.
    """
    referencia_libro = set(LLAVES_LIBRO)
    referencia_autor = set(LLAVES_AUTOR)
    referencia_editor = set(LLAVES_EDITOR)
    referencia_escrito = set(LLAVES_ESCRITO_POR)
    if not incluirID:
        referencia_libro.remove("id")
        referencia_autor.remove("id")
        referencia_editor.remove("id")
    setDiccionario = set(diccionario)
    if setDiccionario == referencia_libro:
        return verificarLibro(diccionario, incluirID)
    elif setDiccionario == referencia_autor:
        return verificarAutor(diccionario, incluirID)
    elif setDiccionario == referencia_editor:
        return verificarEditor(diccionario, incluirID)
    elif setDiccionario == referencia_escrito:
        return verificarEscritoPor(diccionario)
    else:
        return {"Error": "La estructura de la solicitud no coincide con la estructura esperada."}


def verificarNumero(numero, min=None, isFloat=True):
    """
    Verifica que una entrada numérica cumpla con las características deseadas.

    :param numero: Valor numérico por analizar.
    :para min: Valor numérico opcional que indica el mínimo inclusivo con el que deberá cumplir la función.
    :param isFloat: Valor booleano que indica si el número que se espera es de punto flotante o no.
    :return: `True` si el número es válido, `False` de lo contrario.
    """
    # Se almacena el tipo de entradas que se aceptarán de acuerdo a si el número será entero o flotante.
    tipoNumero = (float, int) if isFloat else int
    # Si el número otorgado no pertenece a los tipos de entradas aceptado, se devuelve False.
    if not isinstance(numero, tipoNumero):
        return False
    # Si el número es mayor o igual al mínimo, se regresa True. De lo contrario, False.
    return numero >= min