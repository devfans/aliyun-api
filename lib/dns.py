import sys
import json
from copy import copy
from aliyunsdkcore.request import RpcRequest
from core.api import Api, errors
import logging

logger = logging.getLogger(__name__)

class DnsApi(Api):
    
    def __init__(self, config):
        Api.__init__(self, config)
        self.functions = {
                   'add':  self.addSubDomain,
                'delete':  self.deleteSubDomain,
                   'get':  self.getSubDomain,
                  'list':  self.listSubDomain,
                'verify':  self.verifySubDomain,
                'update':  self.updateSubDomain,
             'addRecord':  self.addRecord,
          'deleteRecord':  self.deleteRecord,
          'updateRecord':  self.updateRecord,
          'verifyRecord':  self.verifyRecord
                }

    def listSubDomain(self, args):
        logger.info(self._listSubDomain(args))

    def _listSubDomain(self, args):
        logger.info('listing domain records')
        if not self.attrsNotNone(args, 'domain'):
            raise Exception('Invalid request')
        req = RpcRequest('Alidns', '2015-01-09', 'DescribeDomainRecords')
        req.add_query_param('DomainName', args.domain)
        # req.add_query_param('Type', getattr(args, 'type') or 'A')

        res = self.do(req)
        return res

    def getSubDomain(self, args):
        logger.info(self._getSubDomain(args))

    def _getSubDomain(self, args):
        logger.info('fetching subdomain')
        if not self.attrsNotNone(args, 'host', 'domain'):
            raise Exception('Invalid request')
        req = RpcRequest('Alidns', '2015-01-09', 'DescribeSubDomainRecords')
        req.add_query_param('SubDomain', '.'.join([args.host, args.domain]))
        # req.add_query_param('Type', getattr(args, 'type') or 'A')
        res = self.do(req)
        return res
   
    def verifySubDomain(self, args):
        valid, recordId = self._verifySubDomain(args)
        if valid:
            logger.info('verified: correct')
            sys.exit(errors.success)
        else:
            logger.info('verified: incorrect')
            sys.exit(errors.failure)

    def _verifySubDomain(self, args):
        logger.info('verifying subdomain resolution')
        res = json.loads(self._getSubDomain(args))
        count = res['TotalCount']
        record = res['DomainRecords']['Record'][0]
        status = record['Status']
        RR = record['RR']
        value = record['Value']
        domain = record['DomainName']
        if self.equalAll((count, 1), (status, 'ENABLE'), (value, args.value)):
            return True, record['RecordId']
        else:
            return False, None

    def verifyRecord(self, args):
        valid, recordId = self._verifyRecord(args)
        if valid:
            logger.info('verified: correct')
            sys.exit(errors.success)
        else:
            logger.info('verified: incorrect')
            sys.exit(errors.failure)

    def _verifyRecord(self, args):
        logger.info('verifying record')
        data = self._getSubDomain(args)
        res = json.loads(data)
        records = res['DomainRecords']['Record']
        for record in records:
            status = record['Status']
            value = record['Value']
            if self.equalAll((status, 'ENABLE'), (value, args.value)):
                return True, record['RecordId']
        else:
            logger.info(data)
            return False, None

    def deleteSubDomain(self, args):
        logger.info(self._deleteSubDomain(args))

    def _deleteSubDomain(self, args):
        logger.info('deleting subdomain')
        if not self.attrsNotNone(args, 'host', 'domain'):
            raise Exception('Invalid request')
        req = RpcRequest('Alidns', '2015-01-09', 'DeleteSubDomainRecords')
        req.add_query_param('DomainName', args.domain)
        req.add_query_param('RR', args.host)
        # req.add_query_param('Type', getattr(args, 'type') or 'A')

        res = self.do(req)
        return res

    def addSubDomain(self, args):
        self._deleteSubDomain(args)
        self._addRecord(args)

    def addRecord(self, args):
        logger.info(self._addRecord(args))

    def _addRecord(self, args):
        logger.info('adding record')
        if not self.attrsNotNone(args, 'host', 'domain', 'value'):
            raise Exception('Invalid request')
        req = RpcRequest('Alidns', '2015-01-09', 'AddDomainRecord')
        req.add_query_param('DomainName', args.domain)
        req.add_query_param('RR', args.host)
        req.add_query_param('Value', args.value)
        req.add_query_param('Type', getattr(args, 'type') or 'A')

        res = self.do(req)
        return res

    def updateSubDomain(self, args):
        res = json.loads(self._getSubDomain(args))
        count = res['TotalCount']
        if count == 1:
            record = res['DomainRecords']['Record'][0]
            if args.value == record['Value']:
                logger.info('Record already exists as the only one for this subdomain.')
                return
            args.id = record['RecordId']
            self._updateRecord(args)
        else:
            logger.warning("there is no or more than one records found for this domain, recreating now")
            self._deleteSubDomain(args)
            self._addRecord(args)

    def updateRecord(self, args):
        if not self.attrsNotNone(args, 'host', 'old', 'domain', 'value'):
            raise Exception('Invalid request')

        argsCopy = copy(args)
        argsCopy.value = args.old
    
        valid, recordId = self._verifyRecord(argsCopy)
        if valid:
            args.id = recordId
            self._updateRecord(args)
        else:
            logger.warning("old record does not exist, will still add new record")
            self._addRecord(args)

    def _updateRecord(self, args):
        logger.info('updating record')
        if not self.attrsNotNone(args, 'host', 'id', 'domain', 'value'):
            raise Exception('Invalid request')
        req = RpcRequest('Alidns', '2015-01-09', 'UpdateDomainRecord')
        req.add_query_param('DomainName', args.domain)
        req.add_query_param('RR', args.host)
        req.add_query_param('RecordId', args.id)
        req.add_query_param('Value', args.value)
        req.add_query_param('Type', getattr(args, 'type') or 'A')

        res = self.do(req)
        return res

    def deleteRecord(self, args):
        if not self.attrsNotNone(args, 'host', 'domain', 'value'):
            raise Exception('Invalid request')

        valid, recordId = self._verifyRecord(args)
        if valid:
            args.id = recordId
            self._deleteRecord(args)
        else:
            logger.warning("this record does not exist")

    def _deleteRecord(self, args):
        logger.info('deleting record')
        if not self.attrsNotNone(args, 'id'):
            raise Exception('Invalid request')
        req = RpcRequest('Alidns', '2015-01-09', 'DeleteDomainRecord')
        req.add_query_param('RecordId', args.id)

        res = self.do(req)
        return res

    
