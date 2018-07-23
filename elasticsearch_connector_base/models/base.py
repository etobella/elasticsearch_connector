# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
import iso8601
from odoo import api, fields, models


class Base(models.AbstractModel):
    _inherit = 'base'
