"""
Favorites Manager Module - Implemented using TDD methodology
This module allows users to manage their favorite restaurants.
"""

import unittest


class FavoritesManager:
    """
    Manages user's favorite restaurants.
    
    Attributes:
        favorites (set): Set of favorite restaurant IDs to prevent duplicates.
        favorite_details (dict): Dictionary mapping restaurant IDs to their details.
    """
    
    def __init__(self):
        """Initialize FavoritesManager with empty favorites."""
        self.favorites = set()
        self.favorite_details = {}
    
    def add_favorite(self, restaurant_id, restaurant_name, cuisine, location):
        """
        Add a restaurant to favorites.
        
        Args:
            restaurant_id (str): Unique identifier for the restaurant.
            restaurant_name (str): Name of the restaurant.
            cuisine (str): Type of cuisine.
            location (str): Restaurant location.
        
        Returns:
            dict: Success status and message.
        """
        if not restaurant_id:
            return {"success": False, "message": "Restaurant ID cannot be empty"}
        
        if restaurant_id in self.favorites:
            return {"success": False, "message": "Restaurant already in favorites"}
        
        self.favorites.add(restaurant_id)
        self.favorite_details[restaurant_id] = {
            "name": restaurant_name,
            "cuisine": cuisine,
            "location": location
        }
        
        return {"success": True, "message": "Restaurant added to favorites"}
    
    def remove_favorite(self, restaurant_id):
        """
        Remove a restaurant from favorites.
        
        Args:
            restaurant_id (str): ID of the restaurant to remove.
        
        Returns:
            dict: Success status and message.
        """
        if restaurant_id not in self.favorites:
            return {"success": False, "message": "Restaurant not in favorites"}
        
        self.favorites.remove(restaurant_id)
        del self.favorite_details[restaurant_id]
        
        return {"success": True, "message": "Restaurant removed from favorites"}
    
    def view_all_favorites(self):
        """
        Get all favorite restaurants.
        
        Returns:
            list: List of dictionaries containing favorite restaurant details.
        """
        return [
            {"id": rid, **details}
            for rid, details in self.favorite_details.items()
        ]
    
    def is_favorite(self, restaurant_id):
        """
        Check if a restaurant is in favorites.
        
        Args:
            restaurant_id (str): ID of the restaurant to check.
        
        Returns:
            bool: True if restaurant is in favorites, False otherwise.
        """
        return restaurant_id in self.favorites
    
    def get_favorites_count(self):
        """
        Get the total number of favorite restaurants.
        
        Returns:
            int: Count of favorite restaurants.
        """
        return len(self.favorites)
    
    def clear_all_favorites(self):
        """
        Remove all favorites.
        
        Returns:
            dict: Success status and message.
        """
        count = len(self.favorites)
        self.favorites.clear()
        self.favorite_details.clear()
        return {"success": True, "message": f"Cleared {count} favorites"}


# Unit Tests for FavoritesManager
class TestFavoritesManager(unittest.TestCase):
    """Unit tests for the FavoritesManager class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.manager = FavoritesManager()
    
    def test_create_favorites_manager(self):
        """Test that FavoritesManager initializes with empty favorites."""
        self.assertIsInstance(self.manager, FavoritesManager)
        self.assertEqual(len(self.manager.favorites), 0)
        self.assertEqual(len(self.manager.favorite_details), 0)
    
    def test_add_favorite_restaurant(self):
        """Test successfully adding a restaurant to favorites."""
        result = self.manager.add_favorite("R001", "Italian Bistro", "Italian", "Downtown")
        
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Restaurant added to favorites")
        self.assertEqual(len(self.manager.favorites), 1)
        self.assertIn("R001", self.manager.favorites)
    
    def test_add_duplicate_favorite(self):
        """Test that adding duplicate favorite is prevented."""
        self.manager.add_favorite("R001", "Italian Bistro", "Italian", "Downtown")
        result = self.manager.add_favorite("R001", "Italian Bistro", "Italian", "Downtown")
        
        self.assertFalse(result['success'])
        self.assertIn("already in favorites", result['message'])
        self.assertEqual(len(self.manager.favorites), 1)
    
    def test_add_favorite_empty_id(self):
        """Test that empty restaurant ID is rejected."""
        result = self.manager.add_favorite("", "Restaurant", "Italian", "Downtown")
        
        self.assertFalse(result['success'])
        self.assertIn("cannot be empty", result['message'])
    
    def test_remove_favorite(self):
        """Test successfully removing a restaurant from favorites."""
        self.manager.add_favorite("R001", "Italian Bistro", "Italian", "Downtown")
        result = self.manager.remove_favorite("R001")
        
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Restaurant removed from favorites")
        self.assertEqual(len(self.manager.favorites), 0)
    
    def test_remove_non_existent_favorite(self):
        """Test removing a non-existent favorite returns error."""
        result = self.manager.remove_favorite("R999")
        
        self.assertFalse(result['success'])
        self.assertIn("not in favorites", result['message'])
    
    def test_view_all_favorites_empty(self):
        """Test viewing favorites when none exist."""
        favorites = self.manager.view_all_favorites()
        
        self.assertIsInstance(favorites, list)
        self.assertEqual(len(favorites), 0)
    
    def test_view_all_favorites_with_data(self):
        """Test viewing favorites when multiple exist."""
        self.manager.add_favorite("R001", "Italian Bistro", "Italian", "Downtown")
        self.manager.add_favorite("R002", "Sushi House", "Japanese", "Midtown")
        
        favorites = self.manager.view_all_favorites()
        
        self.assertEqual(len(favorites), 2)
        self.assertTrue(any(f['name'] == "Italian Bistro" for f in favorites))
        self.assertTrue(any(f['name'] == "Sushi House" for f in favorites))
    
    def test_is_favorite_true(self):
        """Test checking if a restaurant is in favorites (positive case)."""
        self.manager.add_favorite("R001", "Italian Bistro", "Italian", "Downtown")
        
        self.assertTrue(self.manager.is_favorite("R001"))
    
    def test_is_favorite_false(self):
        """Test checking if a restaurant is in favorites (negative case)."""
        self.assertFalse(self.manager.is_favorite("R999"))
    
    def test_get_favorites_count(self):
        """Test getting correct count of favorites."""
        self.assertEqual(self.manager.get_favorites_count(), 0)
        
        self.manager.add_favorite("R001", "Italian Bistro", "Italian", "Downtown")
        self.assertEqual(self.manager.get_favorites_count(), 1)
        
        self.manager.add_favorite("R002", "Sushi House", "Japanese", "Midtown")
        self.assertEqual(self.manager.get_favorites_count(), 2)
    
    def test_clear_all_favorites(self):
        """Test clearing all favorites."""
        self.manager.add_favorite("R001", "Italian Bistro", "Italian", "Downtown")
        self.manager.add_favorite("R002", "Sushi House", "Japanese", "Midtown")
        
        result = self.manager.clear_all_favorites()
        
        self.assertTrue(result['success'])
        self.assertIn("Cleared 2 favorites", result['message'])
        self.assertEqual(len(self.manager.favorites), 0)


if __name__ == '__main__':
    unittest.main()
