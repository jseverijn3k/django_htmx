from django.db.models import Count
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import HttpResponse
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
    
    if request.htmx:
        # check if top is part of the url
        if 'top' in request.GET:
            # comments = post.comments.filter(likes__isnull=False).distinct()
            
            # annotate(num_likes=Count('likes')) -> counts all the likes and stores them in the variable num_likes
            # .filter(num_likes__gt=0) -> filters if the numk_likes is greater than 0 (gt0)
            print("TESTTEST")
            comments = post.comments.annotate(num_likes=Count('likes')).filter(num_likes__gt=0).order_by('-num_likes')
        else:
            comments = post.comments.all()
        return render(request, 'snippets/loop_postpage_comments.html', {'comments': comments, 'replyform': replyform})
    
    context = {
        'post' : post,
        'commentform' : commentform,
        'replyform' : replyform,
    }
    
    return render(request, "a_posts/post_page.html", context)


@login_required
def comment_sent(request, pk):
    post = get_object_or_404(Post, id=pk)
    replyform = ReplyCreateForm()

    if request.method == 'POST':
        form = CommentCreateForm(request.POST)
        if form.is_valid:
            comment = form.save(commit=False)
            comment.author = request.user
            comment.parent_post = post
            comment.save()

    context = {
        'post' : post,
        'comment': comment,
        'replyform': replyform
    }

    return render(request, 'snippets/add_comment.html', context)
            

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
    replyform = ReplyCreateForm()

    if request.method == 'POST':
        form = ReplyCreateForm(request.POST)
        if form.is_valid:
            reply = form.save(commit=False)
            reply.author = request.user
            reply.parent_comment = comment
            reply.save()

    context = {
        'comment': comment,
        'reply' : reply,
        'replyform': replyform
    }
    return render(request, 'snippets/add_reply.html', context)

            

@login_required
def reply_delete_view(request, pk):
    reply = get_object_or_404(Reply, id=pk, author=request.user)

    if request.method == 'POST':
        reply.delete()
        messages.success(request, 'Reply deleted successfully')  
        return redirect('post-page', reply.parent_comment.parent_post.id)
    
    return render(request, "a_posts/reply_delete.html", {'reply' : reply})


# Decorator function that takes the model (eg. Post, Comment or Reply)
def like_toggle(model):
    """
    Decorator for handling like toggling functionality on models (e.g., Post, Comment, or Reply).

    This decorator takes a model as an argument and returns a function that can be used to toggle
    likes on instances of that model. The decorated function is expected to handle the request and
    the model instance.

    Parameters:
        model (django.db.models.Model): The model on which likes are toggled.

    Usage:
    @like_toggle(Post)  # Apply the decorator to a view function handling likes on Post instances
    def post_like_toggle_view(request, post):
        # Your view logic here

    The decorated function should handle the request and the model instance, and the like
    toggling logic is implemented within the decorator.

    Example:
    @like_toggle(Post)
    def post_like_toggle_view(request, post):
        # Your view logic here
    """
    
    def inner_func(func):
        def wrapper(request, *args, **kwargs):
            # we pass in teh model (eg. Post, Comment or Reply) and get the id from the kwargs
            # we use psot as our variable (could also have been osmething else like model_var or comment)
            post = get_object_or_404(model, id=kwargs.get('pk'))
            print(post)
            # check if the user already liked the post
            user_exists = post.likes.filter(username=request.user.username).exists()

            if post.author != request.user:
                if user_exists:
                    post.likes.remove(request.user)
                else:
                    post.likes.add(request.user)
            return func(request, post)
        return wrapper
    return inner_func


@login_required
@like_toggle(Post)
def like_post(request, post):   
    return render(request, 'snippets/likes.html', {'post' : post })


@login_required
@like_toggle(Comment)
def like_comment(request, post):
    return render(request, 'snippets/likes_comment.html', {'comment': post})

@login_required
@like_toggle(Reply)
def like_reply(request, post):
    return render(request, 'snippets/likes_reply.html', {'reply': post})

# @login_required
# def like_comment(request, pk):
#     comment = get_object_or_404(Comment, id=pk)

#     # check if the user already liked the post
#     user_exists = comment.likes.filter(username=request.user.username).exists()

#     if comment.author != request.user:
#         if user_exists:
#             comment.likes.remove(request.user)
#         else:
#             comment.likes.add(request.user)
        
#         return render(request, 'snippets/likes_comment.html', {'comment': comment})


# @login_required
# def like_reply(request, pk):
#     reply = get_object_or_404(Reply, id=pk)

#     # check if the user already liked the post
#     user_exists = reply.likes.filter(username=request.user.username).exists()

#     if reply.author != request.user:
#         if user_exists:
#             reply.likes.remove(request.user)
#         else:
#             reply.likes.add(request.user)
        
#         return render(request, 'snippets/likes_reply.html', {'reply': reply})
    