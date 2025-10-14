"""
Promo Code Manager Module - Implemented using TDD methodology
This module allows users to apply promo codes for discounts on orders.
"""

import unittest
from datetime import datetime, timedelta


class PromoCodeManager:
    """
    Manages promo codes and discount applications.
    
    Attributes:
        promo_codes (dict): Dictionary of promo codes with their details.
        used_codes (dict): Tracking of used one-time promo codes by user.
    """
    
    def __init__(self):
        """Initialize PromoCodeManager with empty promo codes."""
        self.promo_codes = {}
        self.used_codes = {}  # {user_id: [code1, code2, ...]}
    
    def create_promo_code(self, code, discount_type, discount_value, 
                         expiry_date=None, min_order_amount=0, one_time_use=False):
        """
        Create a new promo code.
        
        Args:
            code (str): The promo code string.
            discount_type (str): Either 'percentage' or 'fixed'.
            discount_value (float): The discount amount or percentage.
            expiry_date (datetime, optional): Expiration date.
            min_order_amount (float, optional): Minimum order amount required.
            one_time_use (bool, optional): Whether code can only be used once per user.
        
        Returns:
            dict: Success status and message.
        """
        if not code or not code.strip():
            return {"success": False, "message": "Promo code cannot be empty"}
        
        code = code.strip().upper()
        
        if code in self.promo_codes:
            return {"success": False, "message": "Promo code already exists"}
        
        if discount_type not in ['percentage', 'fixed']:
            return {"success": False, "message": "Invalid discount type"}
        
        if discount_value <= 0:
            return {"success": False, "message": "Discount value must be positive"}
        
        if discount_type == 'percentage' and discount_value > 100:
            return {"success": False, "message": "Percentage cannot exceed 100"}
        
        self.promo_codes[code] = {
            "discount_type": discount_type,
            "discount_value": discount_value,
            "expiry_date": expiry_date,
            "min_order_amount": min_order_amount,
            "one_time_use": one_time_use,
            "active": True
        }
        
        return {"success": True, "message": f"Promo code {code} created"}
    
    def validate_promo_code(self, code, user_id, order_amount):
        """
        Validate if a promo code can be applied.
        
        Args:
            code (str): The promo code to validate.
            user_id (str): ID of the user applying the code.
            order_amount (float): The order amount.
        
        Returns:
            dict: Validation result with success status and message.
        """
        if not code or not code.strip():
            return {"success": False, "message": "Promo code cannot be empty"}
        
        code = code.strip().upper()
        
        # Check if code exists
        if code not in self.promo_codes:
            return {"success": False, "message": "Invalid promo code"}
        
        promo = self.promo_codes[code]
        
        # Check if active
        if not promo['active']:
            return {"success": False, "message": "Promo code is inactive"}
        
        # Check expiry
        if promo['expiry_date'] and datetime.now() > promo['expiry_date']:
            return {"success": False, "message": "Promo code has expired"}
        
        # Check minimum order amount
        if order_amount < promo['min_order_amount']:
            return {
                "success": False,
                "message": f"Minimum order amount is ${promo['min_order_amount']:.2f}"
            }
        
        # Check one-time use
        if promo['one_time_use']:
            if user_id in self.used_codes and code in self.used_codes[user_id]:
                return {"success": False, "message": "Promo code already used"}
        
        return {"success": True, "message": "Promo code is valid"}
    
    def apply_discount(self, code, user_id, order_amount):
        """
        Apply a promo code and calculate the discount.
        
        Args:
            code (str): The promo code to apply.
            user_id (str): ID of the user applying the code.
            order_amount (float): The order amount.
        
        Returns:
            dict: Result with discount amount and final total.
        """
        # Validate the code first
        validation = self.validate_promo_code(code, user_id, order_amount)
        if not validation['success']:
            return validation
        
        code = code.strip().upper()
        promo = self.promo_codes[code]
        
        # Calculate discount
        if promo['discount_type'] == 'percentage':
            discount_amount = (order_amount * promo['discount_value']) / 100
        else:  # fixed
            discount_amount = min(promo['discount_value'], order_amount)
        
        final_total = order_amount - discount_amount
        
        # Mark as used if one-time use
        if promo['one_time_use']:
            if user_id not in self.used_codes:
                self.used_codes[user_id] = []
            self.used_codes[user_id].append(code)
        
        return {
            "success": True,
            "discount_amount": round(discount_amount, 2),
            "final_total": round(final_total, 2),
            "message": f"Discount of ${discount_amount:.2f} applied"
        }
    
    def get_discount_amount(self, code, order_amount):
        """
        Calculate discount amount without applying the code.
        
        Args:
            code (str): The promo code.
            order_amount (float): The order amount.
        
        Returns:
            float: The discount amount, or 0 if invalid.
        """
        code = code.strip().upper()
        
        if code not in self.promo_codes:
            return 0.0
        
        promo = self.promo_codes[code]
        
        if promo['discount_type'] == 'percentage':
            discount = (order_amount * promo['discount_value']) / 100
        else:
            discount = min(promo['discount_value'], order_amount)
        
        return round(discount, 2)
    
    def deactivate_promo_code(self, code):
        """
        Deactivate a promo code.
        
        Args:
            code (str): The promo code to deactivate.
        
        Returns:
            dict: Success status and message.
        """
        code = code.strip().upper()
        
        if code not in self.promo_codes:
            return {"success": False, "message": "Promo code not found"}
        
        self.promo_codes[code]['active'] = False
        return {"success": True, "message": f"Promo code {code} deactivated"}
    
    def get_active_promo_codes(self):
        """
        Get all active promo codes.
        
        Returns:
            list: List of active promo code names.
        """
        return [
            code for code, details in self.promo_codes.items()
            if details['active']
        ]


