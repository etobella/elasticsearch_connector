# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.addons.component.core import Component


class BaseDocumentListener(Component):
    _inherit = 'elasticsearch.base.listener'

    def on_record_unlink(self, record):
        super().on_record_unlink(record)
        # TODO: Unlink records (if necessary?)
