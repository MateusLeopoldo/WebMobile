from django.views.generic import View
from django.shortcuts import redirect, render 
from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse   

class Login(View):

    def get(self, request):
        contexto = {}
        if request.user.is_authenticated:
            return redirect("/album")
        else:
            return render(request, 'autenticacao.html', contexto)
    
    def post(self, request):
        usuario = request.POST.get('usuario', None)
        senha = request.POST.get('senha', None)
        user = authenticate(request, username=usuario, password=senha)
        if user is not None:
             if user.is_active:
                login(request, user)
                return redirect("/album")     
        else:
            # Redireciona de volta para a página de login em caso de falha
            return redirect('/?mensagem=Usuário ou senha inválidos!')
    
class Logout(View):

    def get(self, request):
        logout(request)
        return redirect("/")