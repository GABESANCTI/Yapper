
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Yap, Comment, Like
from django.db.models import Count, F
from .forms import YapForm, CommentForm

def general_timeline(request):
    # Anota o número de likes e comentários diretamente no queryset
    yaps = Yap.objects.all().annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).select_related('user') # Otimiza a consulta para pegar o usuário junto
    
    context = {
        'yaps': yaps,
        'form': YapForm(), # Para permitir criar um yap na timeline geral
    }
    return render(request, 'yaps/general_timeline.html', context)

@login_required
def foryou_timeline(request):
    # Pega os usuários que o usuário logado segue
    followed_users = request.user.following.all()
    # Pega os yaps desses usuários
    yaps = Yap.objects.filter(user__in=followed_users).annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).select_related('user')
    
    context = {
        'yaps': yaps,
        'form': YapForm(),
    }
    return render(request, 'yaps/foryou_timeline.html', context)

@login_required
def create_yap(request):
    if request.method == 'POST':
        form = YapForm(request.POST)
        if form.is_valid():
            yap = form.save(commit=False) # Não salva ainda para adicionar o usuário
            yap.user = request.user
            yap.save()
            return redirect('yaps:general_timeline') # Redireciona para a timeline geral
    else:
        form = YapForm() # Formulário vazio para requisições GET
    return render(request, 'yaps/create_yap.html', {'form': form})

def yap_detail(request, pk):
    yap = get_object_or_404(Yap, pk=pk)
    
    # Incrementa o contador de views do yap
    yap.views_count = F('views_count') + 1
    yap.save(update_fields=['views_count']) # Salva apenas o campo views_count
    yap.refresh_from_db() # Atualiza o objeto 'yap' com o novo valor do banco

    # Pega os comentários e anota o número de curtidas para cada
    comments = yap.comments.all().annotate(likes_count=Count('likes', distinct=True)).select_related('user')
    
    form = CommentForm() # Formulário para adicionar novos comentários
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.yap = yap
            comment.user = request.user
            comment.save()
            return redirect('yaps:yap_detail', pk=pk) # Redireciona de volta para a mesma página

    # Verifica se o usuário logado já curtiu este yap
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
def delete_yap(request, pk):
    yap = get_object_or_404(Yap, pk=pk)
    if request.user == yap.user: # Apenas o dono do yap pode apagá-lo
        yap.delete()
    return redirect('yaps:general_timeline') # Redireciona após apagar

@login_required
def like_yap(request, pk):
    yap = get_object_or_404(Yap, pk=pk)
    # get_or_create: se já existe, retorna o objeto; se não, cria
    Like.objects.get_or_create(user=request.user, yap=yap)
    return redirect('yaps:yap_detail', pk=pk)

@login_required
def unlike_yap(request, pk):
    yap = get_object_or_404(Yap, pk=pk)
    # Deleta a curtida se ela existir
    Like.objects.filter(user=request.user, yap=yap).delete()
    return redirect('yaps:yap_detail', pk=pk)

@login_required
def like_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    Like.objects.get_or_create(user=request.user, comment=comment)
    return redirect('yaps:yap_detail', pk=comment.yap.pk) # Redireciona para o detalhe do Yap pai

@login_required
def unlike_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    Like.objects.filter(user=request.user, comment=comment).delete()
    return redirect('yaps:yap_detail', pk=comment.yap.pk)

@login_required
def delete_comment(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    # Apenas o dono do comentário OU o dono do yap pai pode apagar
    if request.user == comment.user or request.user == comment.yap.user:
        yap_pk = comment.yap.pk # Salva o PK do Yap pai para redirecionar
        comment.delete()
    return redirect('yaps:yap_detail', pk=yap_pk)