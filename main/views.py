from django.shortcuts import render, redirect
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from .forms import *
from .models import *
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404
from django.contrib import messages

# Blog templates from:
# https://getbootstrap.com/docs/5.0/examples/


def sign_up(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('/home')
    else:
        form = RegisterForm()

    return render(request, 'sign_up.html', {'form':form})

def home(request):
    articles = Article.objects.all().order_by('-created')
    p = Paginator(articles, 5)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    return render(request, 'home.html', {'page_obj': page_obj})

def see_article(request, id):
    article = Article.objects.get(id = id)
    comments = article.comments.order_by('created')
    context = {
        'article':article,
        'comments':comments,
    }
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            text = request.POST.get('text')
            new_comment = Comment(author=request.user, article=article, text=text)
            new_comment.save()
    return render(request, 'article.html', context)


def new_tags(request):
    articles = Article.objects.all().order_by('-created')
    tags = []
    for art in articles:
        for tag in art.tags.all():
            if tag not in tags:
                tags.append(tag)
    # tags = Article.tags.most_common()
    p = Paginator(tags, 5)
    page_number = request.GET.get('page')
    page_obj = p.get_page(page_number)
    return render(request, 'new_tags.html', {'page_obj': page_obj})

def profile(request,id):
    user = User.objects.get(id=id)
    articles = Article.objects.filter(author=user).order_by('-created')
    comments = Comment.objects.filter(author=user).order_by('-created')
    context = {
        'id':id,
        'user':user,
        'articles': articles,
        'comments': comments,
    }
    return render(request, 'profile.html', context)

def search_by_tag(request, tag):
    _articles = Article.objects.all().order_by('-created')
    articles = []
    for a in _articles:
        for t in a.tags.all():
            if t.name == tag:
                articles.append(a)
    context = {
        'tag':tag,
        'articles':articles,
    }
    return render(request, 'tag_article.html', context)

@login_required
def delete_comment(request):
    comment_id = request.POST['comment_id']
    article_id = request.POST['article_id']
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        try:
            comment.delete()
            messages.success(request, 'You have successfully deleted the comment')
        except:
            messages.warning(request, 'The comment could not be deleted.')

    return redirect(f'/article/{article_id}')

@login_required
def like_comment(request):
    comment_id = request.POST['comment_id']
    article_id = request.POST['article_id']
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        
        is_like = False
        is_dislike = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_like:
            if is_dislike:
                comment.dislikes.remove(request.user)

            comment.likes.add(request.user)
            messages.success(request, 'Liked comment')
        
        if is_like:
            comment.likes.remove(request.user)

    return redirect(f'/article/{article_id}')

@login_required
def dislike_comment(request):
    comment_id = request.POST['comment_id']
    article_id = request.POST['article_id']
    if request.method == 'POST':
        comment = get_object_or_404(Comment, id=comment_id)
        
        is_like = False
        is_dislike = False

        for like in comment.likes.all():
            if like == request.user:
                is_like = True
                break

        for dislike in comment.dislikes.all():
            if dislike == request.user:
                is_dislike = True
                break

        if not is_dislike:
            if is_like:
                comment.likes.remove(request.user)
            comment.dislikes.add(request.user)
            messages.success(request, 'Disliked comment')
        
        if is_dislike:
            comment.dislikes.remove(request.user)

    return redirect(f'/article/{article_id}')

    