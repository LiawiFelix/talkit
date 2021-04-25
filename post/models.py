from django.db import models

# Create your models here.
class Post(models.Model):
    title= models.CharField(max_length=50, null= True, blank= True)
    content= models.TextField(max_length=1000, null= True, blank= True)

    def __str__(self):
        return self.title
    