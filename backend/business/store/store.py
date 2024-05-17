from typing import Dict
class StoreFacade:
    # singleton
    __instance = None

    def __new__(cls):
        if StoreFacade.__instance is None:
            StoreFacade.__instance = object.__new__(cls)
        return StoreFacade.__instance

    def __init__(self):
        if not hasattr(self, '_initialized'):
            self._initialized = True
            # here you can add fields

    def check_product_availability(self, store_id, product_id, amount) -> bool:
        pass

    def calculate_total_price(self, basket: Dict[int, Dict[int, int]]) -> int: # store_id, product_id, amount
        pass

    def remove_product(self, store_id, product_id, amount) -> None:
        pass