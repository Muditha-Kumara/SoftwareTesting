"""
Delivery Tracking Module - Implemented using TDD methodology
This module allows users to track their order delivery in real-time.
"""

import unittest
from datetime import datetime, timedelta


class DeliveryTracker:
    """
    Tracks delivery status and location for orders.
    
    Attributes:
        order_id (str): The order being tracked.
        current_status (str): Current delivery status.
        status_history (list): Historical record of status changes.
        estimated_time (datetime): Estimated delivery time.
        driver_location (tuple): Current driver coordinates (lat, lng).
    """
    
    VALID_STATUSES = ["Order Placed", "Preparing", "Picked Up", "In Transit", "Delivered"]
    
    def __init__(self, order_id):
        """
        Initialize DeliveryTracker for an order.
        
        Args:
            order_id (str): The order ID to track.
        """
        if not order_id:
            raise ValueError("Order ID cannot be empty")
        
        self.order_id = order_id
        self.current_status = "Order Placed"
        self.status_history = [{"status": "Order Placed", "timestamp": datetime.now()}]
        self.estimated_time = None
        self.driver_location = None
    
    def update_status(self, new_status):
        """
        Update the delivery status.
        
        Args:
            new_status (str): The new status to set.
        
        Returns:
            dict: Success status and message.
        """
        if new_status not in self.VALID_STATUSES:
            return {"success": False, "message": f"Invalid status: {new_status}"}
        
        # Check for valid status transitions (can't go backwards)
        current_index = self.VALID_STATUSES.index(self.current_status)
        new_index = self.VALID_STATUSES.index(new_status)
        
        if new_index < current_index:
            return {"success": False, "message": "Cannot revert to previous status"}
        
        self.current_status = new_status
        self.status_history.append({"status": new_status, "timestamp": datetime.now()})
        
        return {"success": True, "message": f"Status updated to {new_status}"}
    
    def get_current_status(self):
        """
        Get the current delivery status.
        
        Returns:
            str: Current status.
        """
        return self.current_status
    
    def update_estimated_time(self, minutes_from_now):
        """
        Update the estimated delivery time.
        
        Args:
            minutes_from_now (int): Minutes until estimated delivery.
        
        Returns:
            dict: Success status and estimated time.
        """
        if minutes_from_now < 0:
            return {"success": False, "message": "Time cannot be negative"}
        
        self.estimated_time = datetime.now() + timedelta(minutes=minutes_from_now)
        
        return {
            "success": True,
            "estimated_time": self.estimated_time,
            "message": f"Estimated delivery in {minutes_from_now} minutes"
        }
    
    def get_estimated_time(self):
        """
        Get the estimated delivery time.
        
        Returns:
            datetime: Estimated delivery time, or None if not set.
        """
        return self.estimated_time
    
    def get_status_history(self):
        """
        Get the complete status history.
        
        Returns:
            list: List of status changes with timestamps.
        """
        return self.status_history.copy()
    
    def update_driver_location(self, latitude, longitude):
        """
        Update the driver's current location.
        
        Args:
            latitude (float): Driver's latitude.
            longitude (float): Driver's longitude.
        
        Returns:
            dict: Success status and location.
        """
        if not (-90 <= latitude <= 90):
            return {"success": False, "message": "Invalid latitude"}
        if not (-180 <= longitude <= 180):
            return {"success": False, "message": "Invalid longitude"}
        
        self.driver_location = (latitude, longitude)
        
        return {
            "success": True,
            "location": self.driver_location,
            "message": "Driver location updated"
        }
    
    def get_driver_location(self):
        """
        Get the driver's current location.
        
        Returns:
            tuple: (latitude, longitude) or None if not set.
        """
        return self.driver_location
    
    def complete_delivery(self):
        """
        Mark the delivery as complete.
        
        Returns:
            dict: Success status and message.
        """
        result = self.update_status("Delivered")
        if result['success']:
            return {"success": True, "message": "Delivery completed successfully"}
        return result


