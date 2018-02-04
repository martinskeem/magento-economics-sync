import economics
import json
import economics_constants


def customers_list():
    r = economics.get_response(economics_constants.customers_url)
    return json.loads(r.text)


def find_customer_number_by_email(email):
    if email == "" or email is None:
        return None

    r = economics.get_response("{0}?filter=email$eq:{1}".format(economics_constants.customers_url,
                                                                email))

    if r.status_code == 200:
        c = json.loads(r.text)

        if c['collection']:
            return c['collection'][0]['customerNumber']

        return None
    else:
        return None


def customer_merge(customer):
    customer_no = find_customer_number_by_email(customer['email'])

    if customer_no:
        return customer_no

    customer = economics.item_merge(economics_constants.customer_url,
                                    economics_constants.customers_url,
                                    customer['customerNumber'],
                                    customer,
                                    'customer')

    return customer
