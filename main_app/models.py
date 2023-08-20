from django.db import models
from django.urls import reverse 
from datetime import date
from django.contrib.auth.models import User

TRAINING = (
    ('S', 'Stamina'),
    ('D', 'Defense'),
    ('B', 'Bonding'),
 )
TEAMS = (
    ('V', 'Valor'),
    ('M', 'Mystic'),
    ('I', 'Instinct'),
)


# Create your models here.
class Trainer(models.Model):
    name = models.CharField(max_length=50)
    team = models.CharField(
        max_length=1,
        choices=TEAMS,
        default=TEAMS[0][0]
    )

    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('trainers_detail', kwargs={'pk': self.id})


class Pokemon(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    age = models.IntegerField()
    trainers = models.ManyToManyField(Trainer)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'pokemon_id': self.id})
    
    def trained_for_today(self):
        return self.exercise_set.filter(date=date.today()).count() >= len(TRAINING)
    

class Exercise(models.Model):
    date = models.DateField('training date')
    training = models.CharField(
        max_length=1,
        choices=TRAINING,
        default=TRAINING[0][0]
     )
    pokemon = models.ForeignKey(
        'Pokemon',
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.get_training_display()} on {self.date}"

    class Meta:
        ordering = ['-date']
    

class Photo(models.Model):
    url = models.CharField(max_length=200)
    pokemon = models.ForeignKey(Pokemon, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for pokemon_id: {self.pokemon_id} @{self.url}"



