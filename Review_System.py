"""
Review System Module - Implemented using TDD methodology
This module allows users to rate and review restaurants.
"""

import unittest
from datetime import datetime


class ReviewSystem:
    """
    Manages restaurant ratings and reviews.
    
    Attributes:
        reviews (dict): Dictionary mapping restaurant IDs to lists of reviews.
    """
    
    def __init__(self):
        """Initialize ReviewSystem with empty reviews."""
        self.reviews = {}
    
    def add_review(self, restaurant_id, user_id, rating, review_text):
        """
        Add a review for a restaurant.
        
        Args:
            restaurant_id (str): ID of the restaurant being reviewed.
            user_id (str): ID of the user submitting the review.
            rating (int): Rating from 1 to 5 stars.
            review_text (str): The review text.
        
        Returns:
            dict: Success status and message.
        """
        # Validate rating
        if not isinstance(rating, int) or not (1 <= rating <= 5):
            return {"success": False, "message": "Rating must be between 1 and 5"}
        
        # Validate review text
        if not review_text or not review_text.strip():
            return {"success": False, "message": "Review text cannot be empty"}
        
        # Validate IDs
        if not restaurant_id or not user_id:
            return {"success": False, "message": "Restaurant ID and User ID are required"}
        
        # Initialize restaurant reviews if not exists
        if restaurant_id not in self.reviews:
            self.reviews[restaurant_id] = []
        
        # Check if user already reviewed this restaurant
        for review in self.reviews[restaurant_id]:
            if review['user_id'] == user_id:
                return {"success": False, "message": "User has already reviewed this restaurant"}
        
        # Add the review
        review = {
            "user_id": user_id,
            "rating": rating,
            "review_text": review_text.strip(),
            "timestamp": datetime.now(),
            "edited": False
        }
        
        self.reviews[restaurant_id].append(review)
        
        return {"success": True, "message": "Review added successfully"}
    
    def get_restaurant_reviews(self, restaurant_id):
        """
        Get all reviews for a specific restaurant.
        
        Args:
            restaurant_id (str): ID of the restaurant.
        
        Returns:
            list: List of all reviews for the restaurant.
        """
        return self.reviews.get(restaurant_id, []).copy()
    
    def calculate_average_rating(self, restaurant_id):
        """
        Calculate the average rating for a restaurant.
        
        Args:
            restaurant_id (str): ID of the restaurant.
        
        Returns:
            float: Average rating, or 0.0 if no reviews exist.
        """
        restaurant_reviews = self.reviews.get(restaurant_id, [])
        
        if not restaurant_reviews:
            return 0.0
        
        total = sum(review['rating'] for review in restaurant_reviews)
        return round(total / len(restaurant_reviews), 2)
    
    def edit_review(self, restaurant_id, user_id, new_rating=None, new_text=None):
        """
        Edit an existing review by the same user.
        
        Args:
            restaurant_id (str): ID of the restaurant.
            user_id (str): ID of the user editing the review.
            new_rating (int, optional): New rating value.
            new_text (str, optional): New review text.
        
        Returns:
            dict: Success status and message.
        """
        if restaurant_id not in self.reviews:
            return {"success": False, "message": "Restaurant has no reviews"}
        
        # Find the user's review
        user_review = None
        for review in self.reviews[restaurant_id]:
            if review['user_id'] == user_id:
                user_review = review
                break
        
        if not user_review:
            return {"success": False, "message": "User has not reviewed this restaurant"}
        
        # Update rating if provided
        if new_rating is not None:
            if not isinstance(new_rating, int) or not (1 <= new_rating <= 5):
                return {"success": False, "message": "Rating must be between 1 and 5"}
            user_review['rating'] = new_rating
        
        # Update text if provided
        if new_text is not None:
            if not new_text or not new_text.strip():
                return {"success": False, "message": "Review text cannot be empty"}
            user_review['review_text'] = new_text.strip()
        
        user_review['edited'] = True
        user_review['last_edited'] = datetime.now()
        
        return {"success": True, "message": "Review updated successfully"}
    
    def get_user_review(self, restaurant_id, user_id):
        """
        Get a specific user's review for a restaurant.
        
        Args:
            restaurant_id (str): ID of the restaurant.
            user_id (str): ID of the user.
        
        Returns:
            dict: The user's review, or None if not found.
        """
        restaurant_reviews = self.reviews.get(restaurant_id, [])
        
        for review in restaurant_reviews:
            if review['user_id'] == user_id:
                return review.copy()
        
        return None
    
    def delete_review(self, restaurant_id, user_id):
        """
        Delete a user's review for a restaurant.
        
        Args:
            restaurant_id (str): ID of the restaurant.
            user_id (str): ID of the user.
        
        Returns:
            dict: Success status and message.
        """
        if restaurant_id not in self.reviews:
            return {"success": False, "message": "Restaurant has no reviews"}
        
        original_count = len(self.reviews[restaurant_id])
        self.reviews[restaurant_id] = [
            r for r in self.reviews[restaurant_id] if r['user_id'] != user_id
        ]
        
        if len(self.reviews[restaurant_id]) == original_count:
            return {"success": False, "message": "Review not found"}
        
        return {"success": True, "message": "Review deleted successfully"}
    
    def get_review_count(self, restaurant_id):
        """
        Get the total number of reviews for a restaurant.
        
        Args:
            restaurant_id (str): ID of the restaurant.
        
        Returns:
            int: Number of reviews.
        """
        return len(self.reviews.get(restaurant_id, []))


