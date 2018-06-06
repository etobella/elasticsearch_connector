# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo.addons.component.core import AbstractComponent


class BaseElasticsearchConnectorComponent(AbstractComponent):
    """ Base elasticsearch Connector Component
    All components of this connector should inherit from it.
    """

    _name = 'base.elasticsearch.connector'
    _inherit = 'base.connector'
    _collection = 'elasticsearch.backend'
