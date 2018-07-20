# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields
from odoo.addons.component.core import Component


class BusBindingAccountMoveLine(models.Model):
    _name = 'elasticsearch.binding.account.move.line'
    _inherit = 'elasticsearch.binding'
    _description = 'Account Move line Bus Binding'

    odoo_id = fields.Many2one(
        comodel_name='account.move.line',
        required=True,
        ondelete='cascade'
    )


class AccountMoveLine(models.Model):
    _name = 'account.move.line'
    _inherit = ['account.move.line', 'elasticsearch.model']
    _binding_name = 'account_move_line'
    _elasticserach_include_fields = [
        'account_id', 'move_id', 'debit', 'credit', 'date', 'partner_id',
        'journal_id', 'date_maturity',
    ]

    elasticsearch_bind_ids = fields.One2many(
        'elasticsearch.binding.account.move.line',
    )


class AccountMoveLineBusListener(Component):
    _name = 'account.move.line.elasticsearch.listener'
    _inherit = 'abstract.elasticsearch.listener'
    _apply_on = ['account.move.line']


class BusBindingAccountMoveLineExporter(Component):
    _name = 'elasticsearch.binding.account.move.line.exporter'
    _inherit = 'elasticsearch.base.exporter'
    _apply_on = ['elasticsearch.binding.account.move.line']
