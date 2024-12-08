from django.db.utils import IntegrityError
from django.test import TestCase
from django.contrib.auth.models import User
from excelTipsAndTricks.categories.models import Category
from excelTipsAndTricks.tags.models import Tag
from .models import Tip

class TipModelTests(TestCase):
    def setUp(self):
        # Create a user
        self.user = User.objects.create_user(username='testuser', password='password')

        # Create a category with an author
        self.category = Category.objects.create(name='Excel Tips', author=self.user)

        # Create a tag
        self.tag = Tag.objects.create(name='Basic Excel')

    def test_create_tip(self):
        # Create a new Tip
        tip = Tip.objects.create(
            title='How to create a Pivot Table',
            content='This tip explains how to create a Pivot Table in Excel.',
            author=self.user
        )

        # Add the category and tag
        tip.categories.add(self.category)
        tip.tags.add(self.tag)

        # Ensure the tip is correctly saved
        self.assertEqual(tip.title, 'How to create a Pivot Table')
        self.assertEqual(tip.content, 'This tip explains how to create a Pivot Table in Excel.')
        self.assertEqual(tip.author, self.user)
        self.assertIn(self.category, tip.categories.all())
        self.assertIn(self.tag, tip.tags.all())

    def test_title_uniqueness(self):
        # Create the first Tip with an author
        Tip.objects.create(title="Unique Title", content="Test content", author=self.user)

        # Try to create a second Tip with the same title and the same author
        with self.assertRaises(IntegrityError):
            Tip.objects.create(title="Unique Title", content="Another content", author=self.user)
