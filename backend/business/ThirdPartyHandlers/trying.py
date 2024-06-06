import third_party_handlers

yes = third_party_handlers.PaymentHandler()
yes.add_payment_method("test method", {"test": "test"})
yes.remove_payment_method("test method")