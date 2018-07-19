# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Elasticsearch Connector Account',
    'version': '11.0.1.0.1',
    'category': 'Elasticsearch connector',
    'depends': [
        'elasticsearch_connector_base',
    ],
    'author': 'Creu Blanca',
    'license': 'AGPL-3',
    'summary': 'Elasticsearch connector base',
    'data': [
    ],
    'post_init_hook': 'post_init_hook',
    'installable': True,
}