# Unit Tests for ReviewSystem
class TestReviewSystem(unittest.TestCase):
    """Unit tests for the ReviewSystem class."""
    
    def setUp(self):
        """Set up test fixtures before each test method."""
        self.review_system = ReviewSystem()
    
    def test_create_review_system(self):
        """Test that ReviewSystem initializes with empty reviews."""
        self.assertIsInstance(self.review_system, ReviewSystem)
        self.assertEqual(len(self.review_system.reviews), 0)
    
    def test_add_review_valid(self):
        """Test successfully adding a valid review."""
        result = self.review_system.add_review("R001", "U001", 5, "Excellent food!")
        
        self.assertTrue(result['success'])
        self.assertEqual(result['message'], "Review added successfully")
        self.assertEqual(len(self.review_system.reviews["R001"]), 1)
    
    def test_add_review_invalid_rating_high(self):
        """Test that rating above 5 is rejected."""
        result = self.review_system.add_review("R001", "U001", 6, "Great food")
        
        self.assertFalse(result['success'])
        self.assertIn("between 1 and 5", result['message'])
    
    def test_add_review_invalid_rating_low(self):
        """Test that rating below 1 is rejected."""
        result = self.review_system.add_review("R001", "U001", 0, "Terrible")
        
        self.assertFalse(result['success'])
        self.assertIn("between 1 and 5", result['message'])
    
    def test_add_review_invalid_rating_type(self):
        """Test that non-integer rating is rejected."""
        result = self.review_system.add_review("R001", "U001", 4.5, "Good")
        
        self.assertFalse(result['success'])
        self.assertIn("between 1 and 5", result['message'])
    
    def test_add_review_empty_text(self):
        """Test that empty review text is rejected."""
        result = self.review_system.add_review("R001", "U001", 4, "")
        
        self.assertFalse(result['success'])
        self.assertIn("cannot be empty", result['message'])
    
    def test_add_review_whitespace_only(self):
        """Test that whitespace-only review text is rejected."""
        result = self.review_system.add_review("R001", "U001", 4, "   ")
        
        self.assertFalse(result['success'])
        self.assertIn("cannot be empty", result['message'])
    
    def test_add_duplicate_review(self):
        """Test that duplicate review by same user is prevented."""
        self.review_system.add_review("R001", "U001", 5, "Great!")
        result = self.review_system.add_review("R001", "U001", 4, "Still good")
        
        self.assertFalse(result['success'])
        self.assertIn("already reviewed", result['message'])
    
    def test_get_restaurant_reviews(self):
        """Test retrieving all reviews for a restaurant."""
        self.review_system.add_review("R001", "U001", 5, "Excellent!")
        self.review_system.add_review("R001", "U002", 4, "Very good")
        
        reviews = self.review_system.get_restaurant_reviews("R001")
        
        self.assertEqual(len(reviews), 2)
        self.assertTrue(any(r['user_id'] == "U001" for r in reviews))
        self.assertTrue(any(r['user_id'] == "U002" for r in reviews))
    
    def test_get_restaurant_reviews_empty(self):
        """Test retrieving reviews for restaurant with no reviews."""
        reviews = self.review_system.get_restaurant_reviews("R999")
        
        self.assertEqual(len(reviews), 0)
        self.assertIsInstance(reviews, list)
    
    def test_calculate_average_rating(self):
        """Test calculating average rating correctly."""
        self.review_system.add_review("R001", "U001", 5, "Excellent!")
        self.review_system.add_review("R001", "U002", 3, "Average")
        self.review_system.add_review("R001", "U003", 4, "Good")
        
        avg = self.review_system.calculate_average_rating("R001")
        
        self.assertEqual(avg, 4.0)  # (5 + 3 + 4) / 3 = 4.0
    
    def test_calculate_average_rating_no_reviews(self):
        """Test average rating for restaurant with no reviews."""
        avg = self.review_system.calculate_average_rating("R999")
        
        self.assertEqual(avg, 0.0)
    
    def test_edit_own_review_rating(self):
        """Test successfully editing own review's rating."""
        self.review_system.add_review("R001", "U001", 4, "Good food")
        result = self.review_system.edit_review("R001", "U001", new_rating=5)
        
        self.assertTrue(result['success'])
        
        review = self.review_system.get_user_review("R001", "U001")
        self.assertEqual(review['rating'], 5)
        self.assertTrue(review['edited'])
    
    def test_edit_own_review_text(self):
        """Test successfully editing own review's text."""
        self.review_system.add_review("R001", "U001", 4, "Good food")
        result = self.review_system.edit_review("R001", "U001", new_text="Excellent food!")
        
        self.assertTrue(result['success'])
        
        review = self.review_system.get_user_review("R001", "U001")
        self.assertEqual(review['review_text'], "Excellent food!")
        self.assertTrue(review['edited'])
    
    def test_edit_other_user_review(self):
        """Test that editing another user's review fails."""
        self.review_system.add_review("R001", "U001", 4, "Good")
        result = self.review_system.edit_review("R001", "U002", new_rating=5)
        
        self.assertFalse(result['success'])
        self.assertIn("has not reviewed", result['message'])
    
    def test_edit_non_existent_review(self):
        """Test editing review for restaurant with no reviews."""
        result = self.review_system.edit_review("R999", "U001", new_rating=5)
        
        self.assertFalse(result['success'])
        self.assertIn("no reviews", result['message'])
    
    def test_get_user_review(self):
        """Test retrieving specific user's review."""
        self.review_system.add_review("R001", "U001", 5, "Great!")
        
        review = self.review_system.get_user_review("R001", "U001")
        
        self.assertIsNotNone(review)
        self.assertEqual(review['user_id'], "U001")
        self.assertEqual(review['rating'], 5)
    
    def test_get_user_review_not_found(self):
        """Test retrieving non-existent user review."""
        review = self.review_system.get_user_review("R001", "U999")
        
        self.assertIsNone(review)
    
    def test_delete_review(self):
        """Test successfully deleting a review."""
        self.review_system.add_review("R001", "U001", 5, "Great!")
        result = self.review_system.delete_review("R001", "U001")
        
        self.assertTrue(result['success'])
        self.assertEqual(self.review_system.get_review_count("R001"), 0)
    
    def test_get_review_count(self):
        """Test getting correct review count."""
        self.assertEqual(self.review_system.get_review_count("R001"), 0)
        
        self.review_system.add_review("R001", "U001", 5, "Great!")
        self.assertEqual(self.review_system.get_review_count("R001"), 1)
        
        self.review_system.add_review("R001", "U002", 4, "Good")
        self.assertEqual(self.review_system.get_review_count("R001"), 2)


if __name__ == '__main__':
    unittest.main()
