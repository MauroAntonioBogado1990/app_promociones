import flet as ft
import xmlrpc.client  # Para comunicarse con Odoo

"""
mediante este desarrollo se permite recibir notificaciones, 
pero se debe realizar una actualizacion mediante el boton 
para saber si hay una notificación envidada
Además de configurar los datos de conexión, url, nombre de base de datos
usuario y pass

"""

def main(page: ft.Page):
    page.title = "App de Notificaciones con Odoo y XML-RPC"

    notification_label = ft.Text("Esperando notificaciones...", size=18)
    server_url = "http://<odoo_server>:8069"  # Cambia esta URL a la de tu servidor Odoo
    db_name = "nombre_base_de_datos"  # Nombre de la base de datos de Odoo
    username = "tu_usuario_odoo"     # Usuario de Odoo
    password = "tu_contraseña_odoo"  # Contraseña del usuario

    # Función para volver a la pantalla principal
    def mostrar_pantalla_principal(e=None):
        page.controls.clear()  # Limpia los controles actuales
        page.add(
            ft.Column(
                controls=[
                    ft.Text("Bienvenido a la App de Notificaciones", size=20),
                    get_notifications_button,
                    notification_label,
                ]
            )
        )
        page.update()

    # Función para obtener notificaciones desde Odoo mediante XML-RPC
    def obtener_notificaciones(e):
        try:
            # Conexión al servidor XML-RPC de Odoo
            common = xmlrpc.client.ServerProxy(f"{server_url}/xmlrpc/2/common")
            uid = common.authenticate(db_name, username, password, {})
            if not uid:
                notification_label.value = "Error de autenticación en Odoo."
                page.update()
                return

            # Llama al modelo de Odoo para obtener notificaciones
            models = xmlrpc.client.ServerProxy(f"{server_url}/xmlrpc/2/object")
            notificaciones = models.execute_kw(
                db_name, uid, password,
                'fcm.notification', 'search_read',
                [[('state', '=', 'new')]],  # Filtro: solo notificaciones nuevas
                {'fields': ['title', 'body'], 'limit': 5}
            )

            # Muestra las notificaciones obtenidas en la app
            if notificaciones:
                mensajes = "\n".join([f"{n['title']}: {n['body']}" for n in notificaciones])
                notification_label.value = f"Notificaciones recibidas:\n{mensajes}"
            else:
                notification_label.value = "No hay nuevas notificaciones."
            
            page.update()

        except Exception as ex:
            notification_label.value = f"Error al obtener notificaciones: {str(ex)}"
            page.update()

    # Botón inicial para obtener notificaciones
    get_notifications_button = ft.Button("Obtener notificaciones", on_click=obtener_notificaciones)

    # Mostrar la pantalla principal al inicio
    mostrar_pantalla_principal()

ft.app(target=main)
