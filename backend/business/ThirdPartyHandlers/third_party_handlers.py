from abc import ABC, abstractmethod
from typing import Dict


class PaymentHandler:
    def process_payment(self, amount: int, payment_details: Dict) -> bool:
        pass
