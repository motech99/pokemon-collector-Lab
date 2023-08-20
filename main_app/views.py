import os
import uuid
import boto3
from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from .models import Pokemon, Trainer, Photo
from .forms import ExerciseForm
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin


# Create your views here.
def home(request):
    return render(request, 'home.html')

def about(request):
    return render(request, 'about.html')

@login_required
def pokemons_index(request):
    pokemons = Pokemon.objects.filter(user=request.user)
    return render(request, 'pokemons/index.html', {
        'pokemons': pokemons
    })

@login_required
def pokemons_detail(request, pokemon_id):
    pokemon = Pokemon.objects.get(id=pokemon_id)
    id_list = pokemon.trainers.all().values_list('id')
    trainers_pokemon_doesnt_have = Trainer.objects.exclude(id__in=id_list)
    exercise_form = ExerciseForm()
    return render(request, 'pokemons/detail.html', {
        'pokemon': pokemon, 'exercise_form': exercise_form,
        'trainers': trainers_pokemon_doesnt_have
    })

class PokemonCreate(LoginRequiredMixin, CreateView):
    model = Pokemon
    fields = ['name', 'type', 'description', 'age']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)

class  PokemonUpdate(LoginRequiredMixin, UpdateView):
    model = Pokemon
    fields = ['type', 'description', 'age']

class PokemonDelete(LoginRequiredMixin, DeleteView):
    model = Pokemon
    success_url = '/pokemons'  

@login_required
def add_exercise(request, pokemon_id):
    form = ExerciseForm(request.POST)
    if form.is_valid():
        new_exercise = form.save(commit=False)
        new_exercise.pokemon_id = pokemon_id
        new_exercise.save()
    return redirect('detail', pokemon_id=pokemon_id)

class TrainerList(LoginRequiredMixin, ListView):
  model = Trainer

class TrainerDetail(LoginRequiredMixin, DetailView):
  model = Trainer

class TrainerCreate(LoginRequiredMixin, CreateView):
  model = Trainer
  fields = '__all__'

class TrainerUpdate(LoginRequiredMixin, UpdateView):
  model = Trainer
  fields = ['name', 'team']

class TrainerDelete(LoginRequiredMixin, DeleteView):
  model = Trainer
  success_url = '/trainers'

@login_required
def assoc_trainer(request, pokemon_id, trainer_id):
    Pokemon.objects.get(id=pokemon_id).trainers.add(trainer_id)
    return redirect('detail', pokemon_id=pokemon_id)

@login_required
def unassoc_trainer(request, pokemon_id, trainer_id):
    Pokemon.objects.get(id=pokemon_id).trainers.remove(trainer_id)
    return redirect('detail', pokemon_id=pokemon_id)

@login_required
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


def signup(request):
  error_message = ''
  form = UserCreationForm(request.POST)
  if request.method == 'POST':
    if form.is_valid():
      user = form.save()
      login(request, user)
      return redirect('index')
    else:
      error_message = 'Invalid sign up - try again'
  context = {'form': form, 'error_message': error_message}
  return render(request, 'registration/signup.html', context)


