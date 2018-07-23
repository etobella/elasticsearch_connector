# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from datetime import datetime

from odoo import api, models, fields
from odoo.addons.queue_job.job import job


class ElasticsearchDocument(models.Model):
    _name = 'elasticsearch.document.field'
    _description = 'Elasticsearch Document Field'
    _parent_name = 'parent_id'

    index_id = fields.Many2one(
        'elasticsearch.index',
    )
    parent_id = fields.Many2one(
        'elasticsearch.document.field',
    )
    child_ids = fields.One2many(
        'elasticsearch.document.field',
        inverse_name='parent_id'
    )
    model_id = fields.Many2one(
        'ir.model',
        compute='_compute_model',
        store=True,
    )
    field_id = fields.Many2one(
        'ir.model.fields',
        domain="[('model_id', '=', model_id)]",
    )
    field_type = fields.Selection(
        related='field_id.ttype',
        store=True, readonly=True,
    )

    @api.depends('index_id')
    def _compute_model(self):
        for record in self:
            if record.parent_id:
                record.model_id = self.env['ir.model'].search([
                    ('model', '=', record.parent_id.field_id.relation)
                ], limit=1)
            else:
                record.model_id = record.index_id.model_id
