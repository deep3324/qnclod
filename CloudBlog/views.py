from django.shortcuts import render
from django.shortcuts import redirect
from django.conf import settings
from taggit.models import Tag
from CloudBlog.models import Blog, BlogComment, Contact, Badge, Newsletter
from datetime import datetime
from django.contrib import messages
from django.core.mail import send_mail
from django.core.paginator import Paginator
from CloudBlog.templatetags import extras

# Create your views here.

# def base(request):
#     return render(re)

def home(request):
    home= Blog.objects.all().order_by('-sno')
    context = {'home': home, 'blog':home}
    visits = int(request.COOKIES.get('visits', '1'))
    reset_last_visit_time = False
    response = render(request,'home.html', context)
    if 'last_visit' in request.COOKIES:
        # Yes it does! Get the cookie's value.
        last_visit = request.COOKIES['last_visit']
        # Cast the value to a Python date/time object.
        last_visit_time = datetime.strptime(last_visit[:-7], "%Y-%m-%d %H:%M:%S")
        # If it's been more than a day since the last visit...
        if (datetime.now() - last_visit_time).days > 0:
            visits = visits + 1
            # ...and flag that the cookie last visit needs to be updated
            reset_last_visit_time = True
    else:
        # Cookie last_visit doesn't exist, so flag that it should be set.
        reset_last_visit_time = True
        context['visits'] = visits
        #Obtain our Response object early so we can add cookie information.
        response = render(request, 'home.html', context)
    if reset_last_visit_time:
        response.set_cookie('last_visit', datetime.now())
        response.set_cookie('visits', visits)
    # Return response back to the user, updating any cookies that need changed.
    return response

def contact(request):
    deta=Blog.objects.all().order_by('-sno')
    context = {"contact_page": "active", 'blog':deta}
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        subject=request.POST.get('subject')
        message=request.POST.get('message')
        body= 'Contact Request: \n\nName: '+ name + '\nEmail: '+ email + '\nSubject: ' +  subject + '\nMessage: '+ message
        contact = Contact(name=name, email=email, subject=subject, message=message, date=datetime.today())
        contact.save()
        messages.success(request, "Your Contact Request has been submitted, We'll Contact you soon")
        send_mail('Contact Requests',body,settings.EMAIL_HOST_USER,['navneetbhardwaj935@gmail.com'])
    return render(request,'contact.html', context)

def about(request):
    deta=Blog.objects.all().order_by('-sno')
    abt= Badge.objects.all()
    context = {"about_page": "active", 'abt': abt, 'blog':deta }
    return render(request,'about.html', context)

def blogs(request):
    blogs = Blog.objects.all().order_by('-sno')
    paginator = Paginator(blogs, 5)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {"blogs_page": "active", 'blog':blogs, 'page_obj': page_obj}
    return render(request,'blogs.html', context)

def comment(request):
    deta=Blog.objects.all().order_by('-sno')
    if request.method == "POST":
        name=request.POST.get('name')
        email=request.POST.get('email')
        website=request.POST.get('website')
        comment=request.POST.get('comment')
        postSno =request.POST.get('postSno')
        post= Blog.objects.get(sno=postSno)
        parentSno= request.POST.get('parentSno')
        if parentSno=="":
            comment=BlogComment(comment= comment, name=name, email=email, website=website, post=post)
            comment.save()
            messages.success(request, "Your comment has been posted successfully")
        else:
            parent= BlogComment.objects.get(sno=parentSno)
            comment=BlogComment(comment= comment, name=name, email=email, website=website, post=post, parent=parent)
            comment.save()
            messages.success(request, "Your reply has been posted successfully")
    return redirect(f"/blogs/{post.slug}", {'blog':deta})

def blog(request, slug):
    post= Blog.objects.filter(slug=slug)
    blog= Blog.objects.all().order_by('-sno')
    comments= BlogComment.objects.filter(post__in=post, parent=None).order_by('-sno')
    replies= BlogComment.objects.filter(post__in=post).exclude(parent=None)
    replyDict={}
    for reply in replies:
        if reply.parent.sno not in replyDict.keys():
            replyDict[reply.parent.sno]=[reply]
        else:
            replyDict[reply.parent.sno].append(reply)
    return render(request,"blog.html",{'blogs':post, 'blog':blog, 'comments':comments, 'replyDict': replyDict})

def cookie(request):
    deta=Blog.objects.all().order_by('-sno')
    return render(request,'cookie.html', {'blog':deta})

def disclaimer(request):
    deta=Blog.objects.all().order_by('-sno')
    return render(request,'disclaimer.html', {'blog':deta})

def privacy(request):
    deta=Blog.objects.all().order_by('-sno')
    return render(request,'privacy.html', {'blog':deta})

def termandconditions(request):
    tagss = Blog.objects.values('tags').distinct()
    deta=Blog.objects.all().order_by('-sno')
    return render(request,'termandconditions.html', {'tagss':tagss, 'blog':deta})

def newsletter(request):
    deta=Blog.objects.all().order_by('-sno')
    if request.method=='POST':
        name=request.POST.get('name')
        email=request.POST.get('email')
        body= 'Hey'+ name + '\n\nThanks for subscribing for newsletter. \n\n Regards:\nQuotes and Cloud'
        newsletter = Newsletter(name=name, email=email, date=datetime.today())
        newsletter.save()
        messages.success(request, "Your Newsletter Request has been submitted, You'll soon receive newsletter")
        send_mail('Newsletter Request Accepted',body,settings.EMAIL_HOST_USER,[email])
    return redirect('/', {'blog':deta})

def search(request):
    deta=Blog.objects.all().order_by('-sno')
    if request.method=='GET':
        search = request.GET.get('search')
        post = Blog.objects.filter(title__icontains=search)
        return render(request, 'search.html', {'post':post, 'blog':deta})

def tagged(request,id):
    deta=Blog.objects.all().order_by('-sno')
    tag =  Tag.objects.filter(pk=id)
    post_list = Blog.objects.all().filter(tags__in=tag).order_by('-sno')
    return render(request, 'tagged.html', {'post_list': post_list, 'blog':deta}) 
