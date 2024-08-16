from django.db import models

# Create your models here.

class timeStampModel(models.Model):
    created_at=models.DateTimeField(auto_now_add=True)
    updated_at=models.DateTimeField(auto_now=True)

    class Meta:
        abstract=True #don't create table in Database

        

class Category(timeStampModel):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Tag(timeStampModel):
    name=models.CharField(max_length=100)

    def __str__(self):
        return self.name
    
class Post(timeStampModel):
    sTATUS_CHOICES=[
        ("active", "Actuve"),
        ("in_active", "Inactive"),
    ]
    title=models.CharField(max_length=200)
    content=models.TextField()
    featured_image=models.ImageField(upload_to="post_images/%Y/%m/%d", blank=False )
    author=models.ForeignKey("auth.User", on_delete=models.CASCADE)
    status=models.CharField(max_length=20, choices=sTATUS_CHOICES, default="active")
    view_count=models.PositiveIntegerField(default=0)
    published_at=models.DateTimeField(null=True, blank=True)
    category=models.ForeignKey(Category, on_delete=models.CASCADE)
    tag=models.ManyToManyField(Tag)

    def __str__(self):
        return self.title
    

