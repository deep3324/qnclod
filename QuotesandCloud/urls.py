"""QuotesandCloud URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from CloudBlog import views
from django.conf import settings
from django.conf.urls.static import static

admin.site.site_header = "QuotesandCloud Admin"
admin.site.site_title = "QuotesandCloud Admin Portal"
admin.site.index_title = "Quotes and Cloud"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.home, name="home"),
    # path('base', views.base, name="base"),
    path('contact', views.contact, name="contact"),
    path('about', views.about, name="about"),
    path('blogs', views.blogs, name="blogs"),
    path('blogs/<str:slug>', views.blog, name="blog"),
    path('blog', views.blog, name="blog"),
    path('cookie', views.cookie, name="cookie"),
    path('disclaimer', views.disclaimer, name="disclaimer"),
    path('privacy', views.privacy, name="privacy"),
    path('newsletter', views.newsletter, name="newsletter"),
    path('search', views.search, name="search"),
    path('comment', views.comment, name="comment"),
    path('tagged_post/<int:id>', views.tagged, name="tagged"),
    # path('remove', views.remove, name="remove"),
    path('termandconditions', views.termandconditions, name="termandconditions"),
    
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)