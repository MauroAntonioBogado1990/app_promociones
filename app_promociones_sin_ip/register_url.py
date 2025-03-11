from odoo import http
from odoo.http import request

class RegisterClientServer(http.Controller):

    @http.route('/api/register_server', type='json', auth='public', methods=['POST'])
    def register_server(self, **kwargs):
        partner_id = kwargs.get('partner_id')
        server_url = kwargs.get('server_url')

        if partner_id and server_url:
            partner = request.env['res.partner'].sudo().browse(partner_id)
            if partner:
                partner.sudo().write({'app_server_url': server_url})
                return {'success': True, 'message': 'URL registrada correctamente.'}

        return {'success': False, 'message': 'Faltan parámetros o el cliente no existe.'}
