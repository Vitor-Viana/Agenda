from django.shortcuts import render, redirect
from core.models import Anotacao, CodigoRecuperacao
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
import random, string

# Create your views here.

@login_required(login_url='/login/')
def agenda(request):
    usuario = request.user
    anotacoes = Anotacao.objects.filter(usuario=usuario)
    response = {'anotacoes':anotacoes, 'usuario':usuario}
    return render(request, 'agenda.html', response)

@login_required(login_url='/login/')
def criar_agenda(request):
    usuario = request.user
    response = {'usuario':usuario}
    return render(request, 'criar-agenda.html', response)

@login_required(login_url='/login/')
def criar_agenda_submit(request):
    if request.POST:
        titulo = request.POST.get('titulo')
        data_hora = request.POST.get('data-hora')
        descricao = request.POST.get('descricao')

        if titulo and data_hora:
            Anotacao.objects.create(titulo=titulo,
                                    data_hora=data_hora,
                                    descricao=descricao,
                                    usuario=request.user)
        else:
            messages.error(request, 'Os campos título, data e hora são obrigatórios!')
            return redirect('/criar-agenda/')
        
    return redirect('/')

@login_required(login_url='/login/')
def delete_agenda(request, id_anotacao):
    usuario = request.user
    anotacao = Anotacao.objects.get(id=id_anotacao)

    if anotacao.usuario == usuario:
        anotacao.delete()
    return redirect('/')

@login_required(login_url='/login/')
def atualizar_agenda(request, id_anotacao):
    usuario = request.user
    anotacao = Anotacao.objects.get(id=id_anotacao)
    response = {}
    response['anotacao'] = anotacao
    response['usuario'] = usuario

    if anotacao.usuario == usuario:
        return render(request, 'atualizar-agenda.html', response)

    return redirect('/')

@login_required(login_url='/login/')
def atualizar_agenda_submit(request, id_anotacao):
    if request.POST:
        usuario = request.user

        titulo = request.POST.get('titulo')
        data_hora = request.POST.get('data-hora')
        descricao = request.POST.get('descricao')

        anotacao = Anotacao.objects.get(id=id_anotacao)

        if titulo and data_hora and anotacao.usuario == usuario:
            Anotacao.objects.filter(id=id_anotacao).update(titulo=titulo,
                                                           data_hora=data_hora,
                                                           descricao=descricao)
        else:
            messages.error(request, 'Os campos título, data e hora são obrigatórios!')
            return redirect('/atualizar-agenda/'+str(id_anotacao))
        
    return redirect('/')

def login_user(request):
    return render(request, 'login.html')

def submit_login(request):
    if request.POST:
        nome_usuario = request.POST.get('nome-usuario')
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

def cadastrar_usuario(request):
    return render(request, 'cadastrar-usuario.html')

def cadastrar_usuario_submit(request):
    if request.POST:
        nome_usuario = request.POST.get('nome-usuario')
        email = request.POST.get('email')
        senha = request.POST.get('senha')
        confirmar_senha = request.POST.get('confirmar-senha')

        if not nome_usuario or not email or not senha or not confirmar_senha:
            messages.error(request, 'Todos os campos são obrigatórios!')
            return redirect('/cadastrar-usuario/')
        elif senha != confirmar_senha or len(senha) < 8 or len(senha) > 16:
            messages.error(request, 'Senha inválida!')
            return redirect('/cadastrar-usuario/')

        try:
            usuario = User.objects.get(username=nome_usuario)
            messages.error(request, 'Usuário já cadastrado!')
            return redirect('/cadastrar-usuario/')
        except User.DoesNotExist:
            try:
                usuario = User.objects.get(email=email)
                messages.error(request, 'E-mail já cadastrado!')
                return redirect('/cadastrar-usuario/')
            except User.DoesNotExist:
                novoUsuario = User.objects.create_user(username=nome_usuario,
                                                       email=email,
                                                       password=senha)
                novoUsuario.save()

    return redirect('/login/')

def recuperar_senha(request):
    return render(request, 'recuperar-senha.html')

def recuperar_senha_submit(request):
    if request.POST:
        try:
            email = request.POST.get('email')
            usuario = User.objects.get(email=email)

            '''
                Gerando código de recuperação de senha.
                O código é concatenado com o id do usuário para garantir que ele seja único.
            '''
            codigo_recuperacao = ''
            for _ in range(90):
                codigo_recuperacao += random.choice(string.ascii_uppercase)
            
            codigo_recuperacao += str(usuario.id)

            codigo = CodigoRecuperacao.objects.filter(usuario=usuario)
            if codigo:
                codigo.delete()
                CodigoRecuperacao.objects.create(codigo=codigo_recuperacao,
                                                 usuario=usuario)
            else:
                CodigoRecuperacao.objects.create(codigo=codigo_recuperacao,
                                                 usuario=usuario)
            # Enviar E-mail
            print('URL: localhost:8000/recuperar-senha/' + str(codigo_recuperacao) + '/')

            messages.success(request, 'Verifique seu e-mail em busca de um link para redefinir sua senha. Se não aparecer em alguns minutos, verifique sua pasta de spam.')
            
        except User.DoesNotExist:
            messages.error(request, 'E-mail não cadastrado!')
            
    return redirect('/recuperar-senha/')

def redefinir_senha(request, codigo):
    try:
        usuario = CodigoRecuperacao.objects.get(codigo=codigo).usuario
        respons = {'usuario':usuario}
        return render(request, 'redefinir-senha.html', respons)

    except CodigoRecuperacao.DoesNotExist:
        return redirect('/recuperar-senha/')

def redefinir_senha_submit(request, codigo):
    if request.POST:
        try:
            codigo = CodigoRecuperacao.objects.get(codigo=codigo)
            
            senha = request.POST.get('senha')
            confirmar_senha = request.POST.get('confirmar-senha')

            if not senha or not confirmar_senha:
                messages.error(request, 'Todos os campos são obrigatórios!')
                return redirect('/recuperar-senha/'+str(codigo.codigo))
            elif senha != confirmar_senha or len(senha) < 8 or len(senha) > 16:
                messages.error(request, 'Senha inválida!')
                return redirect('/recuperar-senha/'+str(codigo.codigo))

            usuario = User.objects.get(username=codigo.usuario)
            usuario.set_password(senha)
            usuario.save()  

            codigo.delete()

            return redirect('/login/')
            
        except CodigoRecuperacao.DoesNotExist:
            return redirect('/recuperar-senha/')
    
    return redirect('/recuperar-senha/')
