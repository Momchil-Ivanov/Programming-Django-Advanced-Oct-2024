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
        category1 = Category.objects.create(
            name='Unique Category',
            description='Test category',
            image_url='https://example.com/image.jpg',
            author=self.user
        )
        category1.tags.add(self.tag)

        with self.assertRaises(Exception):
            category2 = Category.objects.create(
                name='Unique Category',
                description='Another test category',
                image_url='https://example.com/image2.jpg',
                author=self.user
            )
            category2.tags.add(self.tag)


class CategoryModelTests(TestCase):

    def test_category_creation(self):
        user = User.objects.create_user(username='testuser', password='testpassword')

        category = Category.objects.create(
            name="Test Category",
            description="A category for testing.",
            image_url="https://example.com/image.jpg",
            author=user
        )

        self.assertEqual(Category.objects.count(), 1)
        self.assertEqual(category.name, "Test Category")
        self.assertEqual(category.author, user)
