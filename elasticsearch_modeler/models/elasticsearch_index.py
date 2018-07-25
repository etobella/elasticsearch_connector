# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
import logging
from odoo import api, fields, models
from odoo.tools import safe_eval
import json

_logger = logging.getLogger(__name__)
try:
    import elasticsearch
except (ImportError, IOError) as err:
    _logger.debug(err)


class ElasticsearchIndex(models.Model):
    _inherit = 'elasticsearch.index'

    model_id = fields.Many2one(
        'ir.model',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    model = fields.Char(
        related='model_id.model',
        store=True, readonly=True,
    )
    type = fields.Selection(
        selection_add=[('modeler', 'Modeler')]
    )
    document_field_ids = fields.One2many(
        'elasticsearch.document.field',
        inverse_name='index_id',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    def _get_index_template(self):
        vals = super()._get_index_template()
        vals.update({
            "mappings": {'_doc': {'properties': {
                field.name: field._get_index_values()
                for field in
                self.document_field_ids.filtered(lambda r: not r.parent_id)
            }}}
        })
        return vals

    @api.multi
    def rebuild_documents(self):
        self.ensure_one()
        elements = self.env[self.model].search([]).ids
        documents = {r.odoo_id: r.id for r in self.document_ids}
        creates = []
        rebuilds = []
        # Delete unnecessary documents
        for element in elements:
            if element in documents:
                rebuilds.append(documents.pop(element))
            else:
                creates.append(element)
        logging.info("Deleting")
        for document in documents:
            self.env['elasticsearch.document'].browse(
                documents[document]).unlink()
        logging.info("Creating")
        for create in creates:
            self.env['elasticsearch.document'].create({
                'odoo_id': create,
                'index_id': self.id,
                'model': self.model,
            })
        logging.info("Updating")
        for rebuild in rebuilds:
            self.env['elasticsearch.document'].browse(rebuild).export_update()
        logging.info("Done")
