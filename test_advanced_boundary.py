import unittest
from Order_Placement import Cart, OrderPlacement, UserProfile, RestaurantMenu
from Payment_Processing import PaymentProcessing
from User_Registration import UserRegistration

class TestCartBoundary(unittest.TestCase):
    def setUp(self):
        self.cart = Cart()

    def test_add_zero_quantity_raises(self):
        with self.assertRaises(ValueError):
            self.cart.add_item("Water", 2.00, 0)

    def test_add_negative_quantity_raises(self):
        with self.assertRaises(ValueError):
            self.cart.add_item("Water", 2.00, -1)

class TestPaymentProcessingBoundary(unittest.TestCase):
    def setUp(self):
        self.payment = PaymentProcessing()

    def test_invalid_card_length_15_digits(self):
        details = {"card_number": "123456789012345", "expiry_date": "12/25", "cvv": "123"}
        self.assertFalse(self.payment.validate_credit_card(details))

    def test_valid_card_length_16_digits(self):
        details = {"card_number": "1234567890123456", "expiry_date": "12/25", "cvv": "123"}
        self.assertTrue(self.payment.validate_credit_card(details))

    def test_declined_card(self):
        order = {"total_amount": 100.00}
        details = {"card_number": "1111222233334444", "expiry_date": "12/25", "cvv": "123"}
        result = self.payment.process_payment(order, "credit_card", details)
        self.assertIn("failed", result)

    def test_invalid_payment_method(self):
        order = {"total_amount": 100.00}
        details = {"card_number": "1234567812345678", "expiry_date": "12/25", "cvv": "123"}
        result = self.payment.process_payment(order, "bitcoin", details)
        self.assertIn("Error: Invalid payment method", result)

class TestUserRegistrationBoundary(unittest.TestCase):
    def setUp(self):
        self.registration = UserRegistration()

    def test_strong_password_success(self):
        result = self.registration.register("user@example.com", "Password123", "Password123")
        self.assertTrue(result["success"])

    def test_weak_password_missing_digit(self):
        result = self.registration.register("user@example.com", "Password", "Password")
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Password is not strong enough")

    def test_weak_password_missing_letter(self):
        result = self.registration.register("user@example.com", "12345678", "12345678")
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Password is not strong enough")

    def test_duplicate_email_registration(self):
        self.registration.register("user@example.com", "Password123", "Password123")
        result = self.registration.register("user@example.com", "Password123", "Password123")
        self.assertFalse(result["success"])
        self.assertEqual(result["error"], "Email already registered")

if __name__ == "__main__":
    unittest.main()
