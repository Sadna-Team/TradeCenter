class AddressDTO:
    def __init__(self, address_id, address, city, state, country, postal_code):
        self.address_id = address_id
        self.address = address
        self.city = city
        self.state = state
        self.country = country
        self.postal_code = postal_code

    def to_dict(self):
        return {
            'address_id': self.address_id,
            'address': self.address,
            'city': self.city,
            'state': self.state,
            'country': self.country,
            'postal_code': self.postal_code
        }


class SearchFacade:
    # singleton
    __instance = None

    def __new__(cls):
        if SearchFacade.__instance is None:
            SearchFacade.__instance = object.__new__(cls)
        return SearchFacade.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True


class MarketFacade:
    # singleton
    __instance = None

    def __new__(cls):
        if MarketFacade.__instance is None:
            MarketFacade.__instance = object.__new__(cls)
        return MarketFacade.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            # here you can add fields
