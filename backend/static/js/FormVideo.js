document.getElementById('videoForm').addEventListener('submit', function(event) {
    // Obtener los elementos del formulario
    const videoFile = document.getElementById('videoFile').files[0];
    const thumbnailFile = document.getElementById('thumbnail').files[0];
    const title = document.getElementById('videoTitle').value;
    const description = document.getElementById('videoDescription').value;

    // Validar archivo de video (formato .mp4, máx. 10 MB)
    if (!videoFile || videoFile.type !== 'video/mp4' || videoFile.size > 10 * 1024 * 1024) {
        alert('El archivo de video debe ser .mp4 y no superar los 10 MB.');
        event.preventDefault();
        return;
    }

    // Validar el título (obligatorio)
    if (title.trim() === '') {
        alert('El título es obligatorio.');
        event.preventDefault();
        return;
    }

    // Validar descripción (máx. 300 caracteres)
    if (description.length > 300) {
        alert('La descripción no puede tener más de 300 caracteres.');
        event.preventDefault();
        return;
    }

    // Validar thumbnail (opcional, formato .jpg, máx. 2 MB)
    if (thumbnailFile) {
        if (thumbnailFile.type !== 'image/jpeg' || thumbnailFile.size > 2 * 1024 * 1024) {
            alert('El thumbnail debe ser un archivo .jpg y no superar los 2 MB.');
            event.preventDefault();
            return;
        }
    }
});
