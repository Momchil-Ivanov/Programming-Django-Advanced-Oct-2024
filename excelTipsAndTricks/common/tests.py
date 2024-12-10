from django.test import TestCase
from django.contrib.auth.models import User
from excelTipsAndTricks.tips.models import Tip
from excelTipsAndTricks.common.models import Comment, LikeDislike


class CommentModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.tip = Tip.objects.create(
            title='Test Tip',
            content='This is a test tip.',
            author=self.user,
        )

    def test_create_comment(self):
        comment = Comment.objects.create(
            tip=self.tip,
            author=self.user,
            content='This is a test comment.',
        )

        self.assertEqual(Comment.objects.count(), 1)
        self.assertEqual(comment.tip, self.tip)
        self.assertEqual(comment.author, self.user)
        self.assertEqual(comment.content, 'This is a test comment.')

    def test_comment_string_representation(self):
        comment = Comment.objects.create(
            tip=self.tip,
            author=self.user,
            content='Test comment for string representation.',
        )

        self.assertEqual(str(comment), f"Comment by {self.user.username} on {self.tip.title}")


class LikeDislikeModelTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='password')
        self.tip = Tip.objects.create(
            title='Test Tip',
            content='This is a test tip.',
            author=self.user,
        )

    def test_create_like_dislike(self):
        like = LikeDislike.objects.create(
            user=self.user,
            tip=self.tip,
            action=LikeDislike.LIKE,
        )

        self.assertEqual(LikeDislike.objects.count(), 1)
        self.assertEqual(like.user, self.user)
        self.assertEqual(like.tip, self.tip)
        self.assertEqual(like.action, LikeDislike.LIKE)

    def test_create_dislike(self):
        dislike = LikeDislike.objects.create(
            user=self.user,
            tip=self.tip,
            action=LikeDislike.DISLIKE,
        )

        self.assertEqual(LikeDislike.objects.count(), 1)
        self.assertEqual(dislike.user, self.user)
        self.assertEqual(dislike.tip, self.tip)
        self.assertEqual(dislike.action, LikeDislike.DISLIKE)

    def test_unique_together_constraint(self):
        LikeDislike.objects.create(
            user=self.user,
            tip=self.tip,
            action=LikeDislike.LIKE,
        )

        with self.assertRaises(Exception):
            LikeDislike.objects.create(
                user=self.user,
                tip=self.tip,
                action=LikeDislike.LIKE,
            )
