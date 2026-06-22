import os
from google import genai
from typing import List
from app.config import settings

def generate_embedding(text: str, api_key: str = None) -> List[float]:
    """
    Genera un embedding de texto utilizando el modelo de Google Gemini.
    Retorna una lista de floats de 768 dimensiones.
    """
    api_key_to_use = api_key or settings.gemini_api_key
    client = genai.Client(api_key=api_key_to_use)
        
    model = 'gemini-embedding-2'
    
    try:
        response = client.models.embed_content(
            model=model,
            contents=text,
            config=dict(output_dimensionality=768)
        )
        return response.embeddings[0].values
    except Exception as e:
        print(f"Error generando embedding: {e}")
        raise e
