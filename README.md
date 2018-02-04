# magento-economics-sync
Sync Products and Orders to e-conomic from magento 1.9.* using APIs of each system. 


## Configuration
In order for the synchronization scripts to work, various configuration variables need to be set in a file named `secrets.py`. Add the file to the root of the project folder and use below template:

```python
magento_api_xmlrpc_url = ""         # url for magento api. E.g. "https://host/index.php/api/xmlrpc?type=xmlrpc"
magento_api_user = ""               # xmlrpc api user
magento_api_pass = ""               # xmlrpc api user password

# secrets obtained from economics administrative user interface
economics_headers = {'X-AppSecretToken': '',
                     'X-AgreementGrantToken': '',
                     'Content-Type': 'application/json'}
```
                     
The script Synchronizes changes done last day by default (this can be changed in sync.py with the delta_load_days parameter). If the job is scheduled to more than once per day (e.g. every 30 minutes), this is sufficient. Later, this may be updated to handle delta load more elegantly by maintaining state of already synchronized entities. Example crontab schedule that synchronizes data every 30 minutes:

```bash
/30 * * * * /var/python/magento-sync/bin/python /var/python/magento-sync/sync.py
```

Emits logging into subfolder called `/log`, this has to be created - or path can be changed in `logging.conf`.
