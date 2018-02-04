import economics
import json
import economics_constants


def product_list():
    r = economics.get_response(economics_constants.products_url)
    return json.loads(r.text)


def product_merge(product):
    economics.item_merge(economics_constants.product_url,
                         economics_constants.products_url,
                         product['productNumber'],
                         product,
                         'product')
