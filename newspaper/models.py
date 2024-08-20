from django.db import models


class TimeStampModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        abstract = True  # Don't create table in DB


class Category(TimeStampModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Tag(TimeStampModel):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name


class Post(TimeStampModel):
    STATUS_CHOICES = [
        ("active", "Active"),
        ("in_active", "Inactive"),
    ]
    title = models.CharField(max_length=200)
    content = models.TextField()
    featured_image = models.ImageField(upload_to="post_images/%Y/%m/%d", blank=False)
    author = models.ForeignKey("auth.User", on_delete=models.CASCADE)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="active")
    view_count = models.PositiveBigIntegerField(default=0)
    published_at = models.DateTimeField(null=True, blank=True)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    tag = models.ManyToManyField(Tag)

    def __str__(self):
        return self.title


## 1 - 1 Relationship
# 1 user can have 1 profile => 1
# 1 profile is associated to 1 user  => 1
# OneToOneField() => Can be used in Any Model


## 1 - M Relationship
# 1 user can post M post  => M
# 1 post is associated to only 1 user => 1
# In django use ForeignKey() => Must be used in Many side

# 1 category can have M posts => M
# 1 post is associated to only 1 category => 1

## M - M Relationship
# 1 student can learn from M teachers => M
# 1 teacher can teach M students => M
# ManyToManyField() => Can be used in Any Model

# 1 post can contain M tag => M
# 1 tag can be used in M post => M
