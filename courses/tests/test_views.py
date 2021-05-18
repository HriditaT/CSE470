from django.test import TestCase, Client
from django.urls import reverse
from courses.models import category,Lesson,course,Post
import json
from django.contrib.auth.models import User

class TestViews(TestCase):
    def setUp(self):
        self.client = Client()

    def test_homeview_GET(self):
        response = self.client.get(reverse('courses:home'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'index.html')

    def test_aboutview_GET(self):
        response = self.client.get(reverse('courses:about'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'about.html')

    def test_contactview_GET(self):
        response = self.client.get(reverse('courses:contact'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'contact.html')

    def test_postlistview_GET(self):
        response = self.client.get(reverse('courses:post_list'))
        self.assertEquals(response.status_code,200)
        self.assertTemplateUsed(response,'blog/post_list.html')
        
