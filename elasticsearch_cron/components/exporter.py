# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo.addons.component.core import Component


class ElasticsearchBaseExporter(Component):
    """ Base exporter for the Elasticsearch """

    _name = 'elasticsearch.base.exporter'
    _inherit = ['elasticsearch.basic.exporter']
    _apply_on = None

    def _lock(self, record):
        if self.env.context.get('no_elasticsearch_delay', False):
            return
        return super()._lock(record)

    def check_send(self, record, index, data, *args, **kwargs):
        return True
