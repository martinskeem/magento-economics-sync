import requests
import logging
import json
import secrets


def get_response(url):
    r = requests.get(url, headers=secrets.economics_headers)
    return r


def item_merge(single_item_url, list_items_url, item_key, item, entity_name):
    r = get_response(single_item_url.format(item_key))

    if r.status_code == 200:  # exists
        ru = requests.put(single_item_url.format(item_key), headers=secrets.economics_headers, json=item)
        if ru.status_code == 200:
            return json.loads(ru.text)
        else:
            logging.warning("error while updating {0} '{1}': status {2}. {3}".format(entity_name,
                                                                                     item_key,
                                                                                     ru.status_code,
                                                                                     ru.text))
    elif r.status_code == 404:  # does not exist
        ru = requests.post(list_items_url, headers=secrets.economics_headers, json=item)
        if ru.status_code == 201:
            return json.loads(ru.text)
        else:
            logging.warning("error while creating {0} '{1}': status {2}. {3}".format(entity_name,
                                                                                     item_key,
                                                                                     ru.status_code,
                                                                                     ru.text))

    else:
        logging.warning("error while synchronizing {0} '{1}': status {2}. {3}".format(entity_name,
                                                                                      item_key,
                                                                                      r.status_code,
                                                                                      r.text))

    return None
