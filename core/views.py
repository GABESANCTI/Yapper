from django.shortcuts import render, redirect
from .models import Yap
from .forms import YapForm
from django.contrib.auth.decorators import login_required

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
