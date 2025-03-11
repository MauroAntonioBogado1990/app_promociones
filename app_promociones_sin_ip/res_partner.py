from odoo import models, fields
"""
Este campo será necesario dado que vamos a tener que guardar la ip del cliente para poder realizar el envío

"""
class ResPartner(models.Model):
    _inherit = "res.partner"

    app_server_url = fields.Char("URL del servidor cliente", help="URL del servidor XML-RPC de la app cliente")
