import unittest
from Order_Placement import OrderPlacement, Cart, UserProfile, RestaurantMenu, PaymentMethod

class TestIntegrationOrderPlacement(unittest.TestCase):
    def setUp(self):
        self.cart = Cart()
        self.cart.add_item('Pizza', 10.0, 2)
        self.user_profile = UserProfile(delivery_address='123 Main St')
        self.menu = RestaurantMenu(available_items=['Pizza', 'Burger'])
        self.order_placement = OrderPlacement(self.cart, self.user_profile, self.menu)
        self.payment_method = PaymentMethod()

    def test_place_order_success(self):
        result = self.order_placement.confirm_order(self.payment_method)
        print(result)
        self.assertTrue(result['success'])

    def test_place_order_unavailable_item(self):
        self.cart.add_item('Sushi', 12.0, 1)  # Not in menu
        result = self.order_placement.validate_order()
        print(result)
        self.assertFalse(result['success'])

if __name__ == '__main__':
    unittest.main()
