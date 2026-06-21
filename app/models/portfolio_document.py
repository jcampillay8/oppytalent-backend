from sqlalchemy import Column, Integer, String, Text, ForeignKey, Index
from sqlalchemy.orm import mapped_column
from pgvector.sqlalchemy import Vector
from app.database import Base

class PortfolioDocument(Base):
    __tablename__ = "portfolio_documents"
    
    __table_args__ = (
        Index('ix_portfolio_documents_embedding', 'embedding', postgresql_using='hnsw', postgresql_with={'m': 16, 'ef_construction': 64}, postgresql_ops={'embedding': 'vector_cosine_ops'}),
    )

    id = Column(Integer, primary_key=True, index=True)
    usuario_id = Column(Integer, ForeignKey("usuarios.id", ondelete="CASCADE"), nullable=False, index=True)
    
    # PERFIL, EXPERIENCIA, PROYECTO, ESTUDIO, RECONOCIMIENTO, HABILITACION
    tipo_entidad = Column(String(50), nullable=False, index=True)
    
    entidad_id = Column(Integer, nullable=False, index=True)
    
    contenido_texto = Column(Text, nullable=False)
    
    # Usaremos modelos de Gemini que entregan embeddings de 768 dimensiones
    embedding = mapped_column(Vector(768))

