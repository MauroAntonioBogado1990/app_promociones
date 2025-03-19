import flet as ft
from xmlrpc.server import SimpleXMLRPCServer
import threading  # Para ejecutar el servidor en paralelo
import base64
from io import BytesIO
from PIL import Image  # Necesario para manejar imágenes

def main(page: ft.Page):
    page.title = "App de Notificaciones Automáticas"

    notification_label = ft.Text("Esperando notificaciones...", size=18)
    notification_image = ft.Image(src="", fit=ft.ImageFit.CONTAIN, width=300, height=300)

    # Clase para manejar notificaciones desde Odoo
    class NotificationServer:
        def recibir_notificacion(self, data):
            """
            Recibe las notificaciones enviadas por Odoo.
            data: Diccionario que contiene 'mensaje' y 'imagen' (base64).
            """
            mensaje = data.get('mensaje', 'Sin mensaje')
            imagen_base64 = data.get('imagen')

            # Actualizar el texto de la notificación
            notification_label.value = f"Nueva notificación: {mensaje}"
            print(f"Notificación recibida: {mensaje}")

            # Procesar la imagen si está disponible
            if imagen_base64:
                try:
                    # Decodificar la imagen desde base64
                    image_bytes = base64.b64decode(imagen_base64)
                    image = Image.open(BytesIO(image_bytes))

                    # Guardar temporalmente la imagen y actualizar la vista
                    temp_image_path = "temp_image.png"
                    image.save(temp_image_path, format="PNG")
                    notification_image.src = temp_image_path
                except Exception as e:
                    print(f"Error al procesar la imagen: {e}")
                    notification_image.src = ""
            else:
                notification_image.src = ""  # Limpiar imagen si no se envía ninguna

            page.update()
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
                notification_image,
                ft.ElevatedButton(
                    text="Ver Productos", 
                    on_click=ver_productos
                ),
            ]
        )
    )

ft.app(target=main)

