# Copyright 2018 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, models
from odoo.addons.queue_job.job import job


class Base(models.AbstractModel):
    _inherit = 'base'

    @api.model
    def index_domain(self):
        res = super().index_domain()
        res.append(('is_cron', '=', False))
        return res

    @job(default_channel='root.elasticsearch')
    @api.multi
    def send_elasticsearch(self, index):
        with index.work_on(self._name) as work:
            exporter = work.component(usage='record.exporter')
            for record in self:
                exporter.es_direct_write(
                    record.id, index, record.get_es_values(index))

    def get_es_values(self, index):
        return self.read_elasticsearch(
            index.document_field_ids.filtered(
                lambda r: not r.parent_id))
