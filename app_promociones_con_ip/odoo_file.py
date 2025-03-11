import xmlrpc.client
from odoo import api, fields, models
'''
aqui tendremos que agregar la ip del cliente para poder realizar el envío de las notificaciones
'''
class FCMNotificationCron(models.Model):
    _name = "fcm.notification.cron"

    def enviar_notificaciones(self):
        # Servidor XML-RPC del cliente (app)
        rpc_url = "http://<ip-del-cliente>:8000/"  # Cambia la IP por la del dispositivo cliente
        server = xmlrpc.client.ServerProxy(rpc_url)

        # Mensaje a enviar
        mensaje = "Nueva promoción disponible. ¡No te lo pierdas!"
        try:
            resultado = server.recibir_notificacion(mensaje)
            if resultado:
                _logger.info("Notificación enviada correctamente al cliente.")
        except Exception as e:
            _logger.error(f"Error al enviar notificación al cliente: {e}")
