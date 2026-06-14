from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models


class Maratona(models.Model):
	criado_por = models.ForeignKey(User, on_delete=models.CASCADE, related_name='maratonas', null=True, blank=True)
	cidade = models.CharField(max_length=120)
	data = models.DateField()
	distancia = models.DecimalField(max_digits=5, decimal_places=2)
	imagem = models.FileField(upload_to='maratonas/', blank=True, null=True)

	class Meta:
		ordering = ['data', 'cidade']
		constraints = [
			models.CheckConstraint(
				condition=models.Q(distancia__gte=Decimal('0.01')) & models.Q(distancia__lte=Decimal('999.99')),
				name='maratona_distancia_valida',
			),
		]

	def __str__(self):
		return f'{self.cidade} - {self.data}'
