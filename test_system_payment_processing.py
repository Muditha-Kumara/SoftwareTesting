import unittest
from Payment_Processing import PaymentProcessing

class TestSystemPaymentProcessing(unittest.TestCase):
    def setUp(self):
        self.processor = PaymentProcessing()
        self.order = {'total_amount': 100.0}
        self.valid_details = {'card_number': '1234567812345678', 'expiry_date': '12/25', 'cvv': '123'}
        self.invalid_details = {'card_number': '1111222233334444', 'expiry_date': '12/25', 'cvv': '123'}

    def test_valid_payment(self):
        result = self.processor.process_payment(self.order, 'credit_card', self.valid_details)
        print(result)
        self.assertIn('success', result)

    def test_invalid_payment(self):
        result = self.processor.process_payment(self.order, 'credit_card', self.invalid_details)
        print(result)
        self.assertIn('failed', result)

if __name__ == '__main__':
    unittest.main()
