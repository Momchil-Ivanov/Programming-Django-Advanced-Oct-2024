from django.test import TestCase
from excelTipsAndTricks.tags.models import Tag
from excelTipsAndTricks.tags.forms import TagForm


class TagModelTests(TestCase):
    def test_tag_name_is_lowercase_on_save(self):
        tag = Tag(name='TestTag')
        tag.save()

        tag_from_db = Tag.objects.get(id=tag.id)
        self.assertEqual(tag_from_db.name, 'testtag')


class TagFormTests(TestCase):
    def test_tag_form_name_validation(self):
        form = TagForm(data={'name': 'ValidTag'})
        self.assertTrue(form.is_valid())

        # Invalid tag name (empty)
        form = TagForm(data={'name': ''})
        self.assertFalse(form.is_valid())
        self.assertIn('This field is required.', form.errors['name'])

        # Invalid tag name (too long)
        form = TagForm(data={'name': 'A' * 51})
        self.assertFalse(form.is_valid())
        self.assertIn('Ensure this value has at most 50 characters (it has 51).', form.errors['name'])
