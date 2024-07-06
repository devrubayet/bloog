from django.shortcuts import get_object_or_404, render,HttpResponse,redirect
from django.views import View
from .models import *
from .forms import *
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator,EmptyPage,PageNotAnInteger
from django.db.models import Q
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import PasswordChangeForm
from django.contrib.auth import update_session_auth_hash

from .utils import send_welcome_email  # Import the utility function

# Create your views here.

def index(request):
    posts = post.objects.filter(status='1')
    categories = Category.objects.all()

   
    
    

 


    
    context = {
        'posts':posts,
        'categories':categories,
        
        
        
    }
    return render(request,"index.html",context)




def blogPost(request,pk):
    blog = post.objects.get(id=pk)
    
    
     # Increment the visit count
    blog.visits += 1
    blog.save()
    
    more_blogs = post.objects.filter(Q(category__name__icontains=blog.category) )
    categories = Category.objects.all()
    
    tags = blog.tags.all()  # Retrieve associated tags for the post

    
    popular_posts = post.objects.order_by('-visits')[:5]  # Retrieve top 5 popular posts
    
    
    blog_comments = blog.comment_set.all().order_by('-created')
    
    if request.method == "POST":
        
        commnets = Comment.objects.create(
            blog = blog,
            name = request.POST.get('name'),
            comment = request.POST.get('massage'),
        )

    context = {
        'more_blogs':more_blogs,
        'blog':blog,
        'categories':categories,
        'blog_comments':blog_comments,
        'popular_posts': popular_posts,
        'tags': tags,
    }
    return render(request,"single.html",context)




def AllBlogs(request):
    posts = post.objects.filter(status='1')
    categories = Category.objects.all()
    
    
    
    
    
    page_number = request.GET.get("page")
    paginator = Paginator(posts, 5)  # Show 25 contacts per page.
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)
        
    return render(request,"blog.html",{'page_obj':page_obj,'categories':categories,'posts':posts})


def loginPage(request):

    page = 'login'
    

    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')


        try:
            user = CustomUser.objects.get(username=username)
        except:
           pass

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request,user)
            messages.success(request, "Log in Successfull.")
            return redirect('home')
        else:
            messages.error(request, "user does'nt exits.")


    context = {'page':page}

    return render(request, 'login_register.html',context)



def logoutPage(request):
    logout(request)
    return redirect('home')



def registerUser(request):

    form = MyUserCreationForm()

    if request.method == 'POST':
        form = MyUserCreationForm(request.POST)

        if form.is_valid():
            user = form.save(commit=False)

            user.username = user.username.lower()
            user.name=user.name
            user.save()
            login(request,user)
            messages.success(request,"user creation succes!")
            
             # Send welcome email
            send_welcome_email(user.email)
            return redirect('home')

    context = {
            'form':form,
            # 'messages':messages,
        }
    return render(request, 'login_register.html',context)



def CreatePost(request):
    posts = post.objects.filter(status='1')
    form = CreatePostForm()
    categories = Category.objects.all()

    # if request.method == 'POST':
    #     form = CreatePostForm(request.POST, request.FILES)
        
    #     category_name = request.POST.get('category')
    #     category, created = Category.objects.get_or_create(name=category_name)

    #     post.objects.create(
    #         title=request.POST.get('title'),
    #         category=category,
    #         cover=request.FILES.get('cover'),  # Use request.FILES to get the uploaded file
    #         details=request.POST.get('details'),
    #     )
        
    #     return redirect('home')
    
    if request.method == 'POST':
        form = CreatePostForm(request.POST, request.FILES)
        
        category_name = request.POST.get('category')
        category, created = Category.objects.get_or_create(name=category_name)

        tags = request.POST.get('tags')
        tag_list = [tag.strip() for tag in tags.split(',') if tag.strip()]  # Split tags by comma

        new_post = post.objects.create(
            author = request.user,
            title=request.POST.get('title'),
            category=category,
            cover=request.FILES.get('cover'),  # Use request.FILES to get the uploaded file
            details=request.POST.get('details'),
        )
        
        # Check if cover image is provided, if not, use default image
        if not new_post.cover:
            new_post.cover = 'post_covers/default.png'
            new_post.save()

        for tag_name in tag_list:
            tag, _ = Tag.objects.get_or_create(name=tag_name)
            new_post.tags.add(tag)
            
        
           

        return redirect('home')



    form.fields['tags'].widget.attrs.update({'class': 'form-control'})
    context = {
        'posts':posts,
        'form': form,
        'categories': categories,
    }
    return render(request, "create-post.html", context)





