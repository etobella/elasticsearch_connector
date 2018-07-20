# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import api, fields, models


class Base(models.AbstractModel):
    _inherit = 'base'
    _elasticserach_include_model = False

    @api.multi
    def get_elasticsearch_values(self):
        self.ensure_one()
        if not self._elasticserach_include_model:
            return self.id
        flds = list(set(
            self._elasticserach_include_fields +
            self.get_elasticsearch_fields()))
        vals = self.read(flds, load=False)[0]
        for field in flds:
            if not vals.get(field, False):
                del vals[field]
            if vals.get(field, False) and isinstance(
                    self._fields.get(field), fields.Many2one
            ) and getattr(self, field):
                vals[field] = getattr(self, field).get_elasticsearch_values()
        return vals
