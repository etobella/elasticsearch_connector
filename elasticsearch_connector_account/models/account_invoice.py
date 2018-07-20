# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields
from odoo.addons.component.core import Component


class BusBindingAccountInvoice(models.Model):
    _name = 'elasticsearch.binding.account.invoice'
    _inherit = 'elasticsearch.binding'
    _description = 'Account Move line Bus Binding'

    odoo_id = fields.Many2one(
        comodel_name='account.invoice',
        required=True,
        ondelete='cascade'
    )


class AccountInvoice(models.Model):
    _name = 'account.invoice'
    _inherit = ['account.invoice', 'elasticsearch.model']
    _binding_name = 'account_invoice'
    _elasticserach_include_fields = [
        'partner_id', 'company_id', 'invoice_line_ids', 'date', 'type',
        'user_id', 'date_invoice', 'date_due',
    ]

    elasticsearch_bind_ids = fields.One2many(
        'elasticsearch.binding.account.invoice',
    )


class AccountInvoiceLine(models.Model):
    _name = 'account.invoice.line'
    _inherit = ['account.invoice.line', 'elasticsearch.include.model']

    _elasticserach_include_fields = [
        'product_id', 'quantity', 'discount', 'price_unit', 'price_subtotal',
    ]


class AccountInvoiceBusListener(Component):
    _name = 'account.invoice.elasticsearch.listener'
    _inherit = 'abstract.elasticsearch.listener'
    _apply_on = ['account.invoice']


class BusBindingAccountInvoiceExporter(Component):
    _name = 'elasticsearch.binding.account.invoice.exporter'
    _inherit = 'elasticsearch.base.exporter'
    _apply_on = ['elasticsearch.binding.account.invoice']
