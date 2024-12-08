from django.test import TestCase

from django.test import TestCase
from excelTipsAndTricks.categories.models import Category
from excelTipsAndTricks.tags.models import Tag
from django.contrib.auth.models import User

class CategoryFormTests(TestCase):
    def setUp(self):
        # Create a test user
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create a tag for the category
        self.tag = Tag.objects.create(name='Test Tag')

    def test_category_name_uniqueness(self):
        # Create a category with the test user as the author, and assign the tag to the category
        category1 = Category.objects.create(
            name='Unique Category',
            description='Test category',
            image_url='http://example.com/image.jpg',
            author=self.user  # Assign the author
        )
        category1.tags.add(self.tag)  # Add the tag to the category

        # Try to create a second category with the same name
        with self.assertRaises(Exception):
            category2 = Category.objects.create(
                name='Unique Category',
                description='Another test category',
                image_url='http://example.com/image2.jpg',
                author=self.user  # Assign the author
            )
            category2.tags.add(self.tag)  # Add the same tag to the new category

class CategoryModelTests(TestCase):

    def test_category_creation(self):
        # Create a user to associate with the category
        user = User.objects.create_user(username='testuser', password='testpassword')

        # Create a category
        category = Category.objects.create(
            name="Test Category",
            description="A category for testing.",
            image_url="http://example.com/image.jpg",
            author=user
        )

        # Verify the category was created successfully
        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.author, user)