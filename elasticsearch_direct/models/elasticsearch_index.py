# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class ElasticsearchIndex(models.Model):
    _inherit = 'elasticsearch.index'

    direct = fields.Boolean(
        default=False,
        readonly=True,
        states={'draft': [('readonly', False)]},
    )

    @api.multi
    def rebuild_documents(self):
        self.ensure_one()
        if self.direct:
            elements = self.env[self.model].search([])
            for element in elements:
                element.send_elasticsearch()
            return
        return super().rebuild_documents()
