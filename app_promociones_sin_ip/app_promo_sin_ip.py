import flet as ft
from xmlrpc.server import SimpleXMLRPCServer
import threading  # Para ejecutar el servidor en paralelo

def main(page: ft.Page):
    page.title = "App de Notificaciones Automáticas"

    notification_label = ft.Text("Esperando notificaciones...", size=18)

    # Clase para manejar notificaciones desde Odoo
    class NotificationServer:
        def recibir_notificacion(self, mensaje):
            """Recibe las notificaciones enviadas por Odoo."""
            notification_label.value = f"Nueva notificación recibida: {mensaje}"
            page.update()
            print(f"Notificación recibida: {mensaje}")
            return True  # Confirma que el mensaje fue procesado

    # Configurar el servidor XML-RPC
    server = SimpleXMLRPCServer(("0.0.0.0", 8000), allow_none=True)
    server.register_instance(NotificationServer())

    # Iniciar el servidor en un hilo separado
    def iniciar_servidor():
        print("Servidor XML-RPC escuchando en el puerto 8000...")
        server.serve_forever()

    threading.Thread(target=iniciar_servidor, daemon=True).start()

    # Configurar la pantalla inicial
    page.add(
        ft.Column(
            controls=[
                ft.Text("Bienvenido a la App de Notificaciones Automáticas", size=24),
                notification_label,
            ]
        )
    )

ft.app(target=main)
