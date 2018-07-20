# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).
from odoo import api, SUPERUSER_ID
from datetime import datetime

models = ['account.move.line', 'account.invoice']


def post_init_hook(cr, registry):
    env = api.Environment(cr, SUPERUSER_ID, {})
    for model in models:
        for rec in env[model].search([('elasticsearch_bind_ids', '=', False)]):
            if not rec.elasticsearch_bind_ids:
                for backend in rec.get_backends():
                    for vals in rec.get_binds(backend):
                        env[rec.get_binding_model()].create(vals)
                env.cr.commit()
                for binding in rec.elasticsearch_bind_ids:
                    binding.with_delay().export_create(
                        datetime.now().isoformat())
