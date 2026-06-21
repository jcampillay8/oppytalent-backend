import os
from google import genai
from typing import List

def generate_embedding(text: str, api_key: str = None) -> List[float]:
    """
    Genera un embedding de texto utilizando el modelo de Google Gemini (text-embedding-004).
    Retorna una lista de floats de 768 dimensiones.
    """
    api_key_to_use = api_key or os.getenv("GEMINI_API_KEY")
    client = genai.Client(api_key=api_key_to_use)
        
    model = 'text-embedding-004'
    
    try:
        response = client.models.embed_content(
            model=model,
            contents=text,
        )
        return response.embeddings[0].values
    except Exception as e:
        print(f"Error generando embedding: {e}")
        raise e
