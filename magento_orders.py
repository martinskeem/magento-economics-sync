import secrets
import xmlrpc.client
import logging
from datetime import datetime, timedelta


def orders_list(updated_at_days_ago):
    start_date_delta_load = (datetime.today() - timedelta(days=updated_at_days_ago)).strftime("%Y-%m-%d 00:00:00")

    client = xmlrpc.client.ServerProxy(secrets.magento_api_xmlrpc_url)
    session = client.login(secrets.magento_api_user, secrets.magento_api_pass)

    response = client.call(session, 'sales_order.list', [{'updated_at': {'from': start_date_delta_load}}])

    logging.debug("retrieved {0} orders".format(len(response)))
    
    return response


def order_info(increment_id):
    client = xmlrpc.client.ServerProxy(secrets.magento_api_xmlrpc_url)
    session = client.login(secrets.magento_api_user, secrets.magento_api_pass)

    response = client.call(session, 'sales_order.info', [increment_id])

    return response
