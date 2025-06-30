from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count, F

from .models import Yap, Comment, Like
from .forms import YapForm, CommentForm

@login_required
def general_timeline(request):
    # Otimização: Anota a contagem de likes e comentários na query
    yaps = Yap.objects.all().annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).select_related('user')
    
    form = YapForm()
    context = {
        'yaps': yaps,
        'form': form,
    }
    return render(request, 'yaps/general_timeline.html', context)

@login_required
def foryou_timeline(request):
    followed_users = request.user.following.all()
    yaps = Yap.objects.filter(user__in=followed_users).annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).select_related('user')
    
    form = YapForm()
    context = {
        'yaps': yaps,
        'form': form,
    }
    return render(request, 'yaps/foryou_timeline.html', context)

@login_required
def create_yap(request):
    if request.method == 'POST':
        form = YapForm(request.POST)
        if form.is_valid():
            yap = form.save(commit=False)
            yap.user = request.user
            yap.save()
            return redirect('yaps:general_timeline')
    else:
        form = YapForm()
    return render(request, 'yaps/create_yap.html', {'form': form})

def yap_detail(request, pk):
    yap = get_object_or_404(Yap, pk=pk)
    
    # Contagem de Views: Incrementa o contador de views
    yap.views_count = F('views_count') + 1
    yap.save(update_fields=['views_count'])
    yap.refresh_from_db()

    comments = yap.comments.all().annotate(
        likes_count=Count('likes', distinct=True)
    ).select_related('user')

    form = CommentForm()
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.yap = yap
            comment.user = request.user
            comment.save()
            return redirect('yaps:yap_detail', pk=pk)

    is_liked = False
    if request.user.is_authenticated:
        is_liked = Like.objects.filter(user=request.user, yap=yap).exists()

    context = {
        'yap': yap,
        'comments': comments,
        'form': form,
        'is_liked': is_liked,
    }
    return render(request, 'yaps/yap_detail.html', context)

@login_required
@require_POST
def like_yap(request, pk):
    yap = get_object_or_404(Yap, pk=pk)
    user = request.user
    like_instance = Like.objects.filter(user=user, yap=yap).first()

    if like_instance:
        like_instance.delete()
        liked = False
    else:
        Like.objects.create(user=user, yap=yap)
        liked = True

    return JsonResponse({'total_likes': yap.likes.count(), 'liked': liked})

@login_required
@require_POST
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    user = request.user
    like_instance = Like.objects.filter(user=user, comment=comment).first()

    if like_instance:
        like_instance.delete()
        liked = False
    else:
        Like.objects.create(user=user, comment=comment)
        liked = True
    
    return JsonResponse({'total_likes': comment.likes.count(), 'liked': liked})

@login_required
def delete_yap(request, pk):
    yap = get_object_or_404(Yap, pk=pk)
    if request.user == yap.user:
        yap.delete()
    return redirect('yaps:general_timeline')

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.user or request.user == comment.yap.user:
        yap_pk = comment.yap.pk
        comment.delete()
    return redirect('yaps:yap_detail', pk=yap_pk)