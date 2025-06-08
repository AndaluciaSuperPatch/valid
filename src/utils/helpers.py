from datetime import datetime, timedelta
from typing import Dict, Any
import re
import logging

logger = logging.getLogger('Helpers')

def validate_phone(phone: str) -> bool:
    """Valida que un número de teléfono tenga formato correcto"""
    pattern = r'^\+?[\d\s\-\(\)]{7,15}$'
    return bool(re.match(pattern, phone))

def validate_email(email: str) -> bool:
    """Valida que un email tenga formato correcto"""
    pattern = r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$'
    return bool(re.match(pattern, email))

def format_currency(amount: float, currency: str = 'EUR') -> str:
    """Formatea una cantidad como moneda"""
    return f"{amount:.2f} {currency}"

def calculate_days_since(date_str: str) -> int:
    """Calcula días desde una fecha dada"""
    try:
        date_obj = datetime.strptime(date_str, '%Y-%m-%d %H:%M:%S')
        return (datetime.now() - date_obj).days
    except Exception as e:
        logger.error(f"Error calculando días: {e}")
        return 0

def clean_input_data(data: Dict[str, Any]) -> Dict[str, Any]:
    """Limpia y normaliza datos de entrada"""
    cleaned = {}
    for key, value in data.items():
        if isinstance(value, str):
            cleaned[key] = value.strip()
        elif value is not None:
            cleaned[key] = value
    return cleaned
