from django.test import TestCase

from .models import User, Post, Like

# Create your tests here.
class NetworkTest(TestCase):
    
    def setUp(self):
        user_1 = User.objects.create(username='foo', email='foo@foo.com', password='foo')
        user_2 = User.objects.create(username='bar', email='bar@foo.com', password='bar')

        post_1 = Post.objects.create(author=user_1, body='foo')
        post_2 = Post.objects.create(author=user_1, body='bar')
        post_3 = Post.objects.create(author=user_2, body='foo')

        like_1 = Like.objects.create(liker=user_1, post=post_1)
        like_2 = Like.objects.create(liker=user_2, post=post_1)
        like_3 = Like.objects.create(liker=user_2, post=post_2)

    def test_likes(self):
        """Test likes count"""
        u1 = User.objects.filter(username='foo').first()
        u2 = User.objects.filter(username='bar').first()
        
        p1 = Post.objects.filter(id=1).first()
        p2 = Post.objects.filter(id=2).first()
        p3 = Post.objects.filter(id=3).first()
        

        self.assertEqual(p1.likes.count(), 2)
        self.assertEqual(p2.likes.count(), 1)
        self.assertEqual(p3.likes.count(), 0)