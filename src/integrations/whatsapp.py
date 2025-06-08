from twilio.rest import Client
from typing import Dict, Optional
import logging
from src.utils.logger import setup_logger

logger = setup_logger('WhatsAppIntegration')

class WhatsAppIntegration:
    def __init__(self, account_sid: str, auth_token: str, twilio_number: str):
        self.client = Client(account_sid, auth_token)
        self.twilio_number = twilio_number
        logger.info("WhatsApp Integration inicializada")

    def send_template_message(self, to: str, template_name: str, 
                           parameters: Dict = None) -> bool:
        """Envía un mensaje template de WhatsApp"""
        try:
            message = self.client.messages.create(
                from_=f'whatsapp:{self.twilio_number}',
                to=f'whatsapp:{to}',
                body=self._format_template(template_name, parameters)
            )
            logger.info(f"Mensaje enviado a {to}: {message.sid}")
            return True
        except Exception as e:
            logger.error(f"Error enviando mensaje WhatsApp: {e}")
            return False

    def _format_template(self, template_name: str, parameters: Dict) -> str:
        """Formatea un mensaje template con parámetros"""
        templates = {
            'welcome': (
                "¡Hola {name}! Gracias por contactarnos. "
                "¿Cómo podemos ayudarte hoy?"
            ),
            'follow_up': (
                "Hola {name}, ¿todavía estás interesado en {product}? "
                "Estamos aquí para ayudarte."
            ),
            'sale_confirmation': (
                "¡Gracias por tu compra, {name}! "
                "Tu pedido #{order_id} está siendo procesado."
            )
        }
        
        template = templates.get(template_name, template_name)
        return template.format(**parameters) if parameters else template

    def process_incoming_message(self, message_data: Dict) -> Optional[Dict]:
        """Procesa un mensaje entrante de WhatsApp"""
        try:
            return {
                'from': message_data.get('From', '').replace('whatsapp:', ''),
                'body': message_data.get('Body'),
                'timestamp': message_data.get('DateSent'),
                'message_id': message_data.get('Sid')
            }
        except Exception as e:
            logger.error(f"Error procesando mensaje: {e}")
            return None
