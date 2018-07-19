# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class ElasticsearchIncludeModel(models.AbstractModel):
    _name = 'elasticsearch.include.model'
    _elasticserach_include_model = True
    _elasticserach_include_fields = []

    @api.model
    def get_elasticsearch_fields(self):
        return ['id', 'write_date', 'write_uid', 'create_date', 'create_uid']
