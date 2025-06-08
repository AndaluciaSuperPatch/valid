import requests
from typing import Dict, Optional
import logging
from urllib.parse import urljoin

logger = logging.getLogger('LovableIntegration')

class LovableIntegration:
    def __init__(self, api_key: str, base_url: str = "https://api.lovableapp.com/v1"):
        self.base_url = base_url
        self.headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json"
        }

    def send_lead(self, lead_data: Dict) -> Optional[Dict]:
        """Envía un lead a la API de Lovable"""
        try:
            response = requests.post(
                urljoin(self.base_url, "/leads"),
                json=lead_data,
                headers=self.headers,
                timeout=10
            )
            
            if response.status_code == 201:
                logger.info(f"Lead enviado a Lovable: {lead_data.get('phone')}")
                return response.json()
            
            logger.error(f"Error enviando lead: {response.text}")
            return None
            
        except Exception as e:
            logger.error(f"Error de conexión con Lovable: {e}")
            return None

    def track_sale(self, sale_data: Dict) -> bool:
        """Registra una venta en Lovable"""
        try:
            response = requests.post(
                urljoin(self.base_url, "/sales"),
                json=sale_data,
                headers=self.headers,
                timeout=10
            )
            return response.status_code == 201
        except Exception as e:
            logger.error(f"Error registrando venta: {e}")
            return False
