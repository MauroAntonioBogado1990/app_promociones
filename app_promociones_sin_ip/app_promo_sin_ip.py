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

    # Acción al hacer clic en el botón "Ver Productos"
    def ver_productos(e):
        page.launch_url("http://corporate.hcsinergia.com:10017/shop")

    # Configurar la pantalla inicial con el botón adicional
    page.add(
        ft.Column(
            controls=[
                ft.Text("Bienvenido a la App de Notificaciones Automáticas", size=24),
                notification_label,
                ft.ElevatedButton(
                    text="Ver Productos", 
                    on_click=ver_productos
                ),
            ]
        )
    )

ft.app(target=main)
