# Copyright 2018 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models, fields


class ElasticsearchHost(models.Model):
    _name = 'elasticsearch.host'
    _description = 'ElasticSearch Host'

    host = fields.Char(
        required=True
    )
    port = fields.Integer(
        required=True,
        default=9200,
    )
