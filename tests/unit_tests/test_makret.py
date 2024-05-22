import unittest
from backend.business.market import MarketFacade
from backend.business.roles import RolesFacade
from unittest.mock import MagicMock

class test_marketFacade:
    def setup(self):
        self.market = MarketFacade()

    def test_singleton(self):
        market2 = MarketFacade()
        assert self.market == market2

    def test_create_admin(self):
        self.market.create_admin('admin', 'admin')
        assert self.market.roles_facade.ad == 'admin'