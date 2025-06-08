import os
from src.core.database import DatabaseManager
from src.core.analytics import Analytics

def initialize_system():
    """Inicializa el sistema creando las bases de datos necesarias"""
    # Crear directorio data si no existe
    os.makedirs('data', exist_ok=True)
    
    # Inicializar base de datos principal
    db = DatabaseManager(os.getenv('DB_PATH', 'data/leads.db'))
    db.close()
    
    # Inicializar base de datos de analítica
    analytics_db = Analytics(os.getenv('ANALYTICS_DB_PATH', 'data/analytics.db'))
    
    print("Sistema inicializado correctamente")

if __name__ == '__main__':
    initialize_system()
