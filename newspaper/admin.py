from django.contrib import admin

admin.site.site_header="Manoj Kumar Neupane"
# Register your models here.
from newspaper.models import Post, Category, Tag
admin.site.register(Post)
admin.site.register(Category)
admin.site.register(Tag)

