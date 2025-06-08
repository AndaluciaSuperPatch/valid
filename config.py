import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Configuración de Lovable
    LOVABLE_API_KEY = os.getenv('LOVABLE_API_KEY')
    LOVABLE_BASE_URL = os.getenv('LOVABLE_BASE_URL', 'https://api.lovableapp.com/v1')
    
    # Configuración de la base de datos
    DB_PATH = os.getenv('DB_PATH', 'data/leads.db')
    ANALYTICS_DB_PATH = os.getenv('ANALYTICS_DB_PATH', 'data/analytics.db')
    
    # Configuración del bot
    INITIAL_MESSAGE = os.getenv('INITIAL_MESSAGE', "¡Hola! ¿En qué podemos ayudarte?")
    FOLLOW_UP_DELAY = int(os.getenv('FOLLOW_UP_DELAY', 2))  # días
    
    @classmethod
    def to_dict(cls):
        return {
            'lovable_api_key': cls.LOVABLE_API_KEY,
            'lovable_base_url': cls.LOVABLE_BASE_URL,
            'db_path': cls.DB_PATH,
            'sync_with_lovable': bool(cls.LOVABLE_API_KEY)
        }
