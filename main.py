import argparse            
import sys                 
import logging
import ConfigParser
import traceback
from functools import wraps

from core.api import errors
from lib.dns import DnsApi

logger = logging.getLogger('aliyun-api')
SUBCOMMANDS = {}

def add_subcommand(subcommand):
    def decorator(func):
        SUBCOMMANDS[subcommand] = func

        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        return wrapper

    return decorator

def handle(config, args):
    func = SUBCOMMANDS.get(args.subcommand, None)
    if func is None:
    	print("Subcommand not implemented!")
        sys.exit(errors.error)
    try:
    	func(config, args)
    except Exception as e:
    	logger.error("Exception: %s\n%s\nAborting.", str(e),
                         traceback.format_exc())
        sys.exit(errors.error)

# Register all the handlers here

@add_subcommand('record')
def recordHandler(config, args):
    # domainActions = ['get', 'list', 'verify', 'delete', 'update', 'add']
    # recordActions = ['addRecord', 'deleteRecord', 'verifyRecord', 'updateRecord']
    api = DnsApi(config);
    f = api.functions.get(args.action, None)
    if f is None:
    	raise Exception('Invalid action for dns operation')
    else:
        f(args)
   
if __name__ == '__main__':     
    parser = argparse.ArgumentParser(prog='aliyun-api')

    # parser.add_argument('--config', '-c', action='store_true', default='./aliyun.conf')
  
    subparsers = parser.add_subparsers(title='subcommands', description='supported subcommands', dest='subcommand')
    
    # dns records operation  
    record_parser = subparsers.add_parser('record', help='operate on dns record')
    record_parser.add_argument('-a', '--action', help='operate sub domains:\nget/list/verify/add/remove/update\noperate records:\ndeleteRecord/updateRecord/addRecord/verifyRecord', required=True)
    record_parser.add_argument('-d', '--domain', help='select domain name', required=True)
    record_parser.add_argument('-s', '--host', help='select host name')
    record_parser.add_argument('-t', '--type', help='select record type')
    record_parser.add_argument('-v', '--value', help='value')
    record_parser.add_argument('-o', '--old', help='old value')

    args = parser.parse_args()
    # setup logger
    logger.setLevel(logging.INFO)
    logHandler = logging.StreamHandler()
    logHandler.setLevel(logging.INFO)
    formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
    logHandler.setFormatter(formatter)
    logger.addHandler(logHandler)

    # config
    config = ConfigParser.SafeConfigParser()
    config.read('aliyun.conf')
    handle(config, args)
    logger.info('exiting now..')
    sys.exit(errors.success)


