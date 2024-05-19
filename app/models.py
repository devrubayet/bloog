import os
from django.db import models
from ckeditor.fields import RichTextField
from ckeditor_uploader.fields import RichTextUploadingField

from django.contrib.auth.models import AbstractUser
# Create your models here.


class CustomUser(AbstractUser):
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(unique=True, null=True)
    bio = models.TextField(null = True)

    avatar = models.ImageField(upload_to="user_profile/",null=True, default='user_profile/user.jpg')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    
    


class Tag(models.Model):
    name = models.CharField(max_length=50)
    
    def __str__(self):
        return self.name
    
    
class Category(models.Model):
    name = models.CharField(max_length=200)
    
    def __str__(self):
        return self.name



class post(models.Model):
    STATUS = (
        ('0','Draft'),
        ('1','Publish'),
    )
    title = models.CharField(max_length=2000)
    author = models.ForeignKey(CustomUser,on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    cover = models.ImageField(upload_to='post_covers/',blank=True, null=True, default='post_covers/default.png')
    tags = models.ManyToManyField(Tag)
    status = models.CharField(choices=STATUS,max_length=100)
    
    
    details = RichTextField(null=True, blank=True)
    
    
    visits = models.IntegerField(default=0)  # Track the number of visits
    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created', '-updated']

    def __str__(self):
        return self.title
    
    def delete(self, *args, **kwargs):
        # Delete associated cover picture if exists
        if self.cover:
            if os.path.isfile(self.cover.path):
                os.remove(self.cover.path)
        super(post, self).delete(*args, **kwargs)
    




class Comment(models.Model):
    # user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100, blank=True)
    blog = models.ForeignKey(post, on_delete=models.CASCADE)
    comment = models.TextField(max_length=500, null= True, blank=True)

    updated = models.DateTimeField(auto_now=True)
    created = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.comment[0:50]
    