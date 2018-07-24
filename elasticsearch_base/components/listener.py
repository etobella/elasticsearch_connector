# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.addons.component.core import Component
from datetime import datetime


class ElasticsearchDocumentListener(Component):
    _name = 'elasticsearch.document.listener'
    _inherit = 'base.event.listener'
    _apply_on = 'elasticsearch.document'

    def on_record_create(self, record, fields):
        if self.env.context.get('no_elasticserach_sync', False):
            return
        for rec in record:
            rec.with_delay().export_create(datetime.now().isoformat())

    def on_record_write(self, record, fields):
        if self.env.context.get('no_elasticserach_sync', False):
            return
        for rec in record:
            rec.with_delay().export_update(datetime.now().isoformat())

    def on_record_unlink(self, record):
        if self.env.context.get('no_elasticserach_sync', False):
            return
        if self.env.context.get('no_elasticsearch_delay', False):
            for rec in record:
                rec.export_delete(rec.id, rec.index_id)
        for rec in record:
            rec.with_delay()
