# magento-economics-sync
Sync Products and Orders to e-conomic from magento 1.9.* using APIs. Emits logging into subfolder called /log as configured in logging.conf


## Configuration
In order for the synchronization scripts to work, various configuration variables need to be set in a file named secrets.py. Add the file to the root of the project folder and use below template:

```magento_api_xmlrpc_url = ""         # url for magento api. E.g. "https://host/index.php/api/xmlrpc?type=xmlrpc"
magento_api_user = ""               # xmlrpc api user
magento_api_pass = ""               # xmlrpc api user password

# secrets obtained from economics administrative user interface
economics_headers = {'X-AppSecretToken': '',
                     'X-AgreementGrantToken': '',
                     'Content-Type': 'application/json'}```

