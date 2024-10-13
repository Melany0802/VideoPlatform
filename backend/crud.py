from fastapi import HTTPException
from sqlalchemy.orm import Session
from . import models
from . import schemas

# Buscar videos por título
async def search_videos_in_db(query: str, db: Session):
    try:
        results = db.query(models.Video).filter(models.Video.title.ilike(f"%{query}%")).all()
        return results
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obtener los videos más vistos
def get_top_viewed_videos(db: Session, limit: int = 10):
    print("Getting top viewed videos")
    try:
        # Realiza la consulta para obtener los videos más vistos
        top_viewed_videos = db.query(models.Video).order_by(models.Video.views.desc()).limit(limit).all()
        
        # Verifica si hay videos disponibles
        if not top_viewed_videos:
            return {"message": "No hay videos disponibles."}
        
        return top_viewed_videos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
# Obtener los videos favoritos recientes
def get_top_favorite_videos(db: Session, limit: int = 10):
    print("Getting top favorite videos")
    try:
        # Realiza la consulta para obtener los videos favoritos
        favorite_videos = db.query(models.Video).filter(models.Video.favorites == True).order_by(models.Video.uploaded_at.desc()).limit(limit).all()
        
        # Verifica si hay videos favoritos
        if not favorite_videos:
            return {"message": "No hay videos favoritos disponibles."}
        
        return favorite_videos
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Buscar videos por título o descripción
def search_videos(db: Session, query: str):
    try:
        return db.query(models.Video).filter(
            (models.Video.title.ilike(f"%{query}%")) |
            (models.Video.description.ilike(f"%{query}%"))
        ).all()
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Obtener un video por su ID
def get_video_by_id(db: Session, video_id: int):
    video = db.query(models.Video).filter(models.Video.id == video_id).first()
    if video is None:
        raise HTTPException(status_code=404, detail="Video not found")
    return video

# Crear un nuevo video
def create_video(db: Session, video: schemas.VideoCreate):
    db_video = models.Video(
        title=video.title,
        description=video.description,
        filename=video.filename,
        thumbnail=video.thumbnail,
        channel_name=video.channel_name,
        views=0,
        favorites=False
    )
    try:
        db.add(db_video)
        db.commit()
        db.refresh(db_video)
        return db_video
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Incrementar las vistas de un video
def increment_video_views(db: Session, video_id: int):
    video = get_video_by_id(db, video_id)
    if video:
        video.views += 1
        db.commit()
        return {"message": "Views updated successfully"}
    else:
        raise HTTPException(status_code=404, detail="Video not found")

# Crear un nuevo comentario
def create_comment(db: Session, comment: schemas.CommentCreate, video_id: int):
    db_comment = models.Comment(
        content=comment.content,
        video_id=video_id
    )
    try:
        db.add(db_comment)
        db.commit()
        db.refresh(db_comment)
        return db_comment
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

def upload_video(db: Session, video: schemas.VideoCreate):
    db_video = models.Video(
        title=video.title,
        description=video.description,
        filename=video.filename,
        thumbnail=video.thumbnail,
        channel_name=video.channel_name,
        views=0,
        favorites=False
    )
    try:
        db.add(db_video)
        db.commit()
        db.refresh(db_video)
        return db_video
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))