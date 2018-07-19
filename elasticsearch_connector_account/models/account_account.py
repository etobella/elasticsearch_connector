# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

from odoo import models


class AccountJournal(models.Model):
    _name = 'account.account'
    _inherit = ['account.account', 'elasticsearch.include.model']
    _binding_name = 'account_account'
    _elasticserach_include_fields = [
        'code', 'name'
    ]
