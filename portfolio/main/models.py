from django.db import models

# Create your models here.

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField
    tags = models.ManyToManyField(Tag, related_name="projects")
    link = models.URLField(max_length=200, blank=True) # Blank = True (Ok if no link for project)

    def __str__(self):
        return self.title

# *Self-Learn note:
    # To create a model, you need to include models.Model in parens to use a single model for the class. 
    # Then, followed by dot notation, what sub-categories do you install? title, textfield, etc.