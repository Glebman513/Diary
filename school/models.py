from django.db import models
from django import forms
from datetime import date
from datetime import datetime

class Person(models.Model):
    """
    Абстрактный класс, представляющий человека.
    """
    first_name = models.CharField(max_length=200)
    last_name = models.CharField(max_length=200)
    middle_name = models.CharField(max_length=200, blank=True)  # Добавляем новое поле
    birth_date = models.DateField()

    class Meta:
        abstract = True

    def __str__(self):
        return f'{self.first_name} {self.middle_name} {self.last_name}'  # Добавляем отчество в строковое представление

    def age(self):
        today = date.today()
        return today.year - self.birth_date.year - ((today.month, today.day) < (self.birth_date.month, self.birth_date.day))

class Teacher(Person):
    """
    Модель, представляющая учителя.
    """
    subject = models.ForeignKey('SchoolSubject', on_delete=models.CASCADE)

class Student(Person):
    """
    Модель, представляющая ученика.
    """
    school_class = models.ForeignKey('SchoolClass', on_delete=models.CASCADE)

class Parent(Person):
    """
    Модель, представляющая родителя.
    """
    student = models.ForeignKey('Student', on_delete=models.CASCADE)

class School(models.Model):
    """
    Модель, представляющая школу.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class SchoolSubject(models.Model):
    """
    Модель, представляющая школьный предмет.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class SchoolClass(models.Model):
    """
    Модель, представляющая школьный класс.
    """
    parallel = models.CharField(max_length=1)
    start_year=models.IntegerField(default=2023)

    def grade(self):
        current_year = datetime.now().year
        if int(datetime.now().strftime("%m")) > 8:
            return current_year - self.start_year + 5
        else:
            return current_year - self.start_year + 4
    
    def __str__(self):
        return f'{self.grade()}{self.parallel}'

class SchoolRoom(models.Model):
    """
    Модель, представляющая аудиторию.
    """
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class Lesson(models.Model):
    """
    Модель, представляющая урок.
    """
    subject = models.ForeignKey('SchoolSubject', on_delete=models.CASCADE)
    teacher = models.ForeignKey('Teacher', on_delete=models.CASCADE)
    room = models.ForeignKey('SchoolRoom', on_delete=models.CASCADE)
    date = models.DateField()
    
    def __str__(self):
        return f'{self.subject} ({self.teacher}) {self.date}'

class Grade(models.Model):
    """
    Модель, представляющая оценку на уроке.
    """
    grade = models.IntegerField()
    lesson = models.ForeignKey('Lesson', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)
    
    def __str__(self):
        return f'{self.student}: {self.grade} ({self.lesson})'

class DayGrades(models.Model):
    date = models.DateField()
    grade = models.IntegerField()
    subject = models.ForeignKey('SchoolSubject', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.date} {self.grade} {self.subject}'

class Quarter(models.Model):
    number = models.CharField(max_length=1)
    start_date = models.DateField()
    end_date = models.DateField()

    def __str__(self):
        return f'{self.number}'

class TermGrade(models.Model):
    year = models.IntegerField()
    term = models.ForeignKey('Quarter', on_delete=models.CASCADE)
    grade = models.IntegerField()
    subject = models.ForeignKey('SchoolSubject', on_delete=models.CASCADE)
    student = models.ForeignKey('Student', on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.year} {self.term} {self.subject} {self.student}'

class DaySchedule(models.Model):
    schoolclass = models.ForeignKey('SchoolClass', on_delete=models.CASCADE)
    date = models.DateField()
    day_of_week = models.CharField(
        max_length = 16,
        choices = [
            ('Monday', 'Понедельник'),
            ('Tuesday', 'Вторник'),
            ('Wednesday', 'Среда'),
            ('Thursday', 'Четверг'),
            ('Friday', 'Пятница'),
            ('Saturday', 'Суббота'),
            ('Sunday', 'Воскресенье'),
            ]
            )
    lesson_one = models.ForeignKey('SchoolSubject', related_name="lesson1", on_delete=models.CASCADE, blank=True, default='-')
    lesson_two = models.ForeignKey('SchoolSubject', related_name="lesson2", on_delete=models.CASCADE, blank=True, default='-')
    lesson_three = models.ForeignKey('SchoolSubject', related_name="lesson3", on_delete=models.CASCADE, blank=True, default='-')
    lesson_four = models.ForeignKey('SchoolSubject', related_name="lesson4", on_delete=models.CASCADE, blank=True, default='-')
    lesson_five = models.ForeignKey('SchoolSubject', related_name="lesson5", on_delete=models.CASCADE, blank=True, default='-')
    lesson_six = models.ForeignKey('SchoolSubject', related_name="lesson6", on_delete=models.CASCADE, blank=True, default='-')
    lesson_seven = models.ForeignKey('SchoolSubject', related_name="lesson7", on_delete=models.CASCADE, blank=True, default='-')
    lesson_eight = models.ForeignKey('SchoolSubject', related_name="lesson8", on_delete=models.CASCADE, blank=True, default='-')

    def __str__(self):
        return f'{self.schoolclass} {self.day_of_week}'

