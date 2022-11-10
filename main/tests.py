from django.test import TestCase, Client
from django.urls import reverse
from .models import *
# Create your tests here.

class URLTests(TestCase):
    def test_home(self):
        resp = self.client.get('/')
        self.assertEqual(resp.status_code, 200)
    
    def test_tags(self):
        resp = self.client.get('/new-tags')
        self.assertEqual(resp.status_code, 200)

class CommentAddTest(TestCase):
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user_1 = User.objects.create_user(username='testuser_1', password='12345')
        user_2 = User.objects.create_user(username='testuser_2', password='12345')
        article = Article.objects.create(title='TitleTest', author=user_1, text="text text")
        Comment.objects.create(article=article, author=user_1, text='comment')
        Comment.objects.create(article=article, author=user_2, text='comment')

    def TestComments(self):
        article = Article.objects.get(id=1)
        comments = article.comments
        self.assertEqual(len(comments), 2)

    def delete_comment(self):
        user_1 = User.objects.get(id=1)
        comment = Comment.objects.get(author=user_1)
        comment.delete()

class ArticleModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Set up non-modified objects used by all test methods
        user = User.objects.create_user(username='testuser', password='12345')
        Article.objects.create(title='TitleTest', author=user, text="text text")
    
    def test_title_label(self):
        article = Article.objects.get(id=1)
        field_label = article.title
        self.assertEqual(field_label, 'TitleTest')
    
    def test_title_max_lengthl(self):
        article = Article.objects.get(id=1)
        max_length = article._meta.get_field('title').max_length
        self.assertEqual(max_length, 100)
    
    def test_author_label(self):
        article = Article.objects.get(id=1)
        field_label = article.author.username
        self.assertEqual(field_label, 'testuser')