from django.urls import path
from .views import *
urlpatterns = [
    path('',index, name='home'),
    path('login',loginPage, name='login'),
    path('logout',logoutPage, name='logout'),
    path('register',registerUser, name='register'),
    path('profile/<str:pk>/',userProfile, name='profile'),
    path('create-post/',CreatePost, name='create-post'),
    path('update-post/<str:pk>/',UpdatePost, name='update-post'),
    path('blog-post/<str:pk>/',blogPost, name='blog-post'),
    path('search',search,name="search"),
    path('category',category,name="category"),
    path('blogs',AllBlogs,name="blogs"),
    path('about-us',aboutUs,name="about-us"),
    path('popular_post',popular_posts,name="popular_post"),
    path('contact-us',contactUs,name="contact-us"),
    path('edit-profile/<str:pk>', edit_profile, name='edit-profile'),
    path("own-blogs/<str:pk>",YourBlogs,name="own-blogs"),
]
