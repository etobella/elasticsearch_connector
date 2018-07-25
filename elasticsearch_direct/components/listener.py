# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.addons.component.core import Component
from datetime import datetime


class BaseDocumentListener(Component):
    _inherit = 'elasticsearch.base.listener'

    def on_record_create(self, record, fields):
        super().on_record_create(record, fields)
        if self.env.context.get('no_elasticserach_sync', False):
            return
        if getattr(record, 'es_index_ids', False):
            rec = record.with_context(no_elasticsearch_delay=True)
            if not self.env.context.get('no_elasticsearch_delay', False):
                rec = rec.with_delay()
            rec.send_elasticsearch()

    def on_record_write(self, record, fields):
        super().on_record_write(record, fields)
        if self.env.context.get('no_elasticserach_sync', False):
            return
        if getattr(record, 'es_index_ids', False):
            rec = record.with_context(no_elasticsearch_delay=True)
            if not self.env.context.get('no_elasticsearch_delay', False):
                rec = rec.with_delay()
            rec.send_elasticsearch()

    def on_record_unlink(self, record):
        super().on_record_unlink(record)
        if self.env.context.get('no_elasticserach_sync', False):
            return
        if getattr(record, 'es_index_ids', False):
            rec = record.with_context(no_elasticsearch_delay=True)
            if not self.env.context.get('no_elasticsearch_delay', False):
                rec = rec.with_delay()
            rec.unlink_elasticsearch(rec.id)
