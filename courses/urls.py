from django.urls import path
from django.contrib.auth.decorators import login_required

from courses.views import HomeView,AboutView,ContactView,CourseListView, CourseDetailView,LessonDetailView, SearchView, create_cat, create_course, create_lesson,PostListView,PostDetailView, create_post, delete_post,Profile, teacherReq

app_name = 'courses'

urlpatterns = [
    path('', HomeView.as_view(), name='home'),
    path('about/', AboutView.as_view(), name='about'),
    path('contact/', ContactView.as_view(), name='contact'),
    path('courses/<int:category>', CourseListView, name='course_list'),
    path('courses/<slug>/', login_required(CourseDetailView.as_view()), name='course_detail'),
    path('courses/<course_slug>/<lesson_slug>/', login_required(LessonDetailView.as_view()), name='lesson_detail'),
    path('search/', SearchView, name='search_result'),
    path('create/category', create_cat, name='create_cat'),
    path('create/course', create_course, name='create_course'),
    path('create/lesson', create_lesson, name='create_lesson'),
    path('profile/', Profile, name='profile'),
    path('request/', teacherReq, name='teacherReq'),
    path('blog/',PostListView.as_view(),name='post_list'),
    path('blog/<int:pk>/',PostDetailView.as_view(),name='post_detail'),
    path('blog/create/', create_post, name='create_post'),
    path('blog/<int:id>/delete', delete_post, name='delete_post')


]
