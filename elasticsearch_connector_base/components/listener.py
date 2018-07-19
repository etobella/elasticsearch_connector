# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.addons.component.core import AbstractComponent
from datetime import datetime


class AbstractElasticsearchListener(AbstractComponent):
    _name = 'abstract.elasticsearch.listener'
    _inherit = 'base.event.listener'
    _apply_on = False

    def on_record_create(self, record, fields):
        for rec in record:
            for backend in rec.get_backends():
                for vals in rec.get_binds(backend):
                    import logging
                    logging.info(vals)
                    binding = self.env[rec.get_binding_model()].create(vals)
                    binding.with_delay().export_create(
                        datetime.now().isoformat())

    def on_record_write(self, record, fields):
        for rec in record:
            if rec._fields.get('elasticsearch_bind_ids'):
                for binding in rec.elasticsearch_bind_ids:
                    binding.with_delay().export_update(
                        datetime.now().isoformat())

    def on_record_unlink(self, record):
        for rec in record:
            for binding in rec.elasticsearch_bind_ids:
                binding.with_delay().export_delete(
                    datetime.now().isoformat())
