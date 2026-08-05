from django.db import models
from django.contrib.auth.models import User


class TimeUnit(models.TextChoices):
    MINUTES = 'Minutes', 'Minutos'
    HOURS = 'Hours', 'Horas'
    DAYS = 'Days', 'Dias'


class ServingsUnit(models.TextChoices):
    PIECES = 'Pieces', 'Pedaços'
    PEOPLES = 'Peoples', 'Pessoas'
    SLICES = 'Slices', 'Fatias'
    SERVINGS = 'Servings', 'Porções'
    DISHES = 'Dishes', 'Pratos'
    UNIT = 'Unit', 'Unidades'


class Category(models.Model):
    def __str__(self):
        return self.name

    class Meta:

        verbose_name = 'Category'
        verbose_name_plural = 'Categories'

    name = models.CharField(max_length=65)


class Recipe(models.Model):
    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'Recipe'
        verbose_name_plural = 'Recipes'

    title = models.CharField(max_length=65)
    description = models.CharField(max_length=165)
    slug = models.SlugField()
    preparation_time = models.IntegerField()
    preparation_time_unit = models.CharField(
        max_length=7,
        choices=TimeUnit.choices,
        default=TimeUnit.MINUTES,
    )
    servings = models.IntegerField()
    servings_unit = models.CharField(
        max_length=8,
        choices=ServingsUnit.choices,
        default=ServingsUnit.PIECES,
    )
    preparation_steps = models.TextField()
    preparation_steps_is_html = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    is_published = models.BooleanField(default=False)
    cover = models.ImageField(upload_to='recipes/covers/%Y/%m/%d/')
    category = models.ForeignKey(
        Category,
        on_delete=models.SET_NULL,
        null=True, blank=True, default=None
    )
    author = models.ForeignKey(
        User,
        on_delete=models.SET_NULL,
        null=True,
    )
