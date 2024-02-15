from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone


class Custom_User(AbstractUser):
    USER=[
        ('viewers','Viewers'),('recipent','Recipent')
    ]
    display_name=models.CharField(max_length=100)
    email=models.EmailField(unique=True)
    password=models.CharField(max_length=100)
    city=models.CharField(max_length=100)
    confirm_password=models.CharField(max_length=100)
    user_type=models.CharField(choices=USER,max_length=120)
    otp_token = models.CharField(max_length=10, null= True, blank=True)
    USERNAME_FIELD='email'
    REQUIRED_FIELDS=['username']
    def __str__(self):
        return self.display_name

class RecipeCategory(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class Recipe(models.Model):
    DIFFICULTY_CHOICES = [
        ('Easy', 'Easy'),
        ('Moderate', 'Moderate'),
        ('Difficult', 'Difficult'),
    ]

    title = models.CharField(max_length=255)
    ingredients = models.TextField()
    instructions = models.TextField()
    preparation_time = models.PositiveIntegerField(help_text="In minutes")
    cooking_time = models.PositiveIntegerField(help_text="In minutes")
    total_time = models.PositiveIntegerField(help_text="In minutes")
    difficulty = models.CharField(max_length=10, choices=DIFFICULTY_CHOICES)
    nutritional_information = models.TextField(blank=True, null=True)
    image = models.ImageField(upload_to='recipe_images/', blank=True, null=True)
    category = models.ManyToManyField(RecipeCategory)
    tags = models.ManyToManyField('Tag', related_name='recipes', blank=True)
    total_calorie = models.PositiveIntegerField()

    def __str__(self):
        return self.title

class Tag(models.Model):
    name = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return self.name

class UserProfile(models.Model):
    user = models.OneToOneField(Custom_User, on_delete=models.CASCADE)

    def __str__(self):
        return self.user.username

class FavoriteRecipe(models.Model):
    user = models.ForeignKey(Custom_User, on_delete=models.CASCADE)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.user.username} - {self.recipe.title}'
