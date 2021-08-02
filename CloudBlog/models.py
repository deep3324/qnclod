# from CloudBlog.views import comment
from django.db import models
from django.utils.safestring import mark_safe 
from taggit.managers import TaggableManager 
# Create your models here.

class Newsletter(models.Model):
    name= models.CharField(max_length=100, default="")
    email=models.EmailField(max_length=254, default="")
    date=models.DateField()
    def __str__(self):
        return self.name

class Contact(models.Model):
    name= models.CharField(max_length=100, default="")
    email=models.EmailField(max_length=254, default="")
    subject= models.TextField()
    message= models.TextField()
    date=models.DateField()
    def __str__(self):
        return self.name

class Badge(models.Model):
    name= models.CharField(max_length=100, default="")
    icon=models.ImageField(upload_to='icon', default="")
    date=models.DateField()
    def __str__(self):
        return self.name

class Blog(models.Model):
    sno=models.AutoField(primary_key=True)
    title= models.CharField(max_length=300, default="")
    slug=models.SlugField(max_length=300)
    user=models.CharField(max_length=100, default="")
    image=models.ImageField(upload_to='BlogImage', default="")
    content= models.TextField()
    tags = TaggableManager()
    date=models.DateField()
    def display_my_safefield(self): 
        return mark_safe(self.content)
    def __str__(self):
        return self.title

class BlogComment(models.Model):
    sno= models.AutoField(primary_key=True)
    post=models.ForeignKey(Blog, related_name="comments", on_delete=models.CASCADE)
    name = models.CharField(max_length=150, default="")
    email = models.EmailField(max_length=150, default="")
    comment = models.TextField()
    website = models.URLField(max_length=200, default="")
    parent = models.ForeignKey('self',on_delete=models.CASCADE, null=True )
    timestamp= models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.post.title +" : "+ self.name