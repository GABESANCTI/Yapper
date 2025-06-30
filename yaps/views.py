# yaps/views.py
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.http import JsonResponse
from django.db.models import Count, F
from django.contrib import messages
from django.contrib.auth import get_user_model


from .models import Yap, Comment, Like
from .forms import YapForm, CommentForm
User = get_user_model()

@login_required
def general_timeline(request):
    # Otimização: Anota a contagem de likes e comentários na query
    # E garante a ordenação do mais recente para o mais antigo
    yaps = Yap.objects.all().annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).select_related('user').order_by('-created_at') # <-- CORREÇÃO AQUI
    
    form = YapForm()
    context = {
        'yaps': yaps,
        'form': form,
    }
    return render(request, 'yaps/general_timeline.html', context)

@login_required
def foryou_timeline(request):
    followed_users = request.user.following.all()
    # Adiciona a ordenação explícita também para a timeline 'Para Você'
    yaps = Yap.objects.filter(user__in=followed_users).annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).select_related('user').order_by('-created_at') # <-- CORREÇÃO AQUI
    
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
    
    # Contagem de Views: Incrementa o contador de views ao acessar a página
    yap.views_count = F('views_count') + 1
    yap.save(update_fields=['views_count'])
    yap.refresh_from_db()

    # Pega todos os comentários relacionados a este Yap
    # E anota a contagem de likes para cada um
    comments = yap.comments.all().annotate(
        likes_count=Count('likes', distinct=True)
    ).select_related('user')

    form = CommentForm() # Inicializa o formulário de comentário

    # Lógica para adicionar um novo comentário
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.yap = yap
            comment.user = request.user
            comment.save()
            # Redireciona de volta para a página de detalhes do Yap para evitar re-envio
            return redirect('yaps:yap_detail', pk=pk)
    
    # Verifica se o usuário logado já curtiu este Yap para controlar o botão
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
@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # Permite que o dono do comentário OU o dono do Yap o apague
    if request.user == comment.user or request.user == comment.yap.user:
        yap_pk = comment.yap.pk # Salva o ID do Yap para redirecionar de volta
        comment.delete()
        messages.success(request, "Comentário apagado com sucesso!")
    else:
        messages.error(request, "Você não tem permissão para apagar este comentário.")
    
    return redirect('yaps:yap_detail', pk=yap_pk)