from django.shortcuts import render, redirect
from decouple import config

import requests

from django.contrib.auth import (
    authenticate,
    login,
    logout,
    get_user_model
)

# pega o usuário personalizado
Usuario = get_user_model()


# LOGIN

def login_view(request):

    # impede usuário logado de acessar login novamente

    erro = None

    # verifica envio do formulário
    if request.method == 'POST':

        # pega dados do formulário
        id_acesso = request.POST.get('id_acesso')

        password = request.POST.get('password')

        # autentica usuário
        user = authenticate(

            request,

            id_acesso=id_acesso,

            password=password
        )

        # login válido
        if user is not None:

            login(request, user)

            return redirect('dashboard')

        # login inválido
        else:

            erro = 'ID ou senha inválidos.'

    return render(

        request,

        'usuarios/index.html',

        {'erro': erro}
    )


# CADASTRO

def register_view(request):

    erro = None

    if request.method == 'POST':

        # dados do formulário
        username = request.POST.get('username')

        email = request.POST.get('email')

        password1 = request.POST.get('password1')

        password2 = request.POST.get('password2')

        # resposta do recaptcha
        recaptcha_response = request.POST.get(
            'g-recaptcha-response'
        )

        # dados enviados ao google
        data = {

            'secret': config('RECAPTCHA_SECRET_KEY'),

            'response': recaptcha_response
        }

        # envia validação ao google
        response = requests.post(

            'https://www.google.com/recaptcha/api/siteverify',

            data=data
        )

        # transforma resposta em json
        result = response.json()

        # recaptcha inválido
        if not result.get('success'):

            erro = 'Confirme o reCAPTCHA.'

        # senhas diferentes
        elif password1 != password2:

            erro = 'As senhas não coincidem.'

        # username já existe
        elif Usuario.objects.filter(
            username=username
        ).exists():

            erro = 'Nome de usuário já existe.'

        # cria usuário
        else:

            user = Usuario.objects.create_user(

                username=username,

                email=email,

                password=password1
            )

            # faz login automático
            login(request, user)

            return redirect('dashboard')

    return render(

        request,

        'usuarios/register.html',

        {'erro': erro}
    )


# LOGOUT

def logout_view(request):

    logout(request)

    return redirect('login')


# INDEX

def index_view(request):

    return render(

        request,

        'usuarios/index.html'
    )