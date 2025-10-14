import unittest
from unittest.mock import Mock

# --- Stub Example ---
# Suppose Restaurant_Browsing.py has a function fetch_menu_from_api()
# We'll stub it to return a fixed value for testing.
def fetch_menu_stub():
    return [{"name": "Pizza", "price": 10.0}]

class TestMenuStub(unittest.TestCase):
    def test_menu_stub_returns_fixed_value(self):
        menu = fetch_menu_stub()
        self.assertEqual(menu, [{"name": "Pizza", "price": 10.0}])

# --- Mock Example ---
# Suppose Payment_Processing.py has a PaymentGateway class with a charge() method
class TestPaymentMock(unittest.TestCase):
    def test_payment_gateway_charge_called(self):
        mock_payment_gateway = Mock()
        mock_payment_gateway.charge.return_value = True
        result = mock_payment_gateway.charge(100)
        self.assertTrue(result)
        mock_payment_gateway.charge.assert_called_with(100)

# --- Fake Example ---
# A simplified fake payment gateway for integration testing
class FakePaymentGateway:
    def charge(self, amount):
        return amount < 1000  # Accepts charges below 1000

class TestPaymentFake(unittest.TestCase):
    def test_fake_gateway_accepts_small_amount(self):
        gateway = FakePaymentGateway()
        self.assertTrue(gateway.charge(500))

    def test_fake_gateway_rejects_large_amount(self):
        gateway = FakePaymentGateway()
        self.assertFalse(gateway.charge(1500))

if __name__ == "__main__":
    unittest.main()
