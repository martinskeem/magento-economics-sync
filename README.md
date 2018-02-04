# magento-economics-sync
Sync Products and Orders to e-conomic from magento 1.9.* using APIs of each system. The solution is created to one specific use case and may set certain attributes to constants - it would likely have to be adapted to work correctly for other shops.


## Configuration - secrets.py
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


## Configuration - crontab
The script Synchronizes changes done last day by default (this can be changed in `sync.py` with the `delta_load_days parameter`). If the job is scheduled to more than once per day (e.g. every 30 minutes), this is sufficient. Later, this may be updated to handle delta load more elegantly by maintaining state of already synchronized entities. Example crontab schedule that synchronizes data every 30 minutes:

```bash
/30 * * * * /var/python/magento-sync/bin/python /var/python/magento-sync/sync.py
```


## Configuration - logging
Emits logging into subfolder called `/log`, this has to be created - or path can be changed in `logging.conf`.


## Configuration - e-conomic constants
Some API end points (which are unlikely to require changing) and some default values use for VAT Zone, Customer Groups, Payment Terms etc. These are hardcoded constants - and may have to be configured differently for other shops.


```phython
roducts_url = 'https://restapi.e-conomic.com/products'
product_url = 'https://restapi.e-conomic.com/products/{0}'
customers_url = 'https://restapi.e-conomic.com/customers'
customer_url = 'https://restapi.e-conomic.com/customers/{0}'
invoice_url = 'https://restapi.e-conomic.com/invoices/drafts/{0}'
invoices_url = 'https://restapi.e-conomic.com/invoices/drafts'

customer_vatzone = 1
customer_group = 3
customer_paymentterms = 5
invoice_layout = 18
invoice_shipping_product_id = 'Fragt'
invoice_vat_reverse_rate = .8
product_group = 6000
```
