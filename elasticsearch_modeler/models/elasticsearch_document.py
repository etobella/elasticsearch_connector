# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, models, fields


class ElasticsearchDocument(models.Model):
    _inherit = 'elasticsearch.document'

    odoo_id = fields.Integer(
    )
    model = fields.Char(
    )

    def get_document_values(self):
        if self.index_id.type == 'modeler':
            return self.env[self.model].browse(self.odoo_id).read_elasticsearch(
                self.index_id.document_field_ids.filtered(
                    lambda r: not r.parent_id)
            )
