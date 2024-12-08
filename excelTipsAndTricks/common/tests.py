from django.test import TestCase
from django.contrib.auth.models import User
from excelTipsAndTricks.tips.models import Tip  # Import Tip model from your 'tips' app
from excelTipsAndTricks.common.models import Comment, LikeDislike

class CommentModelTests(TestCase):
    def setUp(self):
        # Create a user and a tip for the comment
        self.user = User.objects.create_user(username='testuser', password='password')
        self.tip = Tip.objects.create(
            title='Test Tip',
            content='This is a test tip.',
            author=self.user,
        )

    def test_create_comment(self):
        # Create a comment for the tip
        comment = Comment.objects.create(
            tip=self.tip,
            author=self.user,
            content='This is a test comment.',
        )

        # Check if the comment is correctly saved in the database
        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(comment.tip, self.tip)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, 'This is a test comment.')

    def test_comment_string_representation(self):
        # Create a comment and check its string representation
        comment = Comment.objects.create(
            tip=self.tip,
            author=self.user,
            content='Test comment for string representation.',
        )

        self.assertEqual(str(comment), f"Comment by {self.user.username} on {self.tip.title}")


class LikeDislikeModelTests(TestCase):
    def setUp(self):
        # Create a user and a tip for the like/dislike
        self.user = User.objects.create_user(username='testuser', password='password')
        self.tip = Tip.objects.create(
            title='Test Tip',
            content='This is a test tip.',
            author=self.user,
        )

    def test_create_like_dislike(self):
        # Create a LikeDislike instance (like)
        like = LikeDislike.objects.create(
            user=self.user,
            tip=self.tip,
            action=LikeDislike.LIKE,
        )

        # Check if the like/dislike is correctly saved in the database
        self.assertEqual(LikeDislike.objects.count(), 1)
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.tip, self.tip)
        self.assertEqual(like.action, LikeDislike.LIKE)

    def test_create_dislike(self):
        # Create a LikeDislike instance (dislike)
        dislike = LikeDislike.objects.create(
            user=self.user,
            tip=self.tip,
            action=LikeDislike.DISLIKE,
        )

        # Check if the dislike is correctly saved in the database
        self.assertEqual(LikeDislike.objects.count(), 1)
        self.assertEqual(dislike.user, self.user)
        self.assertEqual(dislike.tip, self.tip)
        self.assertEqual(dislike.action, LikeDislike.DISLIKE)

    def test_unique_together_constraint(self):
        # Create a like for a user and tip
        LikeDislike.objects.create(
            user=self.user,
            tip=self.tip,
            action=LikeDislike.LIKE,
        )

        # Try to create another like for the same user and tip, expecting a unique constraint violation
        with self.assertRaises(Exception):
            LikeDislike.objects.create(
                user=self.user,
                tip=self.tip,
                action=LikeDislike.LIKE,
            )