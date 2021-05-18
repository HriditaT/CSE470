from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from django.utils import timezone
from PIL import Image
# Create your models here.

class Profile(models.Model):
    user = models.OneToOneField(User,on_delete=models.CASCADE)
    bio = models.CharField(max_length=200, blank=True, null=True,default=' ')
    profile_pic = models.ImageField(default='default.png', upload_to = 'profile_pics')
    is_teacher = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username + ' Profile'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        img = Image.open(self.profile_pic.path)
        if img.height >100 or img.width>100:
            output_size = (200,200)
            img.thumbnail(output_size)
            img.save(self.profile_pic.path)


class teacherReq(models.Model):
    profile = models.ForeignKey(Profile, on_delete=models.CASCADE)
    name = models.CharField(max_length=50)
    email = models.EmailField(max_length=254)
    number = models.CharField(max_length=15)


    def __str__(self):
        return self.profile.user.username


class category(models.Model):
    title = models.CharField(max_length=150)
    description = models.TextField(max_length= 200, null=True)
    image = models.ImageField(upload_to='cat_images', default='cat_images/default.jpg')

    def __str__(self):
        return '{}'.format(self.title)

class course(models.Model):
    creator = models.ForeignKey(User,on_delete = models.CASCADE)
    slug = models.SlugField()
    title = models.CharField(max_length=30)
    category = models.ForeignKey(category,on_delete=models.CASCADE)
    description = models.TextField(max_length=400)
    create_date = models.DateTimeField(auto_now=True)
    price = models.IntegerField()
    image = models.ImageField(upload_to='course_images', default='default.jpg')

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:course_detail", kwargs={"slug": self.slug})

    @property
    def lessons(self):
        return self.lesson_set.all().order_by('position')



class Lesson(models.Model):
    slug = models.SlugField()
    title = models.CharField(max_length=30)
    course = models.ForeignKey(course,on_delete=models.CASCADE)
    video_id = models.CharField(max_length=11)
    position = models.IntegerField()

    def __str__(self):
        return self.title

    def get_absolute_url(self):
        return reverse("courses:lesson_detail", kwargs={"course_slug": self.course.slug,'lesson_slug':self.slug})


class Post(models.Model):
    author = models.ForeignKey(User,on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    text = models.TextField()
    created_date = models.DateTimeField(default=timezone.now)

    def get_absolute_url(self):
        return reverse("courses:blog_detail", kwargs={"pk": self.pk})

    def __str__(self):
        return self.title
