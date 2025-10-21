from django.db import models

# Create your models here.

class Tag(models.Model):
    name = models.CharField(max_length=100, unique=True) # So there cannot be duplicate names.

    def __str__(self):
        return self.name

class Project(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField
    tags = models.ManyToManyField(Tag, related_name="projects") # Many-to-many because many projects can have many tags. 
    link = models.URLField(max_length=200, blank=True) # Blank = True (Ok if no link for project).

    def __str__(self):
        return self.title

# Because we have multiple images per project, we need to create a separate model for the images.
class ProjectImage(models.Model):
    models.ForeignKey(Project, related_name="images", on_delete=models.CASCADE)
    image = models.ImageField(upload_to="project_images/")

    def __str__(self):
        return f"{self.project.title} Image"
    


# *Self-learn note:
    # To create a model, you need to include models.Model in parens to use a single model for the class. 
    # Then, followed by dot notation, what sub-categories do you install? title, textfield, etc.