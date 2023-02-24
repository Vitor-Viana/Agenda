from django.shortcuts import render
from core.models import Anotacao

# Create your views here.

def agenda(request):
    usuario = request.user
    anotacoes = Anotacao.objects.filter(usuario=usuario)
    response = {'anotacoes':anotacoes, 'usuario':usuario}
    return render(request, 'agenda.html', response)
