from django.contrib.auth.models import User
from django.db import models

from datetime import date

class Icon(models.Model):
    name = models.CharField(max_length=200)
    categories = (
        ('logo', 'logo'),
        ('basic', 'basic'),
        ('special', 'special')
    )
    category = models.CharField(max_length=17, choices=categories)
    statuses = (
        ('published', 'published'),
        ('not published', 'not published'),
    )
    status = models.CharField(max_length=17, choices=statuses)
    svg_filepath = models.CharField(max_length=255)
    png_filepath = models.CharField(max_length=255)
    date_added = models.DateTimeField(auto_now_add=True)
    buyers = models.ManyToManyField(User, blank=True)

    def __str__(self):
        """Возвращает строковое представление модели."""
        return self.name


class License(models.Model):
    date_created = models.DateTimeField(auto_now_add=True)
    owner = models.OneToOneField(User, on_delete=models.CASCADE)
    date_ended = models.DateField()

    @property
    def remaining_days(self):
        today = date.today()
        result = self.date_ended - today
        return result.days

    @property
    def end_of_license(self):
        return self.remaining_days <= 0