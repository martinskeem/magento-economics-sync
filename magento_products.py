import secrets
import xmlrpc.client
import logging
from datetime import datetime, timedelta


def products_list(updated_at_days_ago):
    start_date_delta_load = (datetime.today() - timedelta(days=updated_at_days_ago)).strftime("%Y-%m-%d 00:00:00")

    client = xmlrpc.client.ServerProxy(secrets.magento_api_xmlrpc_url)
    session = client.login(secrets.magento_api_user, secrets.magento_api_pass)

    response = client.call(session, 'catalog_product.list', [{'updated_at': {'from': start_date_delta_load}}])

    logging.debug("retrieved {0} products".format(len(response)))
    
    return response


def product_info(product_id_or_sku):
    client = xmlrpc.client.ServerProxy(secrets.magento_api_xmlrpc_url)
    session = client.login(secrets.magento_api_user, secrets.magento_api_pass)

    try:
        response = client.call(session, 'catalog_product.info', [product_id_or_sku])
        return response
    except xmlrpc.client.Fault as f:
        logging.warning("error while retrieving product info for {0}. {1}".format(product_id_or_sku, f.faultString))

    return None
