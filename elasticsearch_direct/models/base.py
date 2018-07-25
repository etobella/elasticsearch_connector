# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from datetime import datetime, date
from odoo import api, fields, models
from odoo.addons.queue_job.job import job
from odoo.tools import safe_eval
from odoo.tools import DEFAULT_SERVER_DATE_FORMAT as DATE_FORMAT
from odoo.tools import DEFAULT_SERVER_DATETIME_FORMAT as DATETIME_FORMAT

DATE_LENGTH = len(date.today().strftime(DATE_FORMAT))
DATETIME_LENGTH = len(datetime.now().strftime(DATETIME_FORMAT))


def to_datetime(value):
    """ Convert an ORM ``value`` into a :class:`datetime` value. """
    if not value:
        return None
    value = value[:DATETIME_LENGTH]
    if len(value) == DATE_LENGTH:
        value += " 00:00:00"
    return datetime.strptime(value + '+0000', DATETIME_FORMAT + '%z')


class Base(models.AbstractModel):
    _inherit = 'base'

    es_index_ids = fields.Many2many(
        'elasticsearch.index',
        compute='_compute_index',
    )

    @api.model
    def index_domain(self):
        res = super().index_domain()
        res.append(('direct', '=', False))
        return res

    @api.model
    def _direct_index_domain(self):
        return [
            ('state', '=', 'posted'),
            ('model', '=', self._name),
            ('direct', '=', True)
        ]

    def _compute_index(self):
        indexes = self.env['elasticsearch.index'].search(
            self._direct_index_domain())
        for record in self:
            record.es_index_ids = indexes

    def get_es_values(self, index):
        return self.read_elasticsearch(index.document_field_ids.filtered(
            lambda r: not r.parent_id))

    @job(default_channel='root.elasticsearch')
    @api.multi
    def send_elasticsearch(self):
        self.ensure_one()
        for index in self.es_index_ids:
            with index.work_on(self._name) as work:
                exporter = work.component(usage='record.exporter')
                return exporter.es_write(
                    self, index, self.get_es_values(index))

    @job(default_channel='root.elasticsearch')
    @api.model
    def unlink_elasticsearch(self, id):
        indexes = self.env['elasticsearch.index'].search(
            self._direct_index_domain())
        for index in indexes:
            with index.work_on(self._name) as work:
                exporter = work.component(usage='record.exporter')
                return exporter.es_unlink(id, index)
