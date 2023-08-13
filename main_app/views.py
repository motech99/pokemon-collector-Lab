from django.shortcuts import render

pokemons = [
    {'name': 'Squirtle', 'type': 'water', 'description': 'Aqua-shell mischief', 'age': 2},
    {'name': 'Charmander', 'type': 'fire', 'description': 'Fiery-tailed reptile', 'age': 4},
]

# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

def pokemons_index(request):
    return render(request, 'pokemons/index.html', {
        'pokemons': pokemons
    })
