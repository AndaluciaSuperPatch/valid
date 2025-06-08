import sqlite3
from datetime import datetime
import logging
from typing import Optional, Dict, List
from src.integrations.lovable import LovableIntegration
from src.core.analytics import Analytics
from src.utils.logger import setup_logger

logger = setup_logger('LeadFlowBot')

class LeadFlowBot:
    def __init__(self, config: Dict):
        self.config = config
        self.db_path = config.get('db_path', 'leads.db')
        self.conn = sqlite3.connect(self.db_path)
        self.lovable = LovableIntegration(config['lovable_api_key'])
        self.analytics = Analytics()
        self._init_db()
        logger.info("LeadFlowBot inicializado")

    def _init_db(self):
        """Inicializa la estructura de la base de datos"""
        cursor = self.conn.cursor()
        
        # Tabla de leads
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY,
            phone TEXT UNIQUE,
            name TEXT,
            email TEXT,
            status TEXT DEFAULT 'new',
            source TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_contact TIMESTAMP
        )
        ''')
        
        # Tabla de interacciones
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS interactions (
            id INTEGER PRIMARY KEY,
            lead_id INTEGER,
            interaction_type TEXT,
            notes TEXT,
            timestamp TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lead_id) REFERENCES leads(id)
        )
        ''')
        self.conn.commit()

    def add_lead(self, phone: str, name: Optional[str] = None, 
                email: Optional[str] = None, source: str = 'organic') -> bool:
        """Añade un nuevo lead al sistema"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            INSERT INTO leads (phone, name, email, source, last_contact)
            VALUES (?, ?, ?, ?, ?)
            ON CONFLICT(phone) DO UPDATE SET
                name = excluded.name,
                email = excluded.email,
                last_contact = excluded.last_contact
            ''', (phone, name, email, source, datetime.now()))
            
            self.conn.commit()
            self.analytics.track_event('new_lead', {'phone': phone, 'source': source})
            
            # Enviar a Lovable
            if self.config.get('sync_with_lovable', False):
                self.lovable.send_lead({
                    'phone': phone,
                    'name': name,
                    'email': email,
                    'source': source
                })
            
            logger.info(f"Nuevo lead añadido: {phone}")
            return True
            
        except Exception as e:
            logger.error(f"Error añadiendo lead: {e}")
            return False

    def get_leads(self, status: Optional[str] = None) -> List[Dict]:
        """Obtiene todos los leads filtrados por estado"""
        cursor = self.conn.cursor()
        
        query = 'SELECT * FROM leads'
        params = []
        
        if status:
            query += ' WHERE status = ?'
            params.append(status)
            
        cursor.execute(query, params)
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

if __name__ == '__main__':
    # Ejemplo de uso
    config = {
        'lovable_api_key': 'tu_api_key',
        'sync_with_lovable': True,
        'db_path': 'leads.db'
    }
    
    bot = LeadFlowBot(config)
    bot.add_lead("+1234567890", "Ejemplo Lead", "lead@example.com")
    print("Leads:", bot.get_leads())
