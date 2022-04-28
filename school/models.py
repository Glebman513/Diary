from datetime import datetime
from django.db import models

# Create your models here.

class Grade(models.Model):
    PARALLEL_NOTATIONS = [
        ('a', 'А'),
        ('b', 'Б'),
        ('v', 'В'),
        ('g', 'Г'),
        ]
    parallel = models.CharField(
        'параллель',
        max_length=1,
        choices=PARALLEL_NOTATIONS
        )
    start_year=models.IntegerField(default=2022)

    def calculate_study_year(self):
        current_year = datetime.now().year
        return current_year - self.start_year + 4

    def __str__(self):
        return f'{self.calculate_study_year()}, {self.parallel}'


class Student(models.Model):
    first_name = models.CharField(
        'имя',
        max_length=128
        )
    surname = models.CharField(
        'фамилия',
        max_length=128
        )
    age = models.PositiveIntegerField()

    grade = models.ForeignKey(
        Grade,
        on_delete=models.PROTECT,
        verbose_name='Класс'
        )

    def __str__(self):
        return self.surname + ' ' + self.first_name