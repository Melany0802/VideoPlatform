from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from datetime import datetime

# Define la URL de la base de datos (actualiza esto según tus necesidades)
DATABASE_URL = "sqlite:///./test.db"  # Cambia esto a tu base de datos real

# Crea el motor
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # Solo necesario para SQLite

# Crea una base declarativa
Base = declarative_base()

# Define el modelo de Video
class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    filename = Column(String, nullable=False)
    thumbnail = Column(String, nullable=True)
    views = Column(Integer, default=0)
    favorites = Column(Boolean, default=False)
    uploaded_at = Column(DateTime, default=datetime.utcnow)
    channel_name = Column(String, nullable=False)

    # Relación con el modelo Comment
    comments = relationship("Comment", back_populates="video", cascade="all, delete-orphan")

# Define el modelo de Comment
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String, nullable=False)
    video_id = Column(Integer, ForeignKey("videos.id"), nullable=False)  # Relación con Video
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación inversa
    video = relationship("Video", back_populates="comments")

# Crea una fábrica de sesiones
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Función para inicializar la base de datos
def init_db():
    Base.metadata.create_all(bind=engine)
