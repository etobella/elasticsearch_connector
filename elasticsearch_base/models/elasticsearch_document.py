# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from datetime import datetime

from odoo import api, models, fields
from odoo.addons.queue_job.job import job


class ElasticsearchDocument(models.Model):
    _name = 'elasticsearch.document'
    _inherit = 'external.binding'
    _description = 'Elasticsearch abstract Document'

    index_id = fields.Many2one(
        comodel_name='elasticsearch.index',
        string='Index',
        required=True,
        ondelete='restrict',
    )
    sync_date = fields.Char()

    @job(default_channel='root.elasticsearch')
    @api.multi
    def export_create(self, date=datetime.now().isoformat()):
        self.ensure_one()
        with self.index_id.work_on(self._name) as work:
            exporter = work.component(usage='record.exporter')
            return exporter.es_write(
                self,
                self.get_document_values(),
                sync_date=date)

    @job(default_channel='root.elasticsearch')
    @api.multi
    def export_update(self, date=datetime.now().isoformat()):
        self.ensure_one()
        with self.index_id.work_on(self._name) as work:
            exporter = work.component(usage='record.exporter')
            return exporter.es_write(
                self,
                self.get_document_values(),
                sync_date=date)

    @job(default_channel='root.elasticsearch')
    @api.multi
    def export_delete(self, id, index):
        with index.work_on(self._name) as work:
            exporter = work.component(usage='record.exporter')
            return exporter.es_unlink(id, index)

    def get_document_values(self):
        return {}
