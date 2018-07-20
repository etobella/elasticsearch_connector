# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ElasticsearchModel(models.AbstractModel):
    _name = 'elasticsearch.model'
    _inherit = 'elasticsearch.include.model'
    _binding_name = False

    elasticsearch_bind_ids = fields.One2many(
        comodel_name='elasticsearch.binding',
        inverse_name='odoo_id',
        string='Elasticsearch Bindings'
    )

    @api.model
    def get_backends(self):
        return self.env['elasticsearch.backend'].search([])

    @api.model
    def get_binding_model(self):
        return 'elasticsearch.binding.' + self._name

    def bind_values(self, backend, elasticsearch_model):
        return {
            'odoo_id': self.id,
            'backend_id': backend.id,
            'index': elasticsearch_model
        }

    @api.multi
    def get_binds(self, backend):
        """
        :return: list of the bind values
        """
        self.ensure_one()
        return [self.bind_values(backend, self._binding_name or self._name)]
