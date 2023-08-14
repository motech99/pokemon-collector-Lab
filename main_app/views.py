from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from .models import Pokemon
from .forms import ExerciseForm

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def pokemons_index(request):
    pokemons = Pokemon.objects.all()
    return render(request, 'pokemons/index.html', {
        'pokemons': pokemons
    })

def pokemons_detail(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    exercise_form = ExerciseForm()
    return render(request, 'pokemons/detail.html', {
        'pokemon': pokemon, 'exercise_form': exercise_form
    })

class PokemonCreate(CreateView):
    model = Pokemon
    fields = '__all__'

class  PokemonUpdate(UpdateView):
    model = Pokemon
    fields = ['type', 'description', 'age']

class PokemonDelete(DeleteView):
    model = Pokemon
    success_url = '/pokemons'  

def add_exercise(request, pokemon_id):
    form = ExerciseForm(request.POST)
    if form.is_valid():
        new_exercise = form.save(commit=False)
        new_exercise.pokemon_id = pokemon_id
        new_exercise.save()
    return redirect('detail', pokemon_id=pokemon_id)