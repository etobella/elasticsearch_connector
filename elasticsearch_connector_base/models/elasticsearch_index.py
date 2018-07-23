# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
import logging
from odoo import api, fields, models
from odoo.tools import safe_eval

_logger = logging.getLogger(__name__)
try:
    import elasticsearch
except (ImportError, IOError) as err:
    _logger.debug(err)


class ElasticsearchIndex(models.Model):
    _name = 'elasticsearch.index'
    _description = 'Elasticsearch Index'
    _inherit = 'connector.backend'

    name = fields.Char(

        required=True, readonly=True, states={'draft': [('readonly', False)]},
    )
    state = fields.Selection([
        ('draft', 'Draft'),
        ('posted', 'Posted'),
        ('cancelled', 'Cancelled')
    ], required=True, default='draft', readonly=True)
    index = fields.Char(
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    host_ids = fields.Many2many(
        'elasticsearch.host',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    model_id = fields.Many2one(
        'ir.model',
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    model = fields.Char(
        related='model_id.model',
        store=True, readonly=True,
    )
    domain = fields.Char(
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
        default='[]'
    )
    document_ids = fields.One2many(
        'elasticsearch.document',
        inverse_name='index_id',
        readonly=True
    )
    document_field_ids = fields.One2many(
        'elasticsearch.document.field',
        inverse_name='index_id',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    def _post_values(self):
        return {'state': 'posted'}

    def _post(self):
        es = elasticsearch.Elasticsearch(hosts=self.get_hosts())
        es.indices.create(
            self.index,
            body={"settings": {"index.mapping.ignore_malformed": True}})

    @api.multi
    def post(self):
        self.ensure_one()
        self._post()
        self.write(self._post_values())

    def _reset_index(self):
        self.ensure_one()
        es = elasticsearch.Elasticsearch(hosts=self.get_hosts())
        self.document_ids.with_context(no_elasticserach_sync=True).unlink()
        es.indices.delete(index=self.index, ignore=[400, 404])
        self.state = 'cancelled'

    def _draft_values(self):
        return {'state': 'draft'}

    @api.multi
    def restore(self):
        self.write(self._draft_values())

    def _cancel_values(self):
        return {'state': 'cancelled'}

    @api.multi
    def cancel(self):
        self.ensure_one()
        self._reset_index()
        self.write(self._cancel_values())

    @api.multi
    def rebuild_documents(self):
        self.ensure_one()
        domain = safe_eval(self.domain)
        elements = self.env[self.model].search(domain).ids
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

    def get_hosts(self):
        return [{"host": r.host, "port": r.port} for r in self.host_ids]
