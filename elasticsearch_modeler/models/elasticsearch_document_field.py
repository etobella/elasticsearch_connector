# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, models, fields

INDEX_TYPE = {
    'binary': 'binary',
    'boolean': 'boolean',
    'char': 'keyword',
    'date': 'date',
    'datetime': 'date',
    'float': 'float',
    'html': 'text',
    'integer': 'integer',
    'job_serialized': 'binary',
    'many2many': 'object',
    'many2one': 'object',
    'monetary': 'double',
    'one2many': 'object',
    'reference': 'keyword',
    'selection': 'keyword',
    'serialized': 'binary',
    'text': 'text',
}


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

    @api.onchange('field_id')
    def _onchange_field(self):
        for record in self:
            record.child_ids = False

    @api.depends('index_id')
    def _compute_model(self):
        for record in self:
            if record.parent_id:
                record.model_id = self.env['ir.model'].search([
                    ('model', '=', record.parent_id.field_id.relation)
                ], limit=1)
            else:
                record.model_id = record.index_id.model_id

    def _get_index_values(self):
        #TODO: Check recursivity
        vals = {
            'type': INDEX_TYPE[self.field_type]
        }
        if self.child_ids:
            vals['properties'] = {
                field.field_id.name: field._get_index_values()
                for field in self.child_ids
            }
        return vals
