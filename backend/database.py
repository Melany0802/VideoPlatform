from datetime import datetime
from requests import Session
from sqlalchemy import Boolean, DateTime, create_engine, Column, Integer, String, ForeignKey
from sqlalchemy.orm import sessionmaker, declarative_base, relationship

# Define la URL de conexión de tu base de datos
DATABASE_URL = "sqlite:///./test.db"  # Cambia a PostgreSQL o MySQL si es necesario

# Crea el motor de la base de datos
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})  # Para SQLite

# Crea una base declarativa
Base = declarative_base()

# Define el modelo de Video
class Video(Base):
    __tablename__ = "videos"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String)
    filename = Column(String)  # Asegúrate de que este sea el nombre correcto
    thumbnail = Column(String)
    views = Column(Integer, default=0)
    favorites = Column(Boolean, default=False)
    uploaded_at = Column(String)
    channel_name = Column(String, )

    # Relación con los comentarios
    comments = relationship("Comment", back_populates="video")

# Define el modelo de Comment
class Comment(Base):
    __tablename__ = "comments"

    id = Column(Integer, primary_key=True, index=True)
    content = Column(String)
    video_id = Column(Integer, ForeignKey("videos.id"))  # Relación con Video
    created_at = Column(DateTime, default=datetime.utcnow)

    # Relación inversa
    video = relationship("Video", back_populates="comments")

# Crea las tablas en la base de datos
def init_db():
    Base.metadata.create_all(bind=engine)

# Crea una sesión
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Dependencia para obtener la sesión
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_sample_data(db: Session):
    # Asegúrate de que la tabla de videos esté vacía antes de agregar datos de ejemplo
    db.query(Video).delete()  # Esto eliminará cualquier video existente, si deseas mantenerlos, quita esta línea

    sample_videos = [
        Video(
            title="Video de Ejemplo 1",
            description="Descripción de Video de Ejemplo 1",
            filename="video1.mp4",  
            thumbnail="thumbnail1.jpg",  
        ),
        Video(
            title="Video de Ejemplo 2",
            description="Descripción de Video de Ejemplo 2",
            filename="video2.mp4",  
            thumbnail="thumbnail2.jpg",  
        ),
    ]
    
    db.add_all(sample_videos)
    db.commit()
