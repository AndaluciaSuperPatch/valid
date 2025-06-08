import sqlite3
from typing import Dict, List, Optional
from datetime import datetime
import logging

logger = logging.getLogger('Database')

class DatabaseManager:
    def __init__(self, db_path: str):
        self.conn = sqlite3.connect(db_path)
        self._initialize_tables()

    def _initialize_tables(self):
        """Crea las tablas necesarias si no existen"""
        cursor = self.conn.cursor()
        
        # Tabla de leads
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS leads (
            id INTEGER PRIMARY KEY,
            phone TEXT UNIQUE NOT NULL,
            name TEXT,
            email TEXT,
            status TEXT DEFAULT 'new',
            source TEXT,
            campaign TEXT,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_contact TIMESTAMP,
            metadata TEXT
        )
        ''')
        
        # Tabla de ventas
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS sales (
            id INTEGER PRIMARY KEY,
            lead_id INTEGER NOT NULL,
            amount REAL NOT NULL,
            product_id TEXT NOT NULL,
            status TEXT DEFAULT 'pending',
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            FOREIGN KEY (lead_id) REFERENCES leads (id)
        )
        ''')
        
        self.conn.commit()
        logger.info("Tablas de base de datos inicializadas")

    def execute_query(self, query: str, params: tuple = ()) -> List[Dict]:
        """Ejecuta una consulta y devuelve los resultados como diccionarios"""
        cursor = self.conn.cursor()
        cursor.execute(query, params)
        
        if not cursor.description:
            self.conn.commit()
            return []
            
        columns = [col[0] for col in cursor.description]
        return [dict(zip(columns, row)) for row in cursor.fetchall()]

    def add_lead(self, lead_data: Dict) -> bool:
        """Añade un nuevo lead a la base de datos"""
        required_fields = ['phone']
        if not all(field in lead_data for field in required_fields):
            raise ValueError(f"Faltan campos requeridos: {required_fields}")
        
        query = '''
        INSERT INTO leads (
            phone, name, email, status, source, campaign, last_contact, metadata
        ) VALUES (?, ?, ?, ?, ?, ?, ?, ?)
        ON CONFLICT(phone) DO UPDATE SET
            name = excluded.name,
            email = excluded.email,
            last_contact = excluded.last_contact,
            metadata = excluded.metadata
        '''
        
        params = (
            lead_data['phone'],
            lead_data.get('name'),
            lead_data.get('email'),
            lead_data.get('status', 'new'),
            lead_data.get('source', 'organic'),
            lead_data.get('campaign'),
            datetime.now(),
            lead_data.get('metadata')
        )
        
        try:
            self.execute_query(query, params)
            logger.info(f"Lead añadido/actualizado: {lead_data['phone']}")
            return True
        except Exception as e:
            logger.error(f"Error añadiendo lead: {e}")
            return False

    def close(self):
        """Cierra la conexión a la base de datos"""
        self.conn.close()
        logger.info("Conexión a base de datos cerrada")
