// comments.js

// Selecciona el botón de comentario y el campo de entrada
const commentButton = document.querySelector('.boton_comment');
const commentInput = document.querySelector('input[placeholder="Add a comment..."]');

// Función para manejar la inserción de comentarios
const handleComment = async () => {
    const commentText = commentInput.value.trim();

    if (commentText === "") {
        alert("Please enter a comment before submitting.");
        return;
    }

    try {
        // Aquí puedes implementar la lógica para enviar el comentario a tu servidor
        const response = await fetch('/api/comments', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({ comment: commentText }),
        });

        if (response.ok) {
            const newComment = await response.json();
            displayComment(newComment); // Muestra el nuevo comentario en la interfaz
            commentInput.value = ""; // Limpia el campo de entrada
        } else {
            alert("Failed to submit comment.");
        }
    } catch (error) {
        console.error("Error submitting comment:", error);
        alert("An error occurred while submitting your comment.");
    }
};

// Función para mostrar un comentario en la interfaz
const displayComment = (comment) => {
    const commentsSection = document.querySelector('.comments-section'); // Asegúrate de tener un contenedor para los comentarios
    const commentElement = document.createElement('div');
    commentElement.className = 'comment'; // Puedes agregar estilos personalizados
    commentElement.innerText = comment.text; // Suponiendo que tu respuesta del servidor incluye un campo 'text'
    commentsSection.appendChild(commentElement);
};

// Añadir el evento al botón
commentButton.addEventListener('click', handleComment);
