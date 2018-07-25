# Copyright 2018 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, fields, models


class ElasticsearchIndex(models.Model):
    _inherit = 'elasticsearch.index'

    is_cron = fields.Boolean(
        default=False,
        readonly=True,
        states={'draft': [('readonly', False)]},
    )
    cron_id = fields.Many2one(
        'ir.cron',
        readonly=True,
    )
    last_update = fields.Datetime(
        readonly=True
    )

    def _post_values(self):
        values = super()._post_values()
        values.update({'last_update': False})
        return values

    def _get_cron_values(self):
        return {
            'name': self.name,
            'model_id': self.env['ir.model'].search([
                ('model', '=', self._name)], limit=1).id,
            'state': 'code',
            'code': 'model.run_cron(%d)' % self.id,
            'interval_number': 1,
            'interval_type': 'hours',
        }

    def _get_cron_domain(self):
        res = []
        if self.last_update:
            res.append(('write_date', '>',self.last_update))
        return res

    @api.multi
    def update_cron(self):
        self.ensure_one()
        new_update = fields.Datetime.now()
        domain = self._get_cron_domain()
        domain.append(('write_date', '<=', new_update))
        elements = self.env[self.model].search(domain)
        elements.send_elasticsearch(self)
        self.write({'last_update': new_update})

    def run_cron(self, id):
        self.browse(id).update_cron()

    @api.multi
    def write(self, vals):
        res = super(ElasticsearchIndex, self).write(vals)
        if 'is_cron' in vals:
            for record in self:
                if record.is_cron:
                    if not record.cron_id:
                        record.cron_id = self.env['ir.cron'].create(
                            record._get_cron_values())
                    record.cron_id.write({'active': True})
                if record.cron_id:
                    record.cron_id.write({'active': False})
        return res

    @api.multi
    def rebuild_documents(self):
        self.ensure_one()
        if self.is_cron:
            self.update_cron()
            return
        return super().rebuild_documents()
