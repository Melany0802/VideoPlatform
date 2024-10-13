from datetime import datetime
from pydantic import BaseModel
from typing import Optional

# Esquema para un video existente
class Video(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    filename: str
    thumbnail: str
    views: int
    favorites: bool
    uploaded_at: datetime  # Cambiado a datetime para mantener el tipo correcto
    channel_name: Optional[str] = None  # Cambiado a Optional para permitir que sea None

    class Config:
        orm_mode = True

# Esquema para crear un nuevo video
class VideoCreate(BaseModel):
    title: str
    description: Optional[str] = None
    filename: str
    thumbnail: Optional[str] = None  # Cambiado a Optional si no se requiere al crear
    favorites: bool = False  # Default a False si no se proporciona
    channel_name: Optional[str] = None

# Esquema de un comentario
class Comment(BaseModel):
    id: int
    content: str
    video_id: int
    created_at: Optional[datetime] = None  # Cambiado a datetime

    class Config:
        orm_mode = True  # Cambiado a orm_mode para la compatibilidad con la base de datos

# Esquema para crear un nuevo comentario
class CommentCreate(BaseModel):
    content: str

# Esquema de respuesta para un video
class VideoResponse(BaseModel):
    id: int
    title: str
    description: Optional[str] = None
    filename: str
    thumbnail: str
    views: int
    favorites: bool
    uploaded_at: datetime  # Cambiado a datetime para mantener el tipo correcto
    channel_name: Optional[str] = None

    class Config:
        orm_mode = True  # Cambiado a orm_mode para la compatibilidad con la base de datos
