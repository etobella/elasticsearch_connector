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
        'security/ir.model.access.csv',
        'views/menu.xml',
        'views/elasticsearch_host_views.xml',
        'views/elasticsearch_index_views.xml',
        'views/elasticsearch_document_views.xml',
        'views/elasticsearch_document_field_views.xml',
    ],
    'external_dependencies': {
        'python': [
            'elasticsearch'
        ],
    },
    'installable': True,
}
