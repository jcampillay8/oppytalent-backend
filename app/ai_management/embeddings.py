import os
import google.generativeai as genai
from typing import List

# Configurar genai si no se ha configurado (generalmente se hace en otro lado o aquí con variables de entorno)
# En OppyTalent se asume que la clave de Google Gemini se pasa globalmente o en cada request.
# Para este servicio base, podemos requerir la api_key o tomarla del entorno.

def generate_embedding(text: str, api_key: str = None) -> List[float]:
    """
    Genera un embedding de texto utilizando el modelo de Google Gemini (text-embedding-004).
    Retorna una lista de floats de 768 dimensiones.
    """
    if api_key:
        genai.configure(api_key=api_key)
    elif os.getenv("GEMINI_API_KEY"):
        genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
        
    # El modelo más reciente para embeddings de texto
    model = 'models/text-embedding-004'
    
    try:
        result = genai.embed_content(
            model=model,
            content=text,
            task_type="retrieval_document"
        )
        # result['embedding'] es una lista de floats
        return result['embedding']
    except Exception as e:
        print(f"Error generando embedding: {e}")
        # En caso de error, retornamos un vector vacío o lanzamos excepción
        raise e
