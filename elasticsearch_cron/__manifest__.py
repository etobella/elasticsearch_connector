# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

{
    'name': 'Elasticsearch cron',
    'version': '11.0.1.0.1',
    'category': 'Elasticsearch connector',
    'depends': [
        'elasticsearch_modeler',
    ],
    'author': 'Creu Blanca',
    'license': 'AGPL-3',
    'summary': 'Elasticsearch cron',
    'data': [
        'views/elasticsearch_index_views.xml',
    ],
    'installable': True,
}
