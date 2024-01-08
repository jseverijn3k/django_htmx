from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.shortcuts import render, redirect, get_object_or_404

from .forms import PostCreateForm, PostEditForm, CommentCreateForm, ReplyCreateForm
from .models import Post, Tag, Comment, Reply

from bs4 import BeautifulSoup
import requests


def home_view(request, tag=None):
    if tag:
        posts = Post.objects.filter(tags__slug=tag)
        tag = get_object_or_404(Tag, slug=tag)
    else:     
        posts=  Post.objects.all()
    
    context = {
        'posts' : posts,
        'categories' : Tag.objects.all(),
        'tag' : tag,
    }

    return render(request, "a_posts/home.html", context)
 

@login_required
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

            post.author = request.user

            post.save()
            form.save_m2m() # save our tags m2m field
            return redirect('home')
        
    form = PostCreateForm()
    return render(request, "a_posts/post_create.html", {'form' : form})


@login_required
def post_delete_view(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)

    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Post deleted successfully')  
        return redirect('home')
    
    return render(request, "a_posts/post_delete.html", {'post' : post})


@login_required
def post_edit_view(request, pk):
    post = get_object_or_404(Post, id=pk, author=request.user)
    form = PostEditForm(instance=post)

    context = {
        'post' : post,
        'form' : form,
    }
    
    if request.method == 'POST' and request.user == post.author:
        form = PostEditForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Post updated successfully')  
            return redirect('home')

    
    return render(request, "a_posts/post_edit.html", context)


def post_page_view(request, pk):
    post = get_object_or_404(Post, id=pk)

    commentform = CommentCreateForm()
    replyform = ReplyCreateForm()
    
    context = {
        'post' : post,
        'commentform' : commentform,
        'replyform' : replyform,
    }
    
    return render(request, "a_posts/post_page.html", context)


@login_required
def comment_sent(request, pk):
    print(request)
    print(f"pk : {pk}")

    post = get_object_or_404(Post, id=pk)
    print(f"Post : {post}")

    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()

    return redirect('post-page', post.id)
            

@login_required
def comment_delete_view(request, pk):
    comment = get_object_or_404(Comment, id=pk, author=request.user)

    if request.method == 'POST':
        comment.delete()
        messages.success(request, 'Comment deleted successfully')  
        return redirect('post-page', comment.parent_post.id)
    
    return render(request, "a_posts/comment_delete.html", {'comment' : comment})


@login_required
def reply_sent(request, pk):
    comment = get_object_or_404(Comment, id=pk)

    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid:
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()

    return redirect('post-page', comment.parent_post.id)
            

@login_required
def reply_delete_view(request, pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)

    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply deleted successfully')  
        return redirect('post-page', reply.parent_comment.parent_post.id)
    
    return render(request, "a_posts/reply_delete.html", {'reply' : reply})

