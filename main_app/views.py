import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Pokemon, Trainer, Photo
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
    id_list = pokemon.trainers.all().values_list('id')
    trainers_pokemon_doesnt_have = Trainer.objects.exclude(id__in=id_list)
    exercise_form = ExerciseForm()
    return render(request, 'pokemons/detail.html', {
        'pokemon': pokemon, 'exercise_form': exercise_form,
        'trainers': trainers_pokemon_doesnt_have
    })

class PokemonCreate(CreateView):
    model = Pokemon
    fields = ['name', 'type', 'description', 'age']

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

class TrainerList(ListView):
  model = Trainer

class TrainerDetail(DetailView):
  model = Trainer

class TrainerCreate(CreateView):
  model = Trainer
  fields = '__all__'

class TrainerUpdate(UpdateView):
  model = Trainer
  fields = ['name', 'team']

class TrainerDelete(DeleteView):
  model = Trainer
  success_url = '/trainers'

def assoc_trainer(request, pokemon_id, trainer_id):
    Pokemon.objects.get(id=pokemon_id).trainers.add(trainer_id)
    return redirect('detail', pokemon_id=pokemon_id)

def unassoc_trainer(request, pokemon_id, trainer_id):
    Pokemon.objects.get(id=pokemon_id).trainers.remove(trainer_id)
    return redirect('detail', pokemon_id=pokemon_id)

def add_photo(request, pokemon_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, pokemon_id=pokemon_id)
        except Exception as e:
            print('An error occurred uploading file to S3')
            print(e)
    return redirect('detail', pokemon_id=pokemon_id)