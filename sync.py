from economics_products import product_merge
from economics_customers import customer_merge
from magento_orders import orders_list, order_info
from magento_products import products_list, product_info
from economics_invoices import invoice_merge
import logging
import logging.config
import os
import economics_constants


def main():
    config_file = os.path.join(os.path.dirname(__file__),
                               'logging.conf')

    logging.config.fileConfig(config_file)
    logging.info('starting')

    sync_products(delta_load_days=1)
    sync_orders(delta_load_days=1)

    logging.info('finished')


def sync_orders(delta_load_days):
    i = 0
    for order_item in orders_list(delta_load_days):

        if order_item['status'] != "complete":
            logging.debug("skipping order '{0}' with status '{1}'".format(order_item["increment_id"],
                                                                          order_item['status']))
            continue

        logging.info("synchronizing order '{0}'".format(order_item["increment_id"]))

        order = order_info(order_item["increment_id"])

        customer_data = {'name': "{0} {1}".format(order["billing_address"]["firstname"],
                                                  order["billing_address"]["lastname"]),
                         'email': order["billing_address"]["email"],
                         'address': order["billing_address"]["street"],
                         'city': order["billing_address"]["city"],
                         'zip': order["billing_address"]["postcode"],
                         'country': order["billing_address"]["country_id"],
                         'telephoneAndFaxNumber': order["billing_address"]["telephone"],
                         'currency': order["order_currency_code"],
                         'customerGroup': {'customerGroupNumber': economics_constants.customer_group},
                         'customerNumber': int(order_item["increment_id"]),
                         'paymentTerms': {'paymentTermsNumber': economics_constants.customer_paymentterms},
                         'vatZone': {'vatZoneNumber': economics_constants.customer_vatzone}}

        customer_no = customer_merge(customer_data)

        order_data = {'draftInvoiceNumber': int(order_item["increment_id"]),
                      'currency': order["order_currency_code"],
                      'date': order["created_at"],
                      'customer': {'customerNumber': customer_no},
                      'layout': {'layoutNumber': economics_constants.invoice_layout},
                      'paymentTerms': {'paymentTermsNumber': economics_constants.customer_paymentterms},
                      'recipient': {'name': "{0} {1}".format(order["billing_address"]["firstname"],
                                                             order["billing_address"]["lastname"]),
                                    'address': order["billing_address"]["street"],
                                    'city': order["billing_address"]["city"],
                                    'zip': order["billing_address"]["postcode"],
                                    'vatZone': {'vatZoneNumber': economics_constants.customer_vatzone}},
                      'references': {'other': order_item["increment_id"]},
                      'lines': []}

        err = False
        for item in order['items']:
            p = product_info(item['product_id'])

            if p is not None:
                line = {'description': item['name'],
                        'product': {'productNumber': p['sku']},
                        'quantity': float(item['qty_ordered']),
                        'unitNetPrice': round(float(item['price']) * economics_constants.invoice_vat_reverse_rate, 2)}

                order_data['lines'].append(line)
            else:
                err = True
                break

        shipping = {'description': 'Fragt',
                    'product': {'productNumber': economics_constants.invoice_shipping_product_id},
                    'quantity': 1,
                    'unitNetPrice': round(float(order['shipping_amount']) * economics_constants.invoice_vat_reverse_rate, 2)}

        order_data['lines'].append(shipping)

        if not err:
            invoice_merge(order_data)

        i += 1

    logging.info('finished synchronizing {0} orders'.format(i))


def sync_products(delta_load_days):
    i = 0
    for product_item in products_list(delta_load_days):
        logging.info("synchronizing '{0}'".format(product_item['sku']))

        product = product_info(product_item["sku"])

        data = {'name': product_item['name'],
                'productGroup': {'productGroupNumber': economics_constants.product_group},
                'productNumber': product_item['sku'],
                'salesPrice': float(product['price'])}

        product_merge(data)
        i += 1

    logging.info('finished synchronizing {0} products'.format(i))


if __name__ == "__main__":
    main()