def UpdatePost(request, pk):
    post_instance = post.objects.get(id=pk)
    form = PostForm(instance=post_instance)
    
    if request.method == "POST":
        form = PostForm(request.POST, request.FILES, instance=post_instance)
        if form.is_valid():
            category_name = form.cleaned_data['category']
            # Check if the category already exists
            try:
                existing_category = Category.objects.get(name=category_name)
                form.instance.category = existing_category
            except Category.DoesNotExist:
                # If it doesn't exist, create a new category
                new_category = Category.objects.create(name=category_name)
                form.instance.category = new_category
            
            form.save()
            messages.success(request, 'Post updated successfully.')
            return redirect('blog-post', pk=post_instance.id)
        else:
            messages.error(request, 'Form is not valid. Please check the errors.')
    
    context = {
        'form': form,
        'post_instance': post_instance,
    }
    return render(request, "update-post.html", context)




@login_required
def edit_profile(request, pk):
    if request.method == 'POST':
        user_form = CustomUserChangeForm(request.POST, request.FILES, instance=request.user)
        password_form = CustomPasswordChangeForm(request.user, request.POST)
        
        
        if 'change_password' in request.POST and request.POST['change_password'] == 'on':  # If checkbox is checked
            if user_form.is_valid() and password_form.is_valid():
                user_form.save()
                password_form.save()
                update_session_auth_hash(request, request.user)  # Update session with new authentication hash
                messages.success(request, 'Profile and password updated successfully.')
                return redirect('profile', pk=request.user.pk)  # Redirect to user profile page after saving
            
            for field, errors in password_form.errors.items():
                for error in errors:
                    messages.error(request, f"{password_form.fields[field].label}: {error}")
            
            
        else:
            # If checkbox is not checked
            if user_form.is_valid():
                user_form.save()
                messages.success(request, 'Profile updated successfully.')
                return redirect('profile', pk=request.user.pk)  # Redirect to user profile page after saving
        
            # Capture form errors and add them to messages
            for field, errors in user_form.errors.items():
                for error in errors:
                    messages.error(request, f"{user_form.fields[field].label}: {error}")
            
    else:
        user_form = CustomUserChangeForm(instance=request.user)
        password_form = CustomPasswordChangeForm(request.user)
    
    return render(request, 'edit_profile.html', {'user_form': user_form, 'password_form': password_form})



def userProfile(request,pk):
    user = CustomUser.objects.get(id=pk)

    blogs = user.post_set.all()
    # blogs_messages = user.comment_set.all()
    category = Category.objects.all()
    context = {'user':user,'blogs':blogs,"categories":category}
    return render(request, 'profile.html',context)




def search(request):
    posts = post.objects.filter(status='1')
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    blogs = post.objects.filter(Q(category__name__icontains=q) |
                                Q(title__icontains=q))
    
    page_number = request.GET.get("page")
    paginator = Paginator(blogs, 5)  # Show 25 contacts per page.
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)    
     
    context = {
        'posts':posts,
        'page_obj':page_obj
        
        
    }
    return render(request,'search-result.html',context)


def category(request):
    posts = post.objects.filter(status='1')
    categories = Category.objects.all()
    

    
    popular_posts = post.objects.order_by('-visits')[:5]  
    q = request.GET.get('q') if request.GET.get('q') != None else ''
    blogs = post.objects.filter(Q(category__name__icontains=q) )
    
    
    page_number = request.GET.get("page")
    paginator = Paginator(blogs, 5)  # Show 25 contacts per page.
    try:
        page_obj = paginator.get_page(page_number)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)           

     
    context = {
        'posts':posts,
        'page_obj':page_obj,
        'categories':categories,
        'popular_posts':popular_posts,
        
        
    }
    return render(request,'category.html',context)



def aboutUs(request):
    posts = post.objects.filter(status='1')
    context = {
        'posts':posts,
       
    }
    return render(request,'about.html',context)

def contactUs(request):
    posts = post.objects.filter(status='1')
    context = {
        'posts':posts,
        
    }
    return render(request,'contact.html',context)

def YourBlogs(request,pk):
    user = CustomUser.objects.get(id=pk)

    blogs = user.post_set.all()
    context = {'user':user,'blogs':blogs,"category":category}
    return render(request,'own-blogs.html',context)
def deleteBLog(request,pk):
    blog = post.objects.get(id=pk)
    blog.delete()
    return redirect('own-blogs', request.user.id)

class TogglePublishView(View):
    def post(self, request, pk):
        post_instance = get_object_or_404(post, pk=pk)
        if post_instance.status == '0':
            post_instance.status = '1'
        else:
            post_instance.status = '0'
        post_instance.save()
        previous_url = request.META.get('HTTP_REFERER', '/')
        return redirect(previous_url)

def popular_posts(request):
    popular_posts = popular_posts.objects.order_by('-visits')[:5]  # Retrieve top 5 popular posts
    return render(request, 'popular_posts.html', {'popular_posts': popular_posts})
 


def all_new_posts(request):
    posts = post.objects.all().order_by('-created','-updated')
    context = {
        'posts':posts
    }
    return render(request,"all_new_post.html", context)