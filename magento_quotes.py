import mysql.connector
import sendgrid_constants
import secrets
import sendgrid
import logging
from sendgrid.helpers.mail import *
from state_management import set_state, read_state


def email_unpaid_quotes():
    last_entity_id = read_state('sales_flat_quote')

    cn = mysql.connector.connect(user=secrets.mysql_magento_user,
                                 host=secrets.mysql_magento_host,
                                 database=secrets.mysql_magento_database,
                                 password=secrets.mysql_magento_password)
    quotes_cursor = cn.cursor(buffered=True)
    quote_items_cursor = cn.cursor()

    quotes_query = ("SELECT entity_id, "
                    "  created_at, "
                    "  base_currency_code, "
                    "  base_grand_total, "
                    "  customer_email, "
                    "  customer_firstname, "
                    "  customer_lastname " 
                    "FROM sales_flat_quote "
                    "WHERE is_active = 1 "
                    "  AND customer_email IS NOT NULL"
                    "  AND entity_id > {} "
                    "  AND created_at < DATE_SUB( NOW( ) , INTERVAL 1 HOUR ) "
                    "ORDER BY entity_id").format(last_entity_id)

    quote_items_query = ("SELECT sku,"
                         "  name,"
                         "  qty,"
                         "  base_row_total "
                         "FROM sales_flat_quote_item "
                         "WHERE quote_id = {}")

    quotes_cursor.execute(quotes_query)

    for (quote_id,
         created_at,
         base_currency_code,
         base_grand_total,
         customer_email,
         customer_firstname,
         customer_lastname) in quotes_cursor:

        quote_items_query_formatted = quote_items_query.format(quote_id)

        quote_items_cursor.execute(quote_items_query_formatted)

        quote_items = ("<table style=\"width:600px\">"
                       "<tr>"
                       "<td><b>SKU</b></td>"
                       "<td><b>Produkt navn</b></td>"
                       "<td><b>Qty</b></td>"
                       "<td><b>Pris</b></td>"
                       "</tr>")

        for (sku,
             name,
             qty,
             base_row_total) in quote_items_cursor:

            quote_items += sendgrid_constants.quote_unpaid_item.format(**{'sku': sku,
                                                                          'name': name,
                                                                          'qty': qty,
                                                                          'base_row_total': base_row_total})
        quote_items += "</table>"

        send_quote_email({'quote_id': quote_id,
                          'created_at': created_at,
                          'base_currency_code': base_currency_code,
                          'base_grand_total': base_grand_total,
                          'customer_email': customer_email,
                          'customer_firstname': customer_firstname,
                          'customer_lastname': customer_lastname,
                          'quote_items': quote_items})

    quote_items_cursor.close()
    quotes_cursor.close()
    cn.close()


def send_quote_email(email):
    try:
        sg = sendgrid.SendGridAPIClient(apikey=secrets.sendgrid_api_key)

        content = Content("text/html", sendgrid_constants.quotes_unpaid_content.format(**email))

        msg = Mail(from_email=Email(sendgrid_constants.quotes_unpaid_from_email),
                   to_email=Email(sendgrid_constants.quotes_unpaid_to_email),
                   subject=sendgrid_constants.quotes_unpaid_subject.format(**email),
                   content=content)
        msg.personalizations[0].add_cc(Email(sendgrid_constants.quotes_unpaid_cc_email))

        sg.client.mail.send.post(request_body=msg.get())

        logging.info("sent quote email regarding quote {}".format(email['quote_id']))
        set_state('sales_flat_quote', email['quote_id'])
    except:
        logging.warning("error while sending email regarding quote {}".format(email['quote_id']))