# Unit Tests for DeliveryTracker
class TestDeliveryTracker(unittest.TestCase):
    """Unit tests for the DeliveryTracker class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.tracker = DeliveryTracker("ORD001")
    
    def test_create_delivery_tracker(self):
        """Test that DeliveryTracker initializes with correct initial status."""
        self.assertIsInstance(self.tracker, DeliveryTracker)
        self.assertEqual(self.tracker.order_id, "ORD001")
        self.assertEqual(self.tracker.current_status, "Order Placed")
        self.assertEqual(len(self.tracker.status_history), 1)
    
    def test_create_tracker_empty_order_id(self):
        """Test that empty order ID raises ValueError."""
        with self.assertRaises(ValueError) as context:
            DeliveryTracker("")
        self.assertIn("Order ID cannot be empty", str(context.exception))
    
    def test_update_status_valid(self):
        """Test successfully updating to a valid status."""
        result = self.tracker.update_status("Preparing")
        
        self.assertTrue(result['success'])
        self.assertEqual(self.tracker.current_status, "Preparing")
        self.assertEqual(len(self.tracker.status_history), 2)
    
    def test_update_status_invalid(self):
        """Test that invalid status is rejected."""
        result = self.tracker.update_status("Invalid Status")
        
        self.assertFalse(result['success'])
        self.assertIn("Invalid status", result['message'])
        self.assertEqual(self.tracker.current_status, "Order Placed")
    
    def test_update_status_backward_transition(self):
        """Test that backward status transitions are prevented."""
        self.tracker.update_status("Preparing")
        self.tracker.update_status("Picked Up")
        
        result = self.tracker.update_status("Preparing")
        
        self.assertFalse(result['success'])
        self.assertIn("Cannot revert", result['message'])
        self.assertEqual(self.tracker.current_status, "Picked Up")
    
    def test_get_current_status(self):
        """Test getting current status."""
        self.assertEqual(self.tracker.get_current_status(), "Order Placed")
        
        self.tracker.update_status("In Transit")
        self.assertEqual(self.tracker.get_current_status(), "In Transit")
    
    def test_update_estimated_time(self):
        """Test updating estimated delivery time."""
        result = self.tracker.update_estimated_time(30)
        
        self.assertTrue(result['success'])
        self.assertIsNotNone(self.tracker.estimated_time)
        self.assertIn("30 minutes", result['message'])
    
    def test_update_estimated_time_negative(self):
        """Test that negative time is rejected."""
        result = self.tracker.update_estimated_time(-10)
        
        self.assertFalse(result['success'])
        self.assertIn("cannot be negative", result['message'])
    
    def test_get_estimated_time(self):
        """Test getting estimated delivery time."""
        self.assertIsNone(self.tracker.get_estimated_time())
        
        self.tracker.update_estimated_time(45)
        estimated = self.tracker.get_estimated_time()
        self.assertIsNotNone(estimated)
        self.assertIsInstance(estimated, datetime)
    
    def test_get_status_history(self):
        """Test getting complete status history."""
        self.tracker.update_status("Preparing")
        self.tracker.update_status("Picked Up")
        
        history = self.tracker.get_status_history()
        
        self.assertEqual(len(history), 3)
        self.assertEqual(history[0]['status'], "Order Placed")
        self.assertEqual(history[1]['status'], "Preparing")
        self.assertEqual(history[2]['status'], "Picked Up")
    
    def test_update_driver_location(self):
        """Test updating driver location with valid coordinates."""
        result = self.tracker.update_driver_location(40.7128, -74.0060)
        
        self.assertTrue(result['success'])
        self.assertEqual(self.tracker.driver_location, (40.7128, -74.0060))
    
    def test_update_driver_location_invalid_latitude(self):
        """Test that invalid latitude is rejected."""
        result = self.tracker.update_driver_location(100, -74.0060)
        
        self.assertFalse(result['success'])
        self.assertIn("Invalid latitude", result['message'])
    
    def test_update_driver_location_invalid_longitude(self):
        """Test that invalid longitude is rejected."""
        result = self.tracker.update_driver_location(40.7128, 200)
        
        self.assertFalse(result['success'])
        self.assertIn("Invalid longitude", result['message'])
    
    def test_get_driver_location(self):
        """Test getting driver location."""
        self.assertIsNone(self.tracker.get_driver_location())
        
        self.tracker.update_driver_location(40.7128, -74.0060)
        location = self.tracker.get_driver_location()
        
        self.assertEqual(location, (40.7128, -74.0060))
    
    def test_complete_delivery(self):
        """Test completing a delivery."""
        # Progress through statuses
        self.tracker.update_status("Preparing")
        self.tracker.update_status("Picked Up")
        self.tracker.update_status("In Transit")
        
        result = self.tracker.complete_delivery()
        
        self.assertTrue(result['success'])
        self.assertEqual(self.tracker.current_status, "Delivered")
        self.assertIn("completed successfully", result['message'])


if __name__ == '__main__':
    unittest.main()
