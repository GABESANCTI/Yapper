from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from .models import Yap
from .forms import YapForm

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
    return render(request, 'yaps/timeline.html', {'form': form, 'posts': posts})
