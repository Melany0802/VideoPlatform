import logging
from fastapi import FastAPI, HTTPException, Request, Depends
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from sqlalchemy.orm import Session
from typing import List

from . import crud, models, schemas
from .database import SessionLocal, engine
from fastapi.middleware.cors import CORSMiddleware


# Crear las tablas de la base de datos
models.Base.metadata.create_all(bind=engine)

app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Cambia esto por los dominios específicos en producción
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Montar la carpeta de archivos estáticos
app.mount("/static", StaticFiles(directory="backend/static"), name="static")

# Configurar las plantillas HTML usando Jinja2
templates = Jinja2Templates(directory="frontend/templates")


# Dependencia: obtener una sesión de la base de datos
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# Página de inicio (index.html)
@app.get("/", response_class=HTMLResponse)
async def read_root(request: Request, limit: int = 10, db: Session = Depends(get_db)):
    logging.info(f"Fetching top viewed videos with limit: {limit}")
    videos = crud.get_top_viewed_videos(db, limit)
    return templates.TemplateResponse("index.html", {"request": request, "videos": videos})

# Formulario para agregar un video (FormVideo.html)
@app.get("/form", response_class=HTMLResponse)
async def form_video(request: Request):
    return templates.TemplateResponse("FormVideo.html", {"request": request})


# Página de detalles de un video (view_video.html)
@app.get("/view/{video_id}", response_class=HTMLResponse)
async def view_video(request: Request, video_id: int, db: Session = Depends(get_db)):
    video = crud.get_video_by_id(db, video_id=video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return templates.TemplateResponse("view_video.html", {"request": request, "video": video})


# Servicio GET: los 10 videos más vistos
@app.get("/videos/top-favorites")
async def get_top_favorite_videos(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_top_favorite_videos(db, limit=limit)


# Servicio GET: los 10 videos favoritos más recientes
@app.get("/videos/top-viewed")
async def get_top_viewed_videos(limit: int = 10, db: Session = Depends(get_db)):
    return crud.get_top_viewed_videos(db, limit=limit)


# Servicio POST: agregar un nuevo video
@app.post("/videos/", response_model=schemas.Video)
def create_video(video: schemas.VideoCreate, db: Session = Depends(get_db)):
    return crud.create_video(db=db, video=video)


# Servicio GET: buscar videos
@app.get("/videos/search/", response_model=List[schemas.Video])
def search_videos(query: str, db: Session = Depends(get_db)):
    videos = crud.search_videos(db, query=query)
    if not videos:
        raise HTTPException(status_code=404, detail="No videos found")
    return videos


# Servicio GET: cargar un video y sus datos
@app.get("/videos/{video_id}", response_model=schemas.Video)
def read_video(video_id: int, db: Session = Depends(get_db)):
    video = crud.get_video_by_id(db, video_id=video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


# Servicio PUT: incrementar las reproducciones de un video
@app.put("/videos/{video_id}/views", response_model=schemas.Video)
def increment_video_views(video_id: int, db: Session = Depends(get_db)):
    video = crud.increment_views(db, video_id=video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


# Servicio PUT: agregar un video a favoritos
@app.put("/videos/{video_id}/favorites", response_model=schemas.Video)
def add_video_to_favorites(video_id: int, db: Session = Depends(get_db)):
    video = crud.add_to_favorites(db, video_id=video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


# Servicio DELETE: quitar un video de favoritos
@app.delete("/videos/{video_id}/favorites", response_model=schemas.Video)
def remove_video_from_favorites(video_id: int, db: Session = Depends(get_db)):
    video = crud.remove_from_favorites(db, video_id=video_id)
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return video


# Servicio GET: cargar comentarios de un video
@app.get("/videos/{video_id}/comments", response_model=List[schemas.Comment])
def get_video_comments(video_id: int, db: Session = Depends(get_db)):
    comments = crud.get_comments_by_video_id(db, video_id=video_id)
    if not comments:
        raise HTTPException(status_code=404, detail="No comments found")
    return comments


# Servicio POST: agregar un comentario a un video
@app.post("/videos/{video_id}/comments", response_model=schemas.Comment)
def add_comment_to_video(video_id: int, comment: schemas.CommentCreate, db: Session = Depends(get_db)):
    return crud.create_comment(db=db, comment=comment, video_id=video_id)
