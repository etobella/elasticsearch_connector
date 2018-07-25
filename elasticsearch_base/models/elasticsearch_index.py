# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
import logging
from odoo import api, fields, models, _
from odoo.exceptions import ValidationError
from odoo.tools import safe_eval
import json

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
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
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
    document_ids = fields.One2many(
        'elasticsearch.document',
        inverse_name='index_id',
        readonly=True
    )
    type = fields.Selection(
        [],
        required=True,
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    template_settings = fields.Text(
        default='{}',
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    def _post_values(self):
        return {'state': 'posted'}

    @api.constrains('template_settings')
    def _check_template_settings(self):
        settings = safe_eval(self.template_settings or '{}')
        if not isinstance(settings, dict):
            raise ValidationError(_('Template settings must be a dictionary'))

    def _get_index_template(self):
        settings = {
            "settings": {"index.mapping.ignore_malformed": True}
        }
        settings["settings"].update(safe_eval(self.template_settings or "{}"))
        return settings

    def _post(self):
        es = elasticsearch.Elasticsearch(hosts=self.get_hosts())
        es.indices.create(
            self.index,
            body=json.dumps(self._get_index_template()))

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

    def get_hosts(self):
        return [{"host": r.host, "port": r.port} for r in self.host_ids]
