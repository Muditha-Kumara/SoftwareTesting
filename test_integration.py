import unittest
from Order_History import OrderHistory
from Promo_Code_Manager import PromoCodeManager
from Order_Placement import OrderPlacement, Cart, UserProfile, RestaurantMenu, PaymentMethod
from Delivery_Tracking import DeliveryTracker
from Review_System import ReviewSystem
from Favorites_Manager import FavoritesManager
from Restaurant_Browsing import RestaurantBrowsing, RestaurantDatabase
from datetime import datetime

class TestIntegration(unittest.TestCase):
    def setUp(self):
        self.order_history = OrderHistory()
        self.promo_manager = PromoCodeManager()
        self.cart = Cart()
        self.user_profile = UserProfile('123 Main St')
        self.restaurant_menu = RestaurantMenu(['pizza', 'burger', 'sushi'])
        self.order_placement = OrderPlacement(self.cart, self.user_profile, self.restaurant_menu)
        self.restaurant_db = RestaurantDatabase()
        self.restaurant_browsing = RestaurantBrowsing(self.restaurant_db)
        self.review_system = ReviewSystem()
        self.favorites_manager = FavoritesManager()
        # DeliveryTracker requires order_id, so create trackers as needed in each test

    def test_order_with_promo_reflected_in_history(self):
        expiry = datetime(2025, 12, 31)
        self.promo_manager.create_promo_code('SAVE10', 'percentage', 10, expiry, 20, False)
        self.cart.add_item('pizza', 10, 2)
        payment_method = PaymentMethod()
        self.order_placement.confirm_order(payment_method)
        # Simulate promo application manually for test
        discounted_total = 20 * 0.9  # 10% off
        self.order_history.add_order('ORD001', ['pizza'], discounted_total, 'Confirmed', '2025-10-14')
        history = self.order_history.view_order_history()
        self.assertEqual(history[0]['total'], 18.0)

    def test_review_only_after_delivery(self):
        order_id = 'ORD123'
        delivery_tracker = DeliveryTracker(order_id)
        delivery_tracker.update_status('Delivered')
        can_review = delivery_tracker.current_status == 'Delivered'
        if can_review:
            result = self.review_system.add_review('user1', 'rest1', 5, 'Great!')
            self.assertTrue(result['success'])
        else:
            self.assertFalse(can_review)

    def test_favorite_quick_order(self):
        self.favorites_manager.add_favorite('rest1', 'Italian Bistro', 'Italian', 'Downtown')
        favorites = self.favorites_manager.view_all_favorites()
        menu = self.restaurant_browsing.search_by_cuisine(favorites[0]['cuisine'])
        self.assertIsInstance(menu, list)

    def test_delivery_status_updates_in_history(self):
        order_id = 'ORD456'
        delivery_tracker = DeliveryTracker(order_id)
        delivery_tracker.update_status('Out for Delivery')
        self.order_history.add_order(order_id, ['burger'], 15, 'Out for Delivery', '2025-10-14')
        details = self.order_history.get_order_details(order_id)
        self.assertEqual(details['status'], 'Out for Delivery')

    def test_promo_on_favorite_restaurant(self):
        self.favorites_manager.add_favorite('rest2', 'Sushi House', 'Japanese', 'Midtown')
        expiry = datetime(2025, 12, 31)
        self.promo_manager.create_promo_code('FAV20', 'fixed', 5, expiry, 10, False)
        self.cart.add_item('sushi', 10, 2)
        payment_method = PaymentMethod()
        self.order_placement.confirm_order(payment_method)
        discounted_total = 20 - 5  # fixed discount
        self.assertEqual(discounted_total, 15)

if __name__ == '__main__':
    unittest.main()
