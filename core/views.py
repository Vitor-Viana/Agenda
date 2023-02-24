from django.shortcuts import render, redirect
from core.models import Anotacao
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages

# Create your views here.

@login_required(login_url='/login/')
def agenda(request):
    usuario = request.user
    anotacoes = Anotacao.objects.filter(usuario=usuario)
    response = {'anotacoes':anotacoes, 'usuario':usuario}
    return render(request, 'agenda.html', response)

def login_user(request):
    return render(request, 'login.html')

def submit_login(request):
    if request.POST:
        nome_usuario = request.POST.get('nomeusuario')
        senha = request.POST.get('senha')

        usuario = authenticate(username=nome_usuario, password=senha)

        if usuario is not None:
            login(request, usuario)
            return redirect('/')
        
        messages.error(request, 'Usuário ou Senha invalidos!')
    
    return redirect('/login')

def logout_user(request):
    logout(request)
    return redirect('/login/')
