import requests

def safeGet(dct, *keys):
    """
        Method to safely access nested values from a dictionary
    """
    for key in keys:
        try:
            dct = dct[key]
        except KeyError:
            return None
    return dct

def get_legal_name(lei):
    """
        Access the legal name from the GLEIF API using a given lei
    """

    request_url = f"https://leilookup.gleif.org/api/v2/leirecords?lei={lei}"
    response = requests.get(request_url).json()

    # Validate Unique Response
    if len(response) == 1:
        return safeGet(response, 0, "Entity", "LegalName", "$")

    return None




