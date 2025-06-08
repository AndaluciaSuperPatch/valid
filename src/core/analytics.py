import sqlite3
from datetime import datetime
from typing import Dict, Any
import json

class Analytics:
    def __init__(self, db_path: str = 'analytics.db'):
        self.conn = sqlite3.connect(db_path)
        self._init_db()

    def _init_db(self):
        cursor = self.conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS events (
            id INTEGER PRIMARY KEY,
            event_name TEXT NOT NULL,
            event_data TEXT,
            timestamp DATETIME NOT NULL,
            source TEXT
        )
        ''')
        self.conn.commit()

    def track_event(self, event_name: str, data: Dict[str, Any] = None, 
                   source: str = 'system') -> bool:
        """Registra un evento en el sistema de analítica"""
        try:
            cursor = self.conn.cursor()
            cursor.execute('''
            INSERT INTO events (event_name, event_data, timestamp, source)
            VALUES (?, ?, ?, ?)
            ''', (event_name, json.dumps(data), datetime.now(), source))
            self.conn.commit()
            return True
        except Exception as e:
            print(f"Error tracking event: {e}")
            return False

    def get_conversion_rate(self, start_date: datetime, end_date: datetime) -> float:
        """Calcula la tasa de conversión entre dos fechas"""
        cursor = self.conn.cursor()
        
        # Total de leads
        cursor.execute('''
        SELECT COUNT(*) FROM events 
        WHERE event_name = 'new_lead' 
        AND timestamp BETWEEN ? AND ?
        ''', (start_date, end_date))
        total_leads = cursor.fetchone()[0] or 1
        
        # Total de conversiones
        cursor.execute('''
        SELECT COUNT(*) FROM events 
        WHERE event_name = 'sale_completed' 
        AND timestamp BETWEEN ? AND ?
        ''', (start_date, end_date))
        total_sales = cursor.fetchone()[0] or 0
        
        return (total_sales / total_leads) * 100
