import economics
import json
import economics_constants


def invoice_list():
    r = economics.get_response(economics_constants.invoices_url)
    return json.loads(r.text)


def find_invoice_by_reference(ref):
    r = economics.get_response("{0}?filter=references.other$eq:{1}".format(economics_constants.invoices_url, ref))

    if r.status_code == 200:
        c = json.loads(r.text)

        if c['collection']:
            return c['collection'][0]['draftInvoiceNumber']

        return None
    else:
        return None


def invoice_merge(order):
    invoice_no = find_invoice_by_reference(order['references']['other'])

    if invoice_no:
        order['draftInvoiceNumber'] = invoice_no

    invoice = economics.item_merge(economics_constants.invoice_url,
                                   economics_constants.invoices_url,
                                   order['draftInvoiceNumber'],
                                   order,
                                   'order')

    return invoice['draftInvoiceNumber']
