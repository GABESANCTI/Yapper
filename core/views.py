from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F ,Q  #Q-> query F-> atomicidade nas buscas
from .models import User
from yaps.models import Yap

from .forms import CustomUserCreationForm,UserUpdateForm

def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST, request.FILES)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Cadastro realizado com sucesso! Bem-vindo(a) ao Yapper!")
            return redirect('yaps:general_timeline')
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').capitalize()}: {error}")
    else:
        form = CustomUserCreationForm()
    return render(request, 'core/register.html', {'form': form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserUpdateForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, "Seu perfil foi atualizado com sucesso!")
            return redirect('core:user_profile', username=request.user.username)
        else:
            for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f"{field.replace('_', ' ').capitalize()}: {error}")
    else:
        # Exibe o formulário preenchido com os dados atuais do usuário
        form = UserUpdateForm(instance=request.user)
    
    context = {
        'form': form,
    }
    return render(request, 'core/edit_profile.html', context)
@login_required
def user_profile(request, username):
    # Pega o usuário do perfil ou retorna 404
    profile_user = get_object_or_404(User, username=username)

    # Contagem de visualizações do perfil
    if request.user.is_authenticated and request.user != profile_user:
        profile_user.profile_views = F('profile_views') + 1
        profile_user.save(update_fields=['profile_views'])
        profile_user.refresh_from_db()

    # Pega os Yaps do usuário do perfil, anotando likes e comentários
    user_yaps = Yap.objects.filter(user=profile_user).annotate(
        likes_count=Count('likes', distinct=True),
        comments_count=Count('comments', distinct=True)
    ).order_by('-created_at')

    
    is_following = False
    if request.user.is_authenticated:
        #  ManyToManyField 'following' 
        is_following = request.user.following.filter(username=username).exists()

    context = {
        'profile_user': profile_user,
        'user_yaps': user_yaps,
        'is_following': is_following,
    }
    return render(request, 'core/user_profile.html', context)


@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user != user_to_follow:
        request.user.following.add(user_to_follow)
    return redirect('core:user_profile', username=username)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    if request.user != user_to_unfollow:
        request.user.following.remove(user_to_unfollow)
    return redirect('core:user_profile', username=username)

#my search view engine 

def search(request):
    query = request.GET.get('q')
    results = User.objects.none() # Inicializa um queryset vazio
    
    if query:
        # Lógica para buscar usuários por username ou display_name (case-insensitive)
        results = User.objects.filter(
            Q(username__icontains=query) | Q(display_name__icontains=query)
        ).distinct()
        
    context = {
        'query': query,
        'results': results,
    }
    return render(request, 'core/search_results.html', context)