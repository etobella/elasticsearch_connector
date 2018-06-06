# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from datetime import datetime

from odoo import api, models, fields
from odoo.addons.queue_job.job import job


class ElasticsearchBinding(models.AbstractModel):
    _name = 'elasticsearch.binding'
    _inherit = 'external.binding'
    _description = 'Elasticsearch abstract Binding'
    _elasticsearch_fields = []

    odoo_id = fields.Many2one(
        required=True,
        comodel_name='elasticsearch.model',
    )
    index = fields.Char()
    doc_type = fields.Char()
    backend_id = fields.Many2one(
        comodel_name='elasticsearch.backend',
        string='CB Backend',
        required=True,
        ondelete='restrict',
    )
    elasticsearch_document_id = fields.Integer()
    sync_date = fields.Char()

    @job(default_channel='root.elasticsearch')
    @api.multi
    def export_create(self, date=datetime.now().isoformat()):
        self.ensure_one()
        with self.backend_id.work_on(self._name) as work:
            exporter = work.component(usage='record.exporter')
            return exporter.create(
                self,
                data=self.get_binding_values(),
                sync_date=date)

    @job(default_channel='root.elasticsearch')
    @api.multi
    def export_update(self, date=datetime.now().isoformat()):
        self.ensure_one()
        with self.backend_id.work_on(self._name) as work:
            exporter = work.component(usage='record.exporter')
            return exporter.update(
                self,
                data=self.get_binding_values(),
                sync_date=date)

    @job(default_channel='root.elasticsearch')
    @api.multi
    def export_delete(self, date=datetime.now().isoformat()):
        self.ensure_one()
        with self.backend_id.work_on(self._name) as work:
            exporter = work.component(usage='record.exporter')
            return exporter.delete(
                self,
                document_id=self.elasticsearch_document_id,
                sync_date=date
            )

    @api.model
    def get_fields(self):
        return ['id', 'write_date', 'write_uid', 'create_date', 'create_uid']

    def get_binding_values(self):
        flds = list(set(self._elasticsearch_fields + self.get_fields()))
        return self.odoo_id.read(flds, load=False)[0]
