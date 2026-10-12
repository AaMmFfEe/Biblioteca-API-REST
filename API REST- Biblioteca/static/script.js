
// mostrar libros
function getLibros() {
    fetch('/libros')
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.Error || 'Error al obtener libros'); });
            }
            return response.json();
        })
        .then(libros => {
            const lista = document.getElementById('librosLista');
            lista.innerHTML = '';
            if (libros.length === 0) {
                lista.innerHTML = '<li>No hay libros registrados.</li>';
                return;
            }
            libros.forEach(libro => {
                const li = document.createElement('li');
                li.textContent = `ID: ${libro.id} | ISBN: ${libro.isbn} | Título: ${libro.titulo} | Editor ID: ${libro.editor_id} | Formato: ${libro.formato} | Páginas: ${libro.paginas} | Año: ${libro.año}`;
                lista.appendChild(li);
            });
        })
        .catch(error => alert('Error: ' + error.message));
}

// Agregar libro
function agregarLibros() {
    const isbn = document.getElementById('isbn').value.trim();
    const titulo = document.getElementById('titulo').value.trim();
    const editor_id = parseInt(document.getElementById('editor_id').value);
    const formato = document.getElementById('formato').value.trim();
    const paginas = parseInt(document.getElementById('paginas').value);
    const año = parseInt(document.getElementById('año').value);

    if (!isbn || !titulo || !formato || isNaN(editor_id) || isNaN(paginas) || isNaN(año)) {
        alert('Todos los campos son obligatorios y los números deben ser válidos.');
        return;
    }

    const data = { isbn, titulo, editor_id, formato, paginas, año };

    fetch('/libros', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json().then(json => ({ ok: response.ok, json })))
    .then(({ ok, json }) => {
        if (!ok) throw new Error(json.Error || 'Error al agregar libro');
        alert(json.Mensaje);
        // Limpiar formulario
        document.getElementById('isbn').value = '';
        document.getElementById('titulo').value = '';
        document.getElementById('editor_id').value = '';
        document.getElementById('formato').value = '';
        document.getElementById('paginas').value = '';
        document.getElementById('año').value = '';
        getLibros(); // refrescar lista
    })
    .catch(error => alert('Error: ' + error.message));
}

// Actualizar libro
function updateLibro(id, data) {
    if (!id || isNaN(id)) {
        alert('Debe proporcionar un ID válido.');
        return;
    }
    // Validar que los campos estén llenos
    for (let key in data) {
        if (data[key] === '' || data[key] === undefined || data[key] === null) {
            alert('Todos los campos deben estar completos.');
            return;
        }
    }

    fetch(`/libros/${id}`, {
        method: 'PUT',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json().then(json => ({ ok: response.ok, json })))
    .then(({ ok, json }) => {
        if (!ok) throw new Error(json.Error || 'Error al actualizar libro');
        alert(json.Mensaje);
        getLibros();
    })
    .catch(error => alert('Error: ' + error.message));
}

// Eliminar libro
function deleteLibro(id) {
    if (!id || isNaN(id)) {
        alert('Debe proporcionar un ID válido.');
        return;
    }
    if (!confirm(`¿Está seguro de eliminar el libro con ID ${id}?`)) return;

    fetch(`/libros/${id}`, {
        method: 'DELETE'
    })
    .then(response => response.json().then(json => ({ ok: response.ok, json })))
    .then(({ ok, json }) => {
        if (!ok) throw new Error(json.Error || 'Error al eliminar libro');
        alert(json.Mensaje);
        getLibros();
    })
    .catch(error => alert('Error: ' + error.message));
}

// mostrar autores
function getAutores() {
    fetch('/autores')
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.Error || 'Error al obtener autores'); });
            }
            return response.json();
        })
        .then(autores => {
            const lista = document.getElementById('autoresLista');
            lista.innerHTML = '';
            if (autores.length === 0) {
                lista.innerHTML = '<li>No hay autores registrados.</li>';
                return;
            }
            autores.forEach(autor => {
                const li = document.createElement('li');
                li.textContent = `ID: ${autor.id} | Nombre: ${autor.nombre} | País: ${autor.pais} | Año: ${autor.año}`;
                lista.appendChild(li);
            });
        })
        .catch(error => alert('Error: ' + error.message));
}

// Agregar autor
function addAutor(data) {
    if (!data.nombre || !data.pais || isNaN(data.año)) {
        alert('Todos los campos son obligatorios y el año debe ser un número.');
        return;
    }

    fetch('/autores', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json().then(json => ({ ok: response.ok, json })))
    .then(({ ok, json }) => {
        if (!ok) throw new Error(json.Error || 'Error al agregar autor');
        alert(json.Mensaje);
        // Limpiar formulario
        document.getElementById('autorNombre').value = '';
        document.getElementById('autorPais').value = '';
        document.getElementById('autorAño').value = '';
        getAutores();
    })
    .catch(error => alert('Error: ' + error.message));
}

// mostrar editores
function getEditores() {
    fetch('/editores')
        .then(response => {
            if (!response.ok) {
                return response.json().then(err => { throw new Error(err.Error || 'Error al obtener editores'); });
            }
            return response.json();
        })
        .then(editores => {
            const lista = document.getElementById('editoresLista');
            lista.innerHTML = '';
            if (editores.length === 0) {
                lista.innerHTML = '<li>No hay editores registrados.</li>';
                return;
            }
            editores.forEach(editor => {
                const li = document.createElement('li');
                li.textContent = `ID: ${editor.id} | Nombre: ${editor.nombre}`;
                lista.appendChild(li);
            });
        })
        .catch(error => alert('Error: ' + error.message));
}

// agregar editor
function addEditor(data) {
    if (!data.nombre) {
        alert('El nombre del editor es obligatorio.');
        return;
    }

    fetch('/editores', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify(data)
    })
    .then(response => response.json().then(json => ({ ok: response.ok, json })))
    .then(({ ok, json }) => {
        if (!ok) throw new Error(json.Error || 'Error al agregar editor');
        alert(json.Mensaje);
        document.getElementById('editorNombre').value = '';
        getEditores();
    })
    .catch(error => alert('Error: ' + error.message));
}