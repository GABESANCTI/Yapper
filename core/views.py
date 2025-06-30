
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from .models import User
from yaps.models import Yap
from django.db.models import F # Para incrementar o contador de views

def user_profile(request, username):
    profile_user = get_object_or_404(User, username=username)
    yaps = profile_user.yaps.all() # Pega todos os yaps do usuário
    
    # Lógica para contar views do perfil
    if request.user.is_authenticated and request.user != profile_user:
        profile_user.profile_views = F('profile_views') + 1
        profile_user.save(update_fields=['profile_views'])
        profile_user.refresh_from_db() # Atualiza o objeto com o novo valor

    is_following = False
    if request.user.is_authenticated:
        # Verifica se o usuário logado está seguindo este perfil
        is_following = request.user.following.filter(username=username).exists()

    context = {
        'profile_user': profile_user,
        'yaps': yaps,
        'is_following': is_following,
    }
    return render(request, 'core/user_profile.html', context)

@login_required
def follow_user(request, username):
    user_to_follow = get_object_or_404(User, username=username)
    if request.user != user_to_follow: # Não pode seguir a si mesmo
        request.user.following.add(user_to_follow)
    return redirect('core:user_profile', username=username)

@login_required
def unfollow_user(request, username):
    user_to_unfollow = get_object_or_404(User, username=username)
    if request.user != user_to_unfollow: # Não pode deixar de seguir a si mesmo
        request.user.following.remove(user_to_unfollow)
    return redirect('core:user_profile', username=username)