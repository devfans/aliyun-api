ALIYUN SDK
==================
Based on official aliyun python sdk.

# Commands Help
usage main.py subcommand

## Record Action Description

Including subdomain operations and record operations

```$ python main.py record -h
usage:  main.py record [-h] -a ACTION -d DOMAIN [-s HOST] [-t TYPE]
                            [-v VALUE] [-o OLD]

optional arguments:
  -h, --help            show this help message and exit
  -a ACTION, --action ACTION
                        operate sub domains: get/list/verify/add/remove/update
                        operate records:
                        deleteRecord/updateRecord/addRecord/verifyRecord
  -d DOMAIN, --domain DOMAIN
                        select domain name
  -s HOST, --host HOST  select host name
  -t TYPE, --type TYPE  select record type
  -v VALUE, --value VALUE
                        value
  -o OLD, --old OLD     old value

```

### SubDomain operations
####  add
Add subdomain. If subdomain records already exist, it will remove all existing records create a new record.

#### verify
Check if it's the only existing record for this subdomain. If true exit 0.

#### update
Update subdomain. If subdomain records already exist, will modify the record if it's the only one, otherwise it will remove all existing records then create a new record.

#### delete
Delete subdomain. Remove all existing records of the subdomain.

#### get
List all the records of the subdomain.

#### list
List all the records of the domain.

### Record operations
#### addRecord
Add one single record if it doesnt exist.

#### verifyRecord
Verify this record exists as valid.

#### updateRecord
Update the old record with new value if it exists, otherwise it will be created.

#### deleteRecord
Delete the record if it exists.

## Dependencies
```
pip install aliyun-python-sdk-core
```
