"""agenda URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from core import views 

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.agenda),
    path('criar-agenda/', views.criar_agenda),
    path('criar-agenda/submit', views.criar_agenda_submit),
    path('atualizar-agenda/<int:id_anotacao>/', views.atualizar_agenda),
    path('atualizar-agenda/<int:id_anotacao>/submit', views.atualizar_agenda_submit),
    path('delete-agenda/<int:id_anotacao>/', views.delete_agenda),
    path('login/', views.login_user),
    path('login/submit', views.submit_login),
    path('logout/', views.logout_user),
    path('cadastrar-usuario/', views.cadastrar_usuario),
    path('cadastrar-usuario/submit', views.cadastrar_usuario_submit),
    path('recuperar-senha/', views.recuperar_senha),
    path('recuperar-senha/submit', views.recuperar_senha_submit),
    path('recuperar-senha/<int:codigo>/', views.recuperar_senha_codigo),
]
