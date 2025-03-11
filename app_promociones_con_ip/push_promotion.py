import flet as ft
from xmlrpc.server import SimpleXMLRPCServer
import threading  # Para ejecutar el servidor de manera independiente

"""
aqui realiza el envio de las notificaciones pero tenemos que tener en cuenta que para poder recibir las
notidicaciones tenemos que tener el ip del cliente, esteblecido en el archivo odoo_file.py
"""

def main(page: ft.Page):
    page.title = "App de Notificaciones Automáticas"

    notification_label = ft.Text("Esperando notificaciones...", size=18)

    # Clase del servidor para recibir notificaciones de Odoo
    class NotificationServer:
        def recibir_notificacion(self, mensaje):
            """Esta función será llamada desde Odoo vía XML-RPC."""
            notification_label.value = f"Nueva notificación: {mensaje}"
            page.update()
            print(f"Notificación recibida: {mensaje}")
            return True  # Confirma que el mensaje fue recibido correctamente

    # Configurar el servidor XML-RPC
    server = SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True)
    server.register_instance(NotificationServer())

    # Ejecuta el servidor en un hilo separado
    def iniciar_servidor():
        print("Servidor XML-RPC escuchando en el puerto 8000...")
        server.serve_forever()

    threading.Thread(target=iniciar_servidor, daemon=True).start()

    # Pantalla inicial
    page.add(
        ft.Column(
            controls=[
                ft.Text("Bienvenido a la App de Notificaciones", size=24),
                notification_label,
            ]
        )
    )

ft.app(target=main)
