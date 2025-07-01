# yaps/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count, F
from django.contrib import messages
# from django.core.paginator import Paginator # Removido, pois não será usado para paginação

from .models import Yap, Comment, Like
from .forms import YapForm, CommentForm
from core.models import User # Importado para uso no projeto, se necessário

@login_required
def general_timeline(request):
    yaps = Yap.objects.all().annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).select_related('user').order_by('-created_at')
    
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
    ).select_related('user').order_by('-created_at')
    
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
    
    # Incrementa o contador de visualizações
    # Usamos F() para evitar race conditions em acessos simultâneos
    yap.views_count = F('views_count') + 1
    yap.save(update_fields=['views_count'])
    yap.refresh_from_db() # Atualiza o objeto com o novo valor

    form = CommentForm() # Inicializa o formulário de comentário

    # Processa o formulário de comentário se for POST
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.yap = yap
            comment.user = request.user
            comment.save()
            # Redireciona de volta para a página de detalhes do Yap para evitar re-envio
            return redirect('yaps:yap_detail', pk=yap.pk)
    
    # Recupera os comentários, anota o número de curtidas e os ordena
    comments = yap.comments.all().annotate(
        num_likes=Count('likes', distinct=True) # Anota a contagem de likes
    ).order_by('-num_likes', 'created_at') # Ordena por mais curtidos, depois por mais antigos (se likes iguais)

    # Verifica se o usuário logado já curtiu este Yap
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
        messages.success(request, "Yap apagado com sucesso!")
    else:
        messages.error(request, "Você não tem permissão para apagar este Yap.")
    return redirect('yaps:general_timeline')

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    if request.user == comment.user or request.user == comment.yap.user:
        yap_pk = comment.yap.pk
        comment.delete()
        messages.success(request, "Comentário apagado com sucesso!")
    else:
        messages.error(request, "Você não tem permissão para apagar este comentário.")
    
    return redirect('yaps:yap_detail', pk=yap_pk)