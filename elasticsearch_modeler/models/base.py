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

    es_document_ids = fields.One2many(
        'elasticsearch.document',
        compute='_compute_elasticsearch_document',
        ondelete='cascade'
    )

    def _compute_elasticsearch_document(self):
        for rec in self:
            rec.es_document_ids = self.env['elasticsearch.document'].search([
                ('odoo_id', '=', rec.id),
                ('model', '=', self._name)
            ])

    @job(default_channel='root.elasticsearch')
    @api.multi
    def check_elasticsearch(self):
        self.ensure_one()
        indexes = self.env['elasticsearch.index'].search([
            ('state', '=', 'posted'),
            ('model', '=', self._name)
        ])
        for index in indexes:
            if self.search([('id', '=', self.id)] + safe_eval(index.domain)):
                self.env['elasticsearch.document'].create({
                    'index_id': index.id,
                    'model': self._name,
                    'odoo_id': self.id,
                })

    def read_elasticsearch(self, flds):
        self.ensure_one()
        x2many_fields = flds.filtered(
            lambda r: r.field_type in ['many2many', 'one2many'])
        many2one_fields = flds.filtered(
            lambda r: r.field_type == 'many2one')
        usual_fields = flds.filtered(
            lambda r: r.field_type not in ['many2many', 'one2many', 'many2one']
        )
        res = self.read(usual_fields.mapped('field_id').mapped('name'))[0]
        # Datetime fields must be converted to isoformat.
        for field in usual_fields.mapped('field_id').mapped('name'):
            if isinstance(
                self._fields.get(field), fields.Datetime
            ):
                if res[field]:
                    res[field] = to_datetime(res[field]).isoformat()
                else:
                    del res[field]
        for field in x2many_fields:
            vals = []
            child_fields = field.child_ids
            for rec in getattr(self, field.field_id.name):
                vals.append(rec.read_elasticsearch(child_fields))
            res[field.field_id.name] = vals
        for field in many2one_fields:
            value = getattr(self, field.field_id.name)
            if value:
                res[field.field_id.name] = value.read_elasticsearch(
                    field.child_ids)
        return res
