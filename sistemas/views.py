from django.contrib import messages
from django.contrib.auth import authenticate, login as auth_login
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.http import require_POST
from decimal import Decimal, InvalidOperation

from .models import Maratona


def _maratonas_permitidas(usuario):
	if usuario.is_superuser:
		return Maratona.objects.all()
	return Maratona.objects.filter(criado_por=usuario)


def _parse_distancia(valor):
	try:
		distancia = Decimal(valor)
	except (InvalidOperation, TypeError):
		return None

	if distancia < Decimal('0.01') or distancia > Decimal('999.99'):
		return None

	return distancia.quantize(Decimal('0.01'))


def home(request):
	if request.method == 'POST':
		username = request.POST.get('username', '').strip()
		password = request.POST.get('password', '')
		user = authenticate(request, username=username, password=password)

		if user is not None:
			auth_login(request, user)
			messages.success(request, 'Login realizado com sucesso.')
			return redirect('maratonas')

		messages.error(request, 'Usuário ou senha inválidos.')

	return render(request, 'sistemas/login.html')


@login_required(login_url='home')
def maratonas(request):
	lista_maratonas = _maratonas_permitidas(request.user)
	return render(request, 'sistemas/maratonas.html', {'maratonas': lista_maratonas, 'active_tab': 'lista'})


@login_required(login_url='home')
def criar_maratona(request):
	if request.method == 'POST':
		cidade = request.POST.get('cidade', '').strip()
		distancia_raw = request.POST.get('distancia', '').strip()
		data = request.POST.get('data', '').strip()
		imagem = request.FILES.get('imagem')
		distancia = _parse_distancia(distancia_raw)

		if not cidade or not data or distancia is None:
			messages.error(request, 'Preencha cidade e data. Distancia deve estar entre 0.01 e 999.99.')
		else:
			Maratona.objects.create(
				criado_por=request.user,
				cidade=cidade,
				distancia=distancia,
				data=data,
				imagem=imagem,
			)
			messages.success(request, 'Maratona criada com sucesso.')
			return redirect('maratonas')

	return render(request, 'sistemas/criar_maratona.html', {'active_tab': 'criar'})


@login_required(login_url='home')
def editar_maratona(request, maratona_id):
	maratona = get_object_or_404(_maratonas_permitidas(request.user), id=maratona_id)

	if request.method == 'POST':
		cidade = request.POST.get('cidade', '').strip()
		distancia_raw = request.POST.get('distancia', '').strip()
		data = request.POST.get('data', '').strip()
		imagem = request.FILES.get('imagem')
		distancia = _parse_distancia(distancia_raw)

		if not cidade or not data or distancia is None:
			messages.error(request, 'Preencha cidade e data. Distancia deve estar entre 0.01 e 999.99.')
		else:
			maratona.cidade = cidade
			maratona.distancia = distancia
			maratona.data = data
			if imagem:
				maratona.imagem = imagem
			maratona.save()
			messages.success(request, 'Maratona atualizada com sucesso.')
			return redirect('maratonas')

	return render(request, 'sistemas/editar_maratona.html', {'active_tab': 'criar', 'maratona': maratona})


@login_required(login_url='home')
@require_POST
def excluir_maratona(request, maratona_id):
	maratona = get_object_or_404(_maratonas_permitidas(request.user), id=maratona_id)
	maratona.delete()
	messages.success(request, 'Maratona excluida com sucesso.')
	return redirect('maratonas')
