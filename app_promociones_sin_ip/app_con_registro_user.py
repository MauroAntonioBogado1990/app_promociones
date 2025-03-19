import flet as ft
from xmlrpc.server import SimpleXMLRPCServer
import threading  # Para ejecutar el servidor en paralelo
import base64
from io import BytesIO
from PIL import Image  # Necesario para manejar imágenes
import xmlrpc.client

def main(page: ft.Page):
    page.title = "App de Notificaciones Automáticas"

    # URL y DB de Odoo
    odoo_url = "http://corporate.hcsinergia.com:10017/"
    db = "distri_demo_eccomerce"

    # Componentes de la pantalla de registro
    username_input = ft.TextField(label="Username", width=300)
    password_input = ft.TextField(label="Password", password=True, width=300)
    status_label = ft.Text(value="", size=14, color="red")
    register_button = ft.ElevatedButton(text="Registrar Dispositivo")

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

    # Acción al hacer clic en el botón "Registrar Dispositivo"
    def autenticar_usuario(e):
        username = username_input.value
        password = password_input.value
        rpc_url = "http://<ip_dispositivo>:8000"  # URL del servidor XML-RPC del cliente
        
        try:
            # Conexión con Odoo
            common = xmlrpc.client.ServerProxy(f"{odoo_url}/xmlrpc/2/common")
            uid = common.authenticate(db, username, password, {})
            
            if uid:
                # Registrar el rpc_url en Odoo
                models = xmlrpc.client.ServerProxy(f"{odoo_url}/xmlrpc/2/object")
                partner_id = models.execute_kw(
                    db, uid, password, 'res.partner', 'search', [[('email', '=', username)]]
                )
                if partner_id:
                    result = models.execute_kw(
                        db, uid, password, 'res.partner', 'write', [[partner_id[0]], {'app_server_url': rpc_url}]
                    )
                    if result:
                        status_label.value = "Dispositivo registrado exitosamente."
                        status_label.color = "green"
                    else:
                        status_label.value = "Error al registrar el dispositivo."
                        status_label.color = "red"
                else:
                    status_label.value = "Usuario no encontrado en Odoo."
                    status_label.color = "red"
            else:
                status_label.value = "Credenciales incorrectas."
                status_label.color = "red"

        except Exception as ex:
            status_label.value = f"Error: {ex}"
            status_label.color = "red"
        
        page.update()

    register_button.on_click = autenticar_usuario

    # Acción al hacer clic en el botón "Ver Productos"
    def ver_productos(e):
        page.launch_url("http://corporate.hcsinergia.com:10017/shop")

    # Configurar la pantalla inicial con las secciones combinadas
    page.add(
        ft.Column(
            controls=[
                ft.Text("Registro de Cliente", size=24),
                username_input,
                password_input,
                register_button,
                status_label,
                ft.Divider(height=20, color="grey"),
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
