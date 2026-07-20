from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from src.core.models import TranslationHistory

@login_required(login_url="login")
def dashboard_view(request):
    history = TranslationHistory.objects.filter(user=request.user)
    return render(request, 'dashboard.html', {'history': history})
