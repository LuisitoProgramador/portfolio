from django.db import models
from django.db.models.fields import CharField,URLField
from django.db.models.fields.files import ImageField

# Create your models here.

class Project(models.Model):
    title = CharField(max_length=100)
    description = CharField(max_length=150)
    img = ImageField(upload_to='portfolio/images')
    url = URLField(blank=True)
    def __str__(self):
        return self.title
    
    