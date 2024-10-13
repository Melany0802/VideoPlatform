document.addEventListener('DOMContentLoaded', () => {
  const topVideosContainer = document.getElementById('topVideosContainer');
  const favoriteVideosContainer = document.getElementById('favoriteVideosContainer');
  const searchInput = document.getElementById('searchInput');

  const API_BASE_URL = 'http://localhost:8000'; // URL base de la API FastAPI

  const createVideoCard = (video) => {
      const col = document.createElement('div');
      col.className = 'col-md-4 mb-4';

      const card = document.createElement('div');
      card.className = 'card h-100';
      card.style.cursor = 'pointer';
      card.dataset.videoId = video.id;

      const img = document.createElement('img');
      img.src = `${API_BASE_URL}/thumbnails/${video.thumbnail}`;
      img.className = 'card-img-top';
      img.alt = `Thumbnail de ${video.title}`;

      const cardBody = document.createElement('div');
      cardBody.className = 'card-body';

      const title = document.createElement('h5');
      title.className = 'card-title';
      title.textContent = video.title;

      const viewsTime = document.createElement('div');
      viewsTime.className = 'views-time';

      const views = document.createElement('span');
      views.innerHTML = `<i class="fas fa-eye"></i> ${video.views} vistas`;

      const timeAgo = document.createElement('span');
      timeAgo.textContent = getTimeAgo(video.uploaded_at);

      viewsTime.appendChild(views);
      viewsTime.appendChild(timeAgo);

      cardBody.appendChild(title);
      cardBody.appendChild(viewsTime);

      card.appendChild(img);
      card.appendChild(cardBody);
      col.appendChild(card);

      card.addEventListener('click', () => {
          window.location.href = `video.html?id=${video.id}`;
      });

      return col;
  };

  const getTimeAgo = (dateString) => {
      const date = new Date(dateString);
      const now = new Date();
      const diffTime = Math.abs(now - date);
      const diffDays = Math.ceil(diffTime / (1000 * 60 * 60 * 24));
      return `${diffDays} días atrás`;
  };

  const loadTopVideos = async () => {
      try {
          const response = await fetch(`${API_BASE_URL}/videos/top-viewed?limit=10`);
          if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
          }
          const videos = await response.json();
          renderVideos(videos, topVideosContainer);
      } catch (error) {
          console.error('Error al cargar los videos más vistos:', error);
      }
  };

  const loadFavoriteVideos = async () => {
      try {
          const response = await fetch(`${API_BASE_URL}/videos/top-favorites?limit=10`);
          if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
          }
          const result = await response.json();

          // Verificar si el resultado es un mensaje o una lista de videos
          if (result.message) {
              favoriteVideosContainer.innerHTML = `<div class="alert alert-warning">${result.message}</div>`;
          } else {
              renderVideos(result, favoriteVideosContainer);
          }
      } catch (error) {
          console.error('Error al cargar los videos favoritos recientes:', error);
          favoriteVideosContainer.innerHTML = `<div class="alert alert-danger">Error al cargar los videos favoritos.</div>`;
      }
  };

  const renderVideos = (videos, container) => {
      container.innerHTML = ''; // Limpiar contenido existente

      if (videos.length === 0) {
          container.innerHTML = '<div class="alert alert-info">No hay videos para mostrar.</div>';
          return;
      }

      videos.forEach((video, index) => {
          if (index % 3 === 0) { // Cada 3 videos crean un nuevo "carousel-item"
              const carouselItem = document.createElement('div');
              carouselItem.className = 'carousel-item' + (index === 0 ? ' active' : '');

              const row = document.createElement('div');
              row.className = 'row';

              for (let i = index; i < index + 3 && i < videos.length; i++) {
                  const videoCard = createVideoCard(videos[i]);
                  row.appendChild(videoCard);
              }

              carouselItem.appendChild(row);
              container.appendChild(carouselItem);
          }
      });
  };

  const searchVideos = async (query) => {
      try {
          const response = await fetch(`${API_BASE_URL}/videos/search?q=${encodeURIComponent(query)}`);
          if (!response.ok) {
              throw new Error(`HTTP error! status: ${response.status}`);
          }
          const videos = await response.json();
          renderVideos(videos, topVideosContainer);
          renderVideos([], favoriteVideosContainer); // Limpiar favoritos si es necesario
      } catch (error) {
          console.error('Error al buscar videos:', error);
      }
  };

  searchInput.addEventListener('keyup', (e) => {
      const query = e.target.value.trim().toLowerCase();
      if (query.length > 2) {
          searchVideos(query);
      } else if (query.length === 0) {
          loadTopVideos();
          loadFavoriteVideos();
      }
  });

  // Cargar videos al inicio
  loadTopVideos();
  loadFavoriteVideos();
});
