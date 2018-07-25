# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import logging

from odoo.addons.component.core import Component

_logger = logging.getLogger(__name__)
try:
    import elasticsearch
except (ImportError, IOError) as err:
    _logger.debug(err)

ISO_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


class ElasticsearchBaseExporter(Component):
    """ Base exporter for the Elasticsearch """

    _name = 'elasticsearch.base.exporter'
    _inherit = ['elasticsearch.basic.exporter']
    _apply_on = None

    def _lock(self, record):
        if self.env.context.get('no_elasticsearch_delay', False):
            return
        return super(ElasticsearchBaseExporter, self)._lock(record)

    def check_send(self, record, index, data, *args, **kwargs):
        return True
