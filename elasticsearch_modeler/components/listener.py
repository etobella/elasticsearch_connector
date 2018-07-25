# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.addons.component.core import Component
from datetime import datetime


class BaseDocumentListener(Component):
    _name = 'elasticsearch.base.listener'
    _inherit = 'base.event.listener'

    def on_record_create(self, record, fields):
        if self.env['elasticsearch.index'].search(record.index_domain()):
            record.with_delay().check_elasticsearch()

    def on_record_write(self, record, fields):
        if getattr(record, 'es_document_ids', False):
            for doc in record.es_document_ids:
                doc.with_delay().export_update(datetime.now().isoformat())
