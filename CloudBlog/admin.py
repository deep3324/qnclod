from django.contrib import admin
from CloudBlog.models import Newsletter, Contact, Badge, Blog, BlogComment

admin.site.register(Newsletter)
admin.site.register(Contact)
admin.site.register(Badge)
admin.site.register(BlogComment)

@admin.register(Blog)
class BlogAdmin(admin.ModelAdmin):
    class Media:
        js= ('js/tiny.js',)
