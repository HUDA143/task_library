# -*- coding: utf-8 -*-

from odoo import models, fields, api
from odoo.exceptions import UserError


class library_management(models.Model):
    _name = 'library_management.library_management'
    _description = 'library_management.library_management'

    name = fields.Char(string="Title",required=True)
    author = fields.Char(string="Author",required=True)
    publication_date = fields.Date(string="Publication Date")

class SaleOrder(models.Model):
    _inherit = 'sale.order'

    customer_reference = fields.Char(string='Customer Reference')

    @api.model
    def send_order_confirmation_email(self, sale_order_ids):
        for order in self.browse(sale_order_ids):
            if order.state != 'sale':
                raise UserError("Cannot send confirmation email for unconfirmed order.")

            template = self.env.ref('sale.email_template_edi_sale', raise_if_not_found=False)
            if not template:
                raise UserError("Email template not found. Please check the configuration.")

            # Prepare the email values
            email_values = {
                'email_to': order.partner_id.email,
                'email_from': self.env.company.email,
                'subject': f"Order Confirmation: {order.name}",
            }

            # Send the email
            template.send_mail(order.id, force_send=True, email_values=email_values)

        return True