"""
Order History Module - Implemented using TDD methodology
This module allows users to view and manage their order history.
"""

import unittest
from datetime import datetime


class OrderHistory:
    """
    Manages user's order history with filtering capabilities.
    
    Attributes:
        orders (list): List of order dictionaries containing order details.
    """
    
    def __init__(self):
        """Initialize OrderHistory with an empty order list."""
        self.orders = []
    
    def add_order(self, order_id, items, total, status, date):
        """
        Add a new order to the history.
        
        Args:
            order_id (str): Unique identifier for the order.
            items (str): Description of items ordered.
            total (float): Total amount of the order.
            status (str): Current status of the order (e.g., 'delivered', 'pending').
            date (str): Date when the order was placed.
        
        Returns:
            bool: True if order was successfully added.
        
        Raises:
            ValueError: If order_id is empty or total is negative.
        """
        if not order_id:
            raise ValueError("Order ID cannot be empty")
        if total < 0:
            raise ValueError("Total cannot be negative")
        
        order = {
            "order_id": order_id,
            "items": items,
            "total": total,
            "status": status,
            "date": date
        }
        self.orders.append(order)
        return True
    
    def view_order_history(self):
        """
        Get all orders in the history.
        
        Returns:
            list: List of all order dictionaries.
        """
        return self.orders.copy()
    
    def filter_orders(self, status=None, date=None):
        """
        Filter orders by status and/or date.
        
        Args:
            status (str, optional): Filter by order status.
            date (str, optional): Filter by order date.
        
        Returns:
            list: Filtered list of orders matching criteria.
        """
        filtered = self.orders.copy()
        
        if status:
            filtered = [order for order in filtered if order['status'] == status]
        
        if date:
            filtered = [order for order in filtered if order['date'] == date]
        
        return filtered
    
    def get_order_details(self, order_id):
        """
        Retrieve details of a specific order.
        
        Args:
            order_id (str): The order ID to search for.
        
        Returns:
            dict: Order details if found, None otherwise.
        """
        for order in self.orders:
            if order['order_id'] == order_id:
                return order.copy()
        return None
    
    def get_order_count(self):
        """
        Get the total number of orders in history.
        
        Returns:
            int: Total count of orders.
        """
        return len(self.orders)
    
    def get_total_spent(self):
        """
        Calculate total amount spent across all orders.
        
        Returns:
            float: Sum of all order totals.
        """
        return sum(order['total'] for order in self.orders)


# Unit Tests for OrderHistory
class TestOrderHistory(unittest.TestCase):
    """Unit tests for the OrderHistory class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.history = OrderHistory()
    
    def test_create_order_history(self):
        """Test that OrderHistory initializes with empty order list."""
        self.assertIsInstance(self.history, OrderHistory)
        self.assertEqual(len(self.history.orders), 0)
    
    def test_add_order_to_history(self):
        """Test successfully adding an order to history."""
        result = self.history.add_order("ORD001", "Pizza, Salad", 25.00, "Delivered", "2025-10-10")
        self.assertTrue(result)
        self.assertEqual(len(self.history.orders), 1)
    
    def test_view_order_history_with_orders(self):
        """Test viewing order history when orders exist."""
        self.history.add_order("ORD001", "Pizza", 25.00, "Delivered", "2025-10-10")
        self.history.add_order("ORD002", "Burger", 15.00, "Pending", "2025-10-11")
        
        orders = self.history.view_order_history()
        self.assertEqual(len(orders), 2)
        self.assertEqual(orders[0]['order_id'], "ORD001")
    
    def test_view_order_history_empty(self):
        """Test viewing order history when no orders exist."""
        orders = self.history.view_order_history()
        self.assertEqual(len(orders), 0)
        self.assertIsInstance(orders, list)
    
    def test_filter_orders_by_status(self):
        """Test filtering orders by status."""
        self.history.add_order("ORD001", "Pizza", 25.00, "Delivered", "2025-10-10")
        self.history.add_order("ORD002", "Burger", 15.00, "Pending", "2025-10-11")
        self.history.add_order("ORD003", "Salad", 12.00, "Delivered", "2025-10-12")
        
        delivered = self.history.filter_orders(status="Delivered")
        self.assertEqual(len(delivered), 2)
        self.assertTrue(all(order['status'] == "Delivered" for order in delivered))
    
    def test_filter_orders_by_date(self):
        """Test filtering orders by date."""
        self.history.add_order("ORD001", "Pizza", 25.00, "Delivered", "2025-10-10")
        self.history.add_order("ORD002", "Burger", 15.00, "Pending", "2025-10-11")
        self.history.add_order("ORD003", "Salad", 12.00, "Delivered", "2025-10-10")
        
        orders_on_date = self.history.filter_orders(date="2025-10-10")
        self.assertEqual(len(orders_on_date), 2)
        self.assertTrue(all(order['date'] == "2025-10-10" for order in orders_on_date))
    
    def test_filter_orders_multiple_criteria(self):
        """Test filtering orders by both status and date."""
        self.history.add_order("ORD001", "Pizza", 25.00, "Delivered", "2025-10-10")
        self.history.add_order("ORD002", "Burger", 15.00, "Pending", "2025-10-10")
        self.history.add_order("ORD003", "Salad", 12.00, "Delivered", "2025-10-11")
        
        filtered = self.history.filter_orders(status="Delivered", date="2025-10-10")
        self.assertEqual(len(filtered), 1)
        self.assertEqual(filtered[0]['order_id'], "ORD001")
    
    def test_get_order_details(self):
        """Test retrieving specific order details."""
        self.history.add_order("ORD001", "Pizza", 25.00, "Delivered", "2025-10-10")
        
        details = self.history.get_order_details("ORD001")
        self.assertIsNotNone(details)
        self.assertEqual(details['items'], "Pizza")
        self.assertEqual(details['total'], 25.00)
    
    def test_get_order_details_not_found(self):
        """Test retrieving details for non-existent order."""
        details = self.history.get_order_details("ORD999")
        self.assertIsNone(details)
    
    def test_order_count(self):
        """Test getting correct count of orders."""
        self.assertEqual(self.history.get_order_count(), 0)
        
        self.history.add_order("ORD001", "Pizza", 25.00, "Delivered", "2025-10-10")
        self.assertEqual(self.history.get_order_count(), 1)
        
        self.history.add_order("ORD002", "Burger", 15.00, "Pending", "2025-10-11")
        self.assertEqual(self.history.get_order_count(), 2)
    
    def test_add_order_invalid_order_id(self):
        """Test that empty order_id raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.history.add_order("", "Pizza", 25.00, "Delivered", "2025-10-10")
        self.assertIn("Order ID cannot be empty", str(context.exception))
    
    def test_add_order_negative_total(self):
        """Test that negative total raises ValueError."""
        with self.assertRaises(ValueError) as context:
            self.history.add_order("ORD001", "Pizza", -25.00, "Delivered", "2025-10-10")
        self.assertIn("Total cannot be negative", str(context.exception))
    
    def test_get_total_spent(self):
        """Test calculating total amount spent."""
        self.history.add_order("ORD001", "Pizza", 25.00, "Delivered", "2025-10-10")
        self.history.add_order("ORD002", "Burger", 15.00, "Delivered", "2025-10-11")
        self.history.add_order("ORD003", "Salad", 10.00, "Delivered", "2025-10-12")
        
        total = self.history.get_total_spent()
        self.assertEqual(total, 50.00)


if __name__ == '__main__':
    unittest.main()
