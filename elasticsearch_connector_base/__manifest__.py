# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Elasticsearch Connector Base',
    'version': '11.0.1.0.1',
    'category': 'Elasticsearch connector',
    'depends': [
        'connector',
    ],
    'author': 'Creu Blanca',
    'license': 'AGPL-3',
    'summary': 'Elasticsearch connector base',
    'data': [
        'data/backend.xml',
        'security/ir.model.access.csv',
    ],
    'external_dependencies': {
        'python': [
            'elasticsearch'
        ],
    },
    'installable': True,
}
