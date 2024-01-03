from django.contrib import messages
from django.shortcuts import render, redirect

from .forms import PostCreateForm, PostEditForm
from .models import Post


from bs4 import BeautifulSoup
import requests

# Create your views here.
def home_view(request, *args, **kwargs):
    print(request.user)
    context = {
        'posts' : Post.objects.all()
    }

    return render(request, "a_posts/home.html", context)

 

def post_create_view(request, *args, **kwargs):
    if request.method == 'POST':
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            website = requests.get(form.data['url'])
            sourcecode = BeautifulSoup(website.text, 'html.parser')
            # print(sourcecode)

            find_image = sourcecode.select('meta[content^="https://live.staticflickr.com/"]')
            print(find_image)
            image = find_image[0]['content']
            post.image = image

            find_title = sourcecode.select('h1.photo-title')
            titile = find_title[0].text.strip()
            post.title = titile

            find_artist = sourcecode.select('a.owner-name') 
            artist = find_artist[0].text.strip()    
            post.artist = artist

            post.save()
            return redirect('home')
        
    form = PostCreateForm()
    return render(request, "a_posts/post_create.html", {'form' : form})

def post_delete_view(request, pk):
    post = Post.objects.get(id=pk)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully')  
        return redirect('home')
    
    return render(request, "a_posts/post_delete.html", {'post' : post})


def post_edit_view(request, pk):
    post = Post.objects.get(id=pk)
    form = PostEditForm(instance=post)

    context = {
        'post' : post,
        'form' : form,
    }
    
    if request.method == 'POST':
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully')  
            return redirect('home')

    
    return render(request, "a_posts/post_edit.html", context)