# Unit Tests for PromoCodeManager
class TestPromoCodeManager(unittest.TestCase):
    """Unit tests for the PromoCodeManager class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.manager = PromoCodeManager()
    
    def test_create_promo_manager(self):
        """Test that PromoCodeManager initializes correctly."""
        self.assertIsInstance(self.manager, PromoCodeManager)
        self.assertEqual(len(self.manager.promo_codes), 0)
    
    def test_create_promo_code_percentage(self):
        """Test creating a percentage-based promo code."""
        result = self.manager.create_promo_code("SAVE20", "percentage", 20)
        
        self.assertTrue(result['success'])
        self.assertIn("SAVE20", self.manager.promo_codes)
    
    def test_create_promo_code_fixed(self):
        """Test creating a fixed-amount promo code."""
        result = self.manager.create_promo_code("GET10", "fixed", 10)
        
        self.assertTrue(result['success'])
        self.assertIn("GET10", self.manager.promo_codes)
    
    def test_create_duplicate_promo_code(self):
        """Test that duplicate promo codes are rejected."""
        self.manager.create_promo_code("SAVE20", "percentage", 20)
        result = self.manager.create_promo_code("SAVE20", "percentage", 30)
        
        self.assertFalse(result['success'])
        self.assertIn("already exists", result['message'])
    
    def test_create_promo_code_empty(self):
        """Test that empty promo code is rejected."""
        result = self.manager.create_promo_code("", "percentage", 20)
        
        self.assertFalse(result['success'])
        self.assertIn("cannot be empty", result['message'])
    
    def test_create_promo_code_invalid_type(self):
        """Test that invalid discount type is rejected."""
        result = self.manager.create_promo_code("TEST", "invalid", 20)
        
        self.assertFalse(result['success'])
        self.assertIn("Invalid discount type", result['message'])
    
    def test_create_promo_code_negative_value(self):
        """Test that negative discount value is rejected."""
        result = self.manager.create_promo_code("TEST", "percentage", -10)
        
        self.assertFalse(result['success'])
        self.assertIn("must be positive", result['message'])
    
    def test_create_promo_code_percentage_over_100(self):
        """Test that percentage over 100 is rejected."""
        result = self.manager.create_promo_code("TEST", "percentage", 150)
        
        self.assertFalse(result['success'])
        self.assertIn("cannot exceed 100", result['message'])
    
    def test_validate_promo_code_valid(self):
        """Test validating a valid promo code."""
        self.manager.create_promo_code("SAVE20", "percentage", 20)
        result = self.manager.validate_promo_code("SAVE20", "U001", 100)
        
        self.assertTrue(result['success'])
    
    def test_validate_promo_code_invalid(self):
        """Test validating an invalid promo code."""
        result = self.manager.validate_promo_code("INVALID", "U001", 100)
        
        self.assertFalse(result['success'])
        self.assertIn("Invalid promo code", result['message'])
    
    def test_validate_promo_code_expired(self):
        """Test that expired promo code is rejected."""
        expired_date = datetime.now() - timedelta(days=1)
        self.manager.create_promo_code("EXPIRED", "percentage", 20, expiry_date=expired_date)
        
        result = self.manager.validate_promo_code("EXPIRED", "U001", 100)
        
        self.assertFalse(result['success'])
        self.assertIn("expired", result['message'])
    
    def test_validate_promo_code_not_expired(self):
        """Test that non-expired promo code is valid."""
        future_date = datetime.now() + timedelta(days=7)
        self.manager.create_promo_code("VALID", "percentage", 20, expiry_date=future_date)
        
        result = self.manager.validate_promo_code("VALID", "U001", 100)
        
        self.assertTrue(result['success'])
    
    def test_apply_discount_percentage(self):
        """Test applying percentage discount correctly."""
        self.manager.create_promo_code("SAVE20", "percentage", 20)
        result = self.manager.apply_discount("SAVE20", "U001", 100)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['discount_amount'], 20.0)
        self.assertEqual(result['final_total'], 80.0)
    
    def test_apply_discount_fixed(self):
        """Test applying fixed discount correctly."""
        self.manager.create_promo_code("GET10", "fixed", 10)
        result = self.manager.apply_discount("GET10", "U001", 50)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['discount_amount'], 10.0)
        self.assertEqual(result['final_total'], 40.0)
    
    def test_apply_discount_fixed_exceeds_total(self):
        """Test that fixed discount doesn't exceed order total."""
        self.manager.create_promo_code("BIG50", "fixed", 50)
        result = self.manager.apply_discount("BIG50", "U001", 30)
        
        self.assertTrue(result['success'])
        self.assertEqual(result['discount_amount'], 30.0)
        self.assertEqual(result['final_total'], 0.0)
    
    def test_minimum_order_requirement(self):
        """Test minimum order amount enforcement."""
        self.manager.create_promo_code("MIN50", "percentage", 10, min_order_amount=50)
        result = self.manager.validate_promo_code("MIN50", "U001", 30)
        
        self.assertFalse(result['success'])
        self.assertIn("Minimum order amount", result['message'])
    
    def test_minimum_order_requirement_met(self):
        """Test promo code valid when minimum order is met."""
        self.manager.create_promo_code("MIN50", "percentage", 10, min_order_amount=50)
        result = self.manager.validate_promo_code("MIN50", "U001", 60)
        
        self.assertTrue(result['success'])
    
    def test_one_time_use_promo(self):
        """Test one-time use promo code enforcement."""
        self.manager.create_promo_code("ONCE", "fixed", 10, one_time_use=True)
        
        # First use should succeed
        result1 = self.manager.apply_discount("ONCE", "U001", 50)
        self.assertTrue(result1['success'])
        
        # Second use by same user should fail
        result2 = self.manager.apply_discount("ONCE", "U001", 50)
        self.assertFalse(result2['success'])
        self.assertIn("already used", result2['message'])
    
    def test_one_time_use_different_users(self):
        """Test one-time use code can be used by different users."""
        self.manager.create_promo_code("ONCE", "fixed", 10, one_time_use=True)
        
        result1 = self.manager.apply_discount("ONCE", "U001", 50)
        self.assertTrue(result1['success'])
        
        # Different user should be able to use it
        result2 = self.manager.apply_discount("ONCE", "U002", 50)
        self.assertTrue(result2['success'])
    
    def test_get_discount_amount(self):
        """Test calculating discount amount without applying."""
        self.manager.create_promo_code("SAVE20", "percentage", 20)
        discount = self.manager.get_discount_amount("SAVE20", 100)
        
        self.assertEqual(discount, 20.0)
    
    def test_get_discount_amount_invalid_code(self):
        """Test discount amount for invalid code returns 0."""
        discount = self.manager.get_discount_amount("INVALID", 100)
        
        self.assertEqual(discount, 0.0)
    
    def test_deactivate_promo_code(self):
        """Test deactivating a promo code."""
        self.manager.create_promo_code("TEMP", "percentage", 15)
        result = self.manager.deactivate_promo_code("TEMP")
        
        self.assertTrue(result['success'])
        
        # Should not be valid after deactivation
        validation = self.manager.validate_promo_code("TEMP", "U001", 100)
        self.assertFalse(validation['success'])
    
    def test_get_active_promo_codes(self):
        """Test retrieving all active promo codes."""
        self.manager.create_promo_code("CODE1", "percentage", 10)
        self.manager.create_promo_code("CODE2", "fixed", 5)
        self.manager.create_promo_code("CODE3", "percentage", 20)
        self.manager.deactivate_promo_code("CODE2")
        
        active_codes = self.manager.get_active_promo_codes()
        
        self.assertEqual(len(active_codes), 2)
        self.assertIn("CODE1", active_codes)
        self.assertNotIn("CODE2", active_codes)
        self.assertIn("CODE3", active_codes)
    
    def test_case_insensitive_promo_codes(self):
        """Test that promo codes are case-insensitive."""
        self.manager.create_promo_code("save20", "percentage", 20)
        
        result = self.manager.validate_promo_code("SAVE20", "U001", 100)
        self.assertTrue(result['success'])
        
        result = self.manager.validate_promo_code("SaVe20", "U001", 100)
        self.assertTrue(result['success'])


if __name__ == '__main__':
    unittest.main()
