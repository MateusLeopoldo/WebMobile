from django.views.generic import View
from django.shortcuts import render 
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse   

class Login(View):

    def get(self, request):
        contexto = {}
        return render(request, 'autenticacao.html', contexto)     
    
    def post(self, request):
        usuario = request.POST.get('usuario', None)
        senha = request.POST.get('senha', None)
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
             if user.is_active:
                login(request, user)
                return HttpResponse('Usuario autenticado com sucesso!')
        
        return render(request, 'autenticacao.html', {'mensagem': 'Login Falhou!'})