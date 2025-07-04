
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Count, F
from django.contrib import messages
from datetime import datetime
from django.utils import timezone 
from django.core.cache import cache 
from .models import Yap, Comment, Like
from .forms import YapForm, CommentForm
from core.models import User
import requests
import random

# gestao dad jokes
def get_dad_joke():
    """
    Busca uma piada aleatória do icanhazdadjoke.com, usando cache.
    """
    # Tenta pegar a piada do cache primeiro
    cached_joke = cache.get('dad_joke_cache_key') # Chave para identificar a piada no cache
    if cached_joke:
        return cached_joke

    url = "https://icanhazdadjoke.com/"
    headers = {
        "Accept": "application/json",
        "User-Agent": "Yapper (seu-contato@example.com ou link-do-seu-repo)" 
    }
    
    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status() 
        data = response.json()
        
        joke_data = {
            'id': data['id'],
            'content': data['joke'],
            'is_dad_joke': True,
            'created_at': timezone.now(), 
            'username': 'DadJokeBot',
            'profile_url': 'https://icanhazdadjoke.com/',
            'is_yap': False
        }
        
        # Armazena a piada no cache por 5 minutos
        cache.set('dad_joke_cache_key', joke_data, 5 * 60)
        return joke_data

    except requests.exceptions.RequestException as e:
        print(f"Erro ao buscar piada: {e}")
        return None

# --- FUNÇÃO AUXILIAR PARA ORDENAR ITENS MISTOS ---
def get_item_creation_time(item):
    """
    Retorna a data de criação de um item, seja ele um objeto Yap ou um dicionário de piada.
    """
    if hasattr(item, 'created_at'): # Se for um objeto (Yap)
        return item.created_at
    elif isinstance(item, dict) and 'created_at' in item: # Se for um dicionário (Piada)
        return item['created_at']
    return datetime.min 




@login_required
def general_timeline(request):
    yaps_from_db = Yap.objects.all().annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).select_related('user').order_by('-created_at')
    
    combined_timeline = []

    # Adiciona os Yaps do banco de dados na lista combinada
    for yap in yaps_from_db:
        yap.is_yap = True # Marca como Yap para o template
        combined_timeline.append(yap)
    
    # Adiciona uma piada do cache na lista combinada

    num_jokes_to_add = 1 
    for _ in range(num_jokes_to_add):
        joke = get_dad_joke() 
        if joke:
            combined_timeline.append(joke)

    # Ordena a lista combinada (Yaps e Piadas) pelo campo 'created_at' em ordem decrescente
    combined_timeline.sort(key=get_item_creation_time, reverse=True)


    context = {
        'yaps': combined_timeline, 
        'form': YapForm(), 
    }
    return render(request, 'yaps/general_timeline.html', context)

@login_required
def foryou_timeline(request):
    # Yaps de usuários que o usuário logado segue
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
        form = YapForm(request.POST, request.FILES) 
        if form.is_valid():
            yap = form.save(commit=False)
            yap.user = request.user
            yap.save()
            messages.success(request, "Yap criado com sucesso!")
            return redirect('yaps:general_timeline')
    else:
        form = YapForm() 
        
    return render(request, 'yaps/create_yap.html', {'form': form})

def yap_detail(request, pk):
    yap = get_object_or_404(Yap, pk=pk)
    
   
    yap.views_count = F('views_count') + 1
    yap.save(update_fields=['views_count'])
    yap.refresh_from_db()

    form = CommentForm() # Inicializa o formulário de comentário
    if request.method == 'POST' and request.user.is_authenticated:
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.yap = yap
            comment.user = request.user
            comment.save()
            messages.success(request, "Comentário adicionado com sucesso!")
            return redirect('yaps:yap_detail', pk=yap.pk)
    
    # Recupera os comentários, anota o número de curtidas e os ordena (ordena por mais curtidos, depois por mais antigos se nº likes iguais)
    comments = yap.comments.all().annotate(
        num_likes=Count('likes', distinct=True) 
    ).order_by('-num_likes', 'created_at') # O

  
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