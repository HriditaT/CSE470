from django import forms
from django.contrib.auth.models import User
from .models import category, course, Lesson,Post,Profile



class categoryForm(forms.ModelForm):
    class Meta:
        model = category
        fields = '__all__'

class courseForm(forms.ModelForm):
    class Meta:
        model = course
        fields = ['creator','slug', 'title', 'category', 'description','price','image']
        labels = {
            'title':'Course Title'
        }
        widgets = {'creator': forms.HiddenInput(), 'slug': forms.HiddenInput()}


class LessonForm(forms.ModelForm):
    class Meta:
        model = Lesson
        fields = ['slug','title', 'course', 'video_id', 'position', ]
        widgets = {
            'slug': forms.HiddenInput()
        }

class PostForm(forms.ModelForm):

    class Meta:
        model= Post
        fields = ('title','text')

    def save_form(self, request, instance, form, change):
        user = request.user
        instance = form.save(commit=False)
        if not change or not instance.author:
            instance.author = user
        instance.modified_by = user
        instance.save()
        form.save_m2m()
        return instance

class userUpdateForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email']


class profileUpdateForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields =['bio','profile_pic']
