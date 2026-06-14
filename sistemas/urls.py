from django.urls import path

from .views import criar_maratona, editar_maratona, excluir_maratona, home, maratonas

urlpatterns = [
    path('', home, name='home'),
    path('maratonas/', maratonas, name='maratonas'),
    path('maratonas/criar/', criar_maratona, name='criar_maratona'),
    path('maratonas/<int:maratona_id>/editar/', editar_maratona, name='editar_maratona'),
    path('maratonas/<int:maratona_id>/excluir/', excluir_maratona, name='excluir_maratona'),
]