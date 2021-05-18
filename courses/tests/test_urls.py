from django.test import SimpleTestCase
from django.urls import reverse,resolve
from courses.views import HomeView,AboutView,ContactView,CourseListView, CourseDetailView,LessonDetailView, SearchView, create_cat, create_course, create_lesson,PostListView,PostDetailView, create_post, delete_post


class Testurls(SimpleTestCase):

    def test_home_urls_is_resolved(self):
        url1 = reverse('courses:home')
        print(resolve(url1))
        self.assertEquals(resolve(url1).func.view_class,HomeView)

    def test_about_urls_is_resolved(self):
        url2 = reverse('courses:about')
        print(resolve(url2))
        self.assertEquals(resolve(url2).func.view_class,AboutView)

    def test_search_result_urls_is_resolved(self):
        url3 = reverse('courses:search_result')
        print(resolve(url3))
        self.assertEquals(resolve(url3).func,SearchView)

    def test_contact_urls_is_resolved(self):
        url4 = reverse('courses:contact')
        print(resolve(url4))
        self.assertEquals(resolve(url4).func.view_class,ContactView)

    def test_post_list_urls_is_resolved(self):
        url5 = reverse('courses:post_list')
        print(resolve(url5))
        self.assertEquals(resolve(url5).func.view_class,PostListView)

    def test_create_post_urls_is_resolved(self):
        url6 = reverse('courses:create_post')
        print(resolve(url6))
        self.assertEquals(resolve(url6).func,create_post)
