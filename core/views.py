from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth import login, logout
from .models import Yap
from .forms import YapForm
from .forms import RegisterForm


#formulario de registro de usuario simples
def register_view(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)  # loga o usuário após registrar
            return redirect('timeline')  # redireciona pra timeline
    else:
        form = RegisterForm()
    return render(request, 'core/register.html', {'form': form})

#login de usuarios :D
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            login(request, user)
            return redirect('timeline')  # redireciona para timeline
    else:
        form = AuthenticationForm()
    return render(request, 'core/login.html', {'form': form})

@login_required
def logout_view(request):
    logout(request)
    return redirect('login')


#timeline ja com o formulario de postagem e user auth
@login_required
def timeline(request):
    if request.method == 'POST':
        form = YapForm(request.POST)
        if form.is_valid():
            yap = form.save(commit=False)
            yap.autor = request.user
            yap.save()
            return redirect('timeline')
    else:
        form = YapForm()
    
    posts = Yap.objects.all().order_by('-criado_em')
    return render(request, 'core/timeline.html', {'posts': posts, 'form': form})
