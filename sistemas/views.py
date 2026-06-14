from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.shortcuts import redirect, render


def home(request):
	if request.method == 'POST':
		username = request.POST.get('username', '').strip()
		password = request.POST.get('password', '')
		user = authenticate(request, username=username, password=password)

		if user is not None:
			auth_login(request, user)
			messages.success(request, 'Login realizado com sucesso.')
			return redirect('home')

		messages.error(request, 'Usuário ou senha inválidos.')

	return render(request, 'sistemas/login.html')
