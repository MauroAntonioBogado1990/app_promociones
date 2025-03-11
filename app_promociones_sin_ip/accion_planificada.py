"""
Esta es una accion planificada para poder realizar el envío de notificaciones push
"""



def enviar_notificaciones(self):
    """Enviar notificaciones automáticamente a los clientes registrados."""
    clientes = self.env['res.partner'].search([('app_server_url', '!=', False)])
    for cliente in clientes:
        rpc_url = cliente.app_server_url  # URL del servidor cliente
        try:
            server = xmlrpc.client.ServerProxy(rpc_url)
            mensaje = f"Hola {cliente.name}, ¡nueva promoción disponible!"
            resultado = server.recibir_notificacion(mensaje)
            if resultado:
                _logger.info(f"Notificación enviada a {cliente.name}")
            else:
                _logger.warning(f"{cliente.name} no confirmó recepción.")
        except Exception as e:
            _logger.error(f"Error al enviar notificación a {cliente.name}: {e}")
