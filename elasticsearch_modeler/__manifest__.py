# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Elasticsearch modeler',
    'version': '11.0.1.0.1',
    'category': 'Elasticsearch connector',
    'depends': [
        'elasticsearch_base',
    ],
    'author': 'Creu Blanca',
    'license': 'AGPL-3',
    'summary': 'Elasticsearch connector base',
    'data': [
        'security/ir.model.access.csv',
        'views/elasticsearch_index_views.xml',
        'views/elasticsearch_document_field_views.xml',
    ],
    'installable': True,
}
