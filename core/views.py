from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import login
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db.models import Count, F

# Importe seus modelos personalizados
from .models import User
from yaps.models import Yap # Para pegar os yaps do usuário

# Importe seus formulários
from .forms import CustomUserCreationForm

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

# View para o perfil do usuário
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

    # Verifica se o usuário logado está seguindo o usuário do perfil
    is_following = False
    if request.user.is_authenticated:
        # A relação ManyToManyField 'following' está no seu modelo User
        is_following = request.user.following.filter(username=username).exists()

    context = {
        'profile_user': profile_user,
        'user_yaps': user_yaps,
        'is_following': is_following,
    }
    return render(request, 'core/user_profile.html', context)

# Views para seguir/deixar de seguir
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