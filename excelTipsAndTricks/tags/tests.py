from django.test import TestCase
from excelTipsAndTricks.tags.models import Tag
from excelTipsAndTricks.tags.forms import TagForm

class TagModelTests(TestCase):
    def test_tag_name_is_lowercase_on_save(self):
        # Create a tag with uppercase letters in its name
        tag = Tag(name='TestTag')
        tag.save()

        # Retrieve the tag from the database and check if its name is lowercase
        tag_from_db = Tag.objects.get(id=tag.id)
        self.assertEqual(tag_from_db.name, 'testtag')  # The name should be in lowercase

class TagFormTests(TestCase):
    def test_tag_form_name_validation(self):
        # Valid tag name
        form = TagForm(data={'name': 'ValidTag'})
        self.assertTrue(form.is_valid())  # Form should be valid

        # Invalid tag name (empty)
        form = TagForm(data={'name': ''})
        self.assertFalse(form.is_valid())  # Form should be invalid
        self.assertIn('This field is required.', form.errors['name'])

        # Invalid tag name (too long)
        form = TagForm(data={'name': 'A' * 51})
        self.assertFalse(form.is_valid())  # Form should be invalid
        self.assertIn('Ensure this value has at most 50 characters (it has 51).', form.errors['name'])