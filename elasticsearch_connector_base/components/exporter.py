# Copyright 2017 Creu Blanca
# License LGPL-3.0 or later (https://www.gnu.org/licenses/lgpl.html).

import logging
import psycopg2
import json
from datetime import datetime

import odoo
from odoo.addons.component.core import Component
from odoo.addons.connector.exception import RetryableJobError

_logger = logging.getLogger(__name__)
try:
    import elasticsearch
except (ImportError, IOError) as err:
    _logger.debug(err)

ISO_FORMAT = '%Y-%m-%dT%H:%M:%S.%f'


class ElasticsearchBaseExporter(Component):
    """ Base exporter for the Elasticsearch """

    _name = 'elasticsearch.document.exporter'
    _inherit = ['base.exporter', 'base.elasticsearch.connector']
    _usage = 'record.exporter'
    _apply_on = ['elasticsearch.document']
    _exporter_failure_timeout = 2

    def _lock(self, document):
        """ Lock the binding record.
        Lock the binding record so we are sure that only one export
        job is running for this record if concurrent jobs have to export the
        same record.
        When concurrent jobs try to export the same record, the first one
        will lock and proceed, the others will fail to lock and will be
        retried later.
        This behavior works also when the export becomes multilevel
        with :meth:`_export_dependencies`. Each level will set its own lock
        on the binding record it has to export.
        """
        sql = ("SELECT id FROM %s WHERE ID = %%s FOR UPDATE NOWAIT" %
               self.model._table)
        try:
            self.env.cr.execute(sql, (document.id,),
                                log_exceptions=False)
        except psycopg2.OperationalError:
            _logger.info('A concurrent job is already exporting the same '
                         'record (%s with id %s). Job delayed later.',
                         self.model._name, document.id)
            raise RetryableJobError(
                'A concurrent job is already exporting the same record '
                '(%s with id %s). The job will be retried later.' %
                (self.model._name, document.id),
                seconds=self._exporter_failure_timeout)

    def es_create(self, document, *args, **kwargs):
        self._lock(document)
        index = document.index_id.index
        es = elasticsearch.Elasticsearch(
            hosts=document.index_id.get_hosts())
        data = json.dumps(kwargs['data'])
        es.index(index, '_doc', id=document.id, body=data)
        document.with_context(no_elasticserach_sync=True).write({
            'sync_date': kwargs['sync_date']
        })
        if not odoo.tools.config['test_enable']:
            self.env.cr.commit()  # pylint: disable=E8102
        self._after_export()
        return True

    def es_unlink(self, id, index, *args, **kwargs):
        """ Run the synchronization
        :param binding: binding record to export
        """
        es = elasticsearch.Elasticsearch(hosts=index.get_hosts())
        es.delete(index.index, '_doc', id)
        self._after_export()
        return True

    def es_write(self, document, *args, **kwargs):
        """ Run the synchronization
        :param binding: binding record to export
        """
        self._lock(document)
        sync_date = datetime.strptime(kwargs['sync_date'], ISO_FORMAT)
        if (
            not document.sync_date or
            sync_date >= datetime.strptime(document.sync_date, ISO_FORMAT)
        ):
            index = document.index_id.index
            es = elasticsearch.Elasticsearch(
                hosts=document.index_id.get_hosts())
            data = json.dumps(kwargs['data'])
            es.index(index, '_doc', id=document.id, body=data)
            document.with_context(no_elasticserach_sync=True).write({
                'sync_date': kwargs['sync_date']
            })
        else:
            _logger.info(
                'Record from %s with id %s has already been sended (%s), so it'
                ' is deprecated ' % (
                    self.model._name, document.id, kwargs['sync_date']
                )
            )
        # Commit so we keep the external ID when there are several
        # exports (due to dependencies) and one of them fails.
        # The commit will also release the lock acquired on the binding
        # record
        if not odoo.tools.config['test_enable']:
            self.env.cr.commit()  # pylint: disable=E8102
        self._after_export()
        return True

    def _after_export(self):
        """ Can do several actions after exporting a record"""
        pass
