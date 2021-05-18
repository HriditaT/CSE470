import secrets
from django.shortcuts import render, redirect
from django.views.generic import TemplateView,ListView,DetailView,View,CreateView,UpdateView,DeleteView
from courses.models import category,Lesson,course,teacherReq,Post
from django.shortcuts import render, get_object_or_404,redirect
from django.contrib.auth.mixins import LoginRequiredMixin,UserPassesTestMixin
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import categoryForm, courseForm, LessonForm,profileUpdateForm, userUpdateForm, PostForm
from django.utils import timezone
from django.urls import reverse_lazy
from courses.models import Profile as Pro
from django.contrib.auth.models import User
from django.core.mail import send_mail
from django.core.mail import EmailMessage
# Create your views here.


class HomeView(TemplateView):
    template_name = 'index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        cat = category.objects.all()
        context['category'] = cat
        return context

class AboutView(TemplateView):
    template_name = 'about.html'


class ContactView(TemplateView):
    template_name = 'contact.html'



def CourseListView(request, category):
    courses = course.objects.filter(category=category)
    context = {
        'courses':courses
    }
    return render(request, 'courses/course_list.html', context)



class CourseDetailView(DetailView):
    context_object_name = 'course'
    template_name = 'courses/course_detail.html'
    model = course



class LessonDetailView(View,LoginRequiredMixin):
    def get(self, request, course_slug, lesson_slug, *args, **kwargs):
        course = get_object_or_404(course, slug=course_slug)
        lesson = get_object_or_404(Lesson, slug=lesson_slug)
        context = {'lesson': lesson}
        return render(request, "courses/lesson_detail.html", context)


@login_required
def SearchView(request):
    if request.method == 'POST':
        sWord = request.POST.get('search')
        results = Lesson.objects.filter(title__contains=sWord)
        context = {
            'results':results
        }
        return render(request, 'courses/search_result.html', context)


@login_required
def create_cat(request):
    if not request.user.profile.is_teacher == True:
        messages.error(request, f'You do not have teacher access')
        return redirect('courses:home')
    if request.method == 'POST':
        form = categoryForm(data=request.POST, files=request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, f'Category Created')
            return redirect('courses:home')
    else:
        form = categoryForm()
    context = {
        'form':form
    }
    return render(request, 'courses/create_cat.html', context)


@login_required
def create_course(request):
    if not request.user.profile.is_teacher == True:
        messages.error(request, f'You do not have teacher access')
        return redirect('courses:home')
    if request.method == 'POST':
        form = courseForm(request.POST)
        if form.is_valid():
            form.save()
            category = form.cleaned_data['category']
            slug = category.id
            messages.success(request, f'Course Created')
            return redirect('/courses/' + str(slug))
    else:
        form = courseForm(initial={'creator':request.user.id, 'slug':secrets.token_hex(nbytes=16)})
    context = {
        'form':form
    }
    return render(request, 'courses/create_course.html', context)


@login_required
def create_lesson(request):
    if not request.user.profile.is_teacher == True:
        messages.error(request, f'You do not have teacher access')
        return redirect('courses:home')
    if request.method == 'POST':
        form = LessonForm(request.POST)
        if form.is_valid():
            form.save()
            course = form.cleaned_data['course']
            slug = lesson.slug
            messages.success(request, f'Lesson Created')
            return redirect('/courses/' + str(slug) )
    else:
        form = LessonForm(initial={'slug':secrets.token_hex(nbytes=16)})
    context = {
        'form':form
    }
    return render(request, 'courses/create_lesson.html', context)


def view_404(request, exception):
    return render(request, '404.html')

def view_403(request, exception):
    return render(request, '403.html')

def view_500(request):
    return render(request, '500.html')


@login_required
def Profile(request):
    if request.method == 'POST':
        u_form = userUpdateForm(request.POST,instance=request.user)
        p_form = profileUpdateForm(request.POST,request.FILES,instance=request.user.profile)
        if u_form.is_valid() and p_form.is_valid():
            u_form.save()
            p_form.save()
            messages.success(request, 'Your account has been successfully updated!')
            return redirect('courses:profile')
    else:
        u_form = userUpdateForm(instance=request.user)
        p_form = profileUpdateForm(instance=request.user.profile)

    context= {
        'u_form':u_form,
        'p_form':p_form
    }
    return render(request,'profile/profile.html',context)

@login_required
def teacherReq(request):
    if request.method == 'POST':
        u= request.user
        b= ""
        cprofile = Profile(instance= request,user=u,bio=b)
        cprofile.save()
        tname = request.POST.get('name')
        temail = request.POST.get('e-mail')
        tnumber = request.POST.get('phone')
        prof = request.user.profile
        treq = teacherReq(profile=prof, name=tname, email=temail, number=tnumber)
        treq.save()
        prof_id = prof.id
        Pro.objects.filter(id=prof_id).update(is_teacher=True)

        message = 'Your request for a teacher account has been accepted! Now you can go back to Knowledge and upload courses and lectures. Good Luck!'
        send_mail(
            'The request was accepted.',
            message,
            'knowledge@no-reply.com',
            [email],
            fail_silently=False,
        )
        send_mail(
            'Knowledge',
            'Someone applied for a teacher account. Me info: ' + tname + ' , ' + temail + ' , ' + tnumber + ' , ' + str(prof) + '.',
            'knowledge@no-reply.com',
            ['hridita1998@gmail.com'],
            fail_silently=False,
        )
        messages.info(request, f'The request was sent successfully, you will be notified by email.')
        return redirect('courses:home')



class PostListView(ListView):
    context_object_name = 'posts'
    template_name = 'blog/post_list.html'
    ordering = ['-created_date']
    model = Post



class PostDetailView(DetailView):
    context_object_name = 'post'
    template_name = 'blog/post_detail.html'
    model = Post

@login_required
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        text = request.POST.get('text')
        postim = Post(title=title, text=text, author=request.user)
        postim.save()
        messages.success(request, f'Post created successfully.')
        return redirect('courses:post_list')
    return render(request, 'blog/create_post.html')
    
@login_required
def delete_post(request, id):
    Post(id = id).delete()
    return redirect('courses:post_list')
