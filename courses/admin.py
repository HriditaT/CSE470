from django.contrib import admin
from courses.models import category,Lesson,course,Post,Profile,teacherReq
# Register your models here.

admin.site.register(course)
admin.site.register(Lesson)
admin.site.register(category)
admin.site.register(Post)
admin.site.register(Profile)
admin.site.register(teacherReq)
