from django.contrib.auth.models import User
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models

# TODO
# coach location filed options


class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self) -> str:
        return self.name


class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)

    def __str__(self) -> str:
        return self.user.username


class Coach(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    speciality = models.CharField(max_length=200, default='')
    rating = models.IntegerField(default=0, validators=[
                                 MaxValueValidator(5), MinValueValidator(0)])
    location = models.CharField(max_length=150, default='Egypt')
    price_per_hour = models.IntegerField(default=0)
    price_per_30_mins = models.IntegerField(default=0)
    available_for_kids = models.BooleanField(default=False)
    photo = models.ImageField(upload_to='photo/%Y/%m/%d', blank=True)

    def __str__(self) -> str:
        return self.user.username


class Session(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    coach = models.ForeignKey(Coach, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    time = models.DateTimeField()
    review = models.CharField(max_length=500, default='')

    def __str__(self) -> str:
        return f'{self.category}: {self.coach} - {self.client}'
