import yagmail # type: ignore
import os
from dotenv import load_dotenv

load_dotenv()

class Notification():
    
    _default_title = "PRICE_CHECKER - Actualización de precio de uno de los artículos"
    _dict_body = {
        "subida":"Ha SUBIDO el precio de {}.\n Precio actual: {}€. Precio anterior: {} € \n Enlace al producto: {}",
        "bajada":"Ha BAJADO el precio de {}.\n Precio actual: {}€. Precio anterior: {} € \n Enlace al producto: {}"
    }
    
    def __init__(self, correo_destino):
        self._email_origen = os.getenv("EMAIL")
        self._passw_origen = os.getenv("APP_PASSWORD")
        self._correo_destino = correo_destino
        self._yag = yagmail.SMTP(self._email_origen, self._passw_origen)
        
    def messages(self, msg_id):
        return self._dict_body[msg_id]

    def enviar_correo(self, contenido, titulo=_default_title):
        self._yag.send(
            to=self._correo_destino,
            subject=titulo,
            contents=contenido
        )