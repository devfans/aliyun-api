import logging
from aliyunsdkcore.client import AcsClient

logger = logging.getLogger(__name__)
# script exit code
class Status(object):
    def __init__(self):
        self.success = 0
        self.failure = 1
        self.unauthorized = 2
        self.error = 3

errors = Status()

class Api(object):
    def __init__(self, config):
        self.apiUser = config.get('aliyun', 'apiUser', None)
        self.apiKey = config.get('aliyun', 'apiKey', None)
        self.region = config.get('aliyun', 'region', None)
        if (self.apiUser or self.apiKey or self.region) is None:
            logger.warning('aliyun credential is invalid')

        self.client = AcsClient(self.apiUser, self.apiKey, self.region)

    def do(self, request):
        res = self.client.do_action_with_exception(request)
        return res

    def equalAll(self, *kvs):
        for k, v in kvs:
            if k != v:
                return False
        else:
            return True

    def attrsNotNone(self, obj, *attrs):
        for attr in attrs:
            if getattr(obj, attr, None) is None:
                logger.error(attr + ' is none')
                return False
        else:
            return True

