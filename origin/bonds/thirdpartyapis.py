import requests

def safeget(dct, *keys):
    """
        https://stackoverflow.com/questions/25833613/python-safe-method-to-get-value-of-nested-dictionary
    """
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct

def get_legal_name(lei):

    request_url = f"https://leilookup.gleif.org/api/v2/leirecords?lei={lei}"
    response = requests.get(request_url).json()

    # Validate Unique Response
    if len(response) == 1:
        return safeget(response, 0, "Entity", "LegalName", "$")

    return None




