from django.contrib import admin

admin.site.site_header="Manoj Kumar Neupane"
# Register your models here.
from newspaper.models import Post, Category, Tag, UserProfile, Comment
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)
admin.site.register(UserProfile)
admin.site.register(Comment)

