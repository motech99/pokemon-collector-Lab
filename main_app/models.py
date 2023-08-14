from django.db import models
from django.urls import reverse 
from datetime import date

TRAINING = (
    ('S', 'Stamina'),
    ('D', 'Defense'),
    ('B', 'Bonding')
 )

# Create your models here.
class Pokemon(models.Model):
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)
    description = models.TextField(max_length=100)
    age = models.IntegerField()


    def __str__(self):
        return f'{self.name} ({self.id})'
    
    def get_absolute_url(self):
        return reverse('detail', kwargs={'pokemon_id': self.id})
    
    def trained_for_today(self):
        return self.training_set.filter(date=date.today()).count() >= len(TRAINING)

    

class Exercise(models.Model):
    date = models.DateField('training date')
    training = models.CharField(
        max_length=1,
        choices=TRAINING,
        default=TRAINING[0][0]
        )
    pokemon = models.ForeignKey(
        Pokemon,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f"{self.get_training_display()} on {self.date}"

    class Meta:
        ordering = ['-date']
    




