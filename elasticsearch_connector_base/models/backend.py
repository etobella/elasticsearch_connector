# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import fields, models


class ElasticsearchBackend(models.Model):
    _name = 'elasticsearch.backend'
    _description = 'Elasticsearch Backend'
    _inherit = 'connector.backend'

    name = fields.Char(
        readonly=True
    )
    destination = fields.Char(
        string='Destination',
    )
    port = fields.Integer()

    def get_hosts(self):
        return [{"host": self.destination, "port": self.port}]
