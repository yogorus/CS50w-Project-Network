from django.test import TestCase, Client
from django.urls import reverse

from .models import User, Post, Like

# Create your tests here.
class NetworkTest(TestCase):
    
    def setUp(self):
        user_1 = User.objects.create(username='foo', email='foo@foo.com', password='foo')
        user_2 = User.objects.create(username='bar', email='bar@foo.com', password='bar')

        post_1 = Post.objects.create(author=user_1, body='foo')
        post_2 = Post.objects.create(author=user_1, body='bar')
        post_3 = Post.objects.create(author=user_2, body='')

        like_1 = Like.objects.create(liker=user_1, post=post_1)
        like_2 = Like.objects.create(liker=user_2, post=post_1)
        like_3 = Like.objects.create(liker=user_2, post=post_2)

        user_1.followers.add(user_2)

    def test_likes(self):
        """Test likes count"""
        p1 = Post.objects.filter(id=1).first()
        p2 = Post.objects.filter(id=2).first()
        p3 = Post.objects.filter(id=3).first()
        

        self.assertEqual(p1.likes.count(), 2)
        self.assertEqual(p2.likes.count(), 1)
        self.assertEqual(p3.likes.count(), 0)

    def test_post(self):
        """Test post validation"""
        post_2 = Post.objects.filter(id=2).first()
        post_3 = Post.objects.filter(id=3).first()
        
        self.assertTrue(post_2.is_valid())
        self.assertFalse(post_3.is_valid())
    
    def test_pages(self):
        """Test page render"""

        # Set up client
        c = Client()
        
        # Get response
        url_1 = reverse('posts', kwargs={'section': 'all'})
        response_1 = c.get(url_1)

        url_2 = reverse('posts', kwargs={'section': f'{User.objects.get(pk=1).username}'})
        response_2 = c.get(url_2)

        url_3 = reverse('posts', kwargs={'section': 'baz'})
        response_3 = c.get(url_3)
        
        self.assertEqual(response_1.status_code, 200)
        self.assertEqual(response_2.status_code, 200)
        self.assertEqual(response_3.status_code, 404)
    
    
    def test_follow(self):
        """Test follow"""
        u1 = User.objects.get(pk=1)
        u2 = User.objects.get(pk=2)
        
        self.assertEqual(u1.followers.count(), 1)
        self.assertEqual(u2.following.count(), 1)
        self.assertEqual(u2.followers.count(), 0)
        
        