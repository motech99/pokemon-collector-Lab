from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('about/', views.about, name='about'),
    path('pokemons/', views.pokemons_index, name='index'),
    path('pokemons/<int:pokemon_id>/', views.pokemons_detail, name='detail'),
    path('pokemons/create/', views.PokemonCreate.as_view(), name='pokemons_create'),
    path('pokemons/<int:pk>/update/', views.PokemonUpdate.as_view(), name='pokemons_update'),
    path('pokemons/<int:pk>/delete/', views.PokemonDelete.as_view(), name='pokemons_delete'),
    path('pokemons/<int:pokemon_id>/add_exercise/', views.add_exercise, name='add_exercise'),
    path('pokemons/<int:pokemon_id>/assoc_trainer/<int:trainer_id>/', views.assoc_trainer, name='assoc_trainer'),
    path('pokemons/<int:pokemon_id>/unassoc_trainer/<int:trainer_id>/', views.unassoc_trainer, name='unassoc_trainer'),
    path('trainers/', views.TrainerList.as_view(), name='trainers_index'),
    path('trainers/<int:pk>/', views.TrainerDetail.as_view(), name='trainers_detail'),
    path('trainers/create/', views.TrainerCreate.as_view(), name='trainers_create'),
    path('trainers/<int:pk>/update/', views.TrainerUpdate.as_view(), name='trainers_update'),
    path('trainers/<int:pk>/delete/', views.TrainerDelete.as_view(), name='trainer_delete'),
]