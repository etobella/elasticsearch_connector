# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.addons.component.core import Component


class ElasticsearchModelBinder(Component):
    _name = 'elasticsearch.binder'
    _inherit = ['base.binder', 'base.elasticsearch.connector']
    _apply_on = False
