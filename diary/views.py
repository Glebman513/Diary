from django.views.generic import ListView
from school.models import Lesson, Grade, DaySchedule, DayGrades, SchoolSubject, TermGrade, Quarter, Student
from datetime import datetime, timedelta
from django.shortcuts import render
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, models
from .forms import LoginForm
from django.http import HttpResponseRedirect
import pandas
import statistics

week_days = [
            ('Monday', 'Понедельник'),
            ('Tuesday', 'Вторник'),
            ('Wednesday', 'Среда'),
            ('Thursday', 'Четверг'),
            ('Friday', 'Пятница'),
            ('Saturday', 'Суббота'),
            ('Sunday', 'Воскресенье'),
            ]

#def login(request):
 #   return 1

def schedule_view(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect('http://127.0.0.1:8000/accounts/login/')
    schedule = {}
    for day in week_days:
        schedule[day[1]] = DaySchedule.objects.filter(day_of_week = day[0]).first()
    context = {
        'schedule': schedule,
    }
    return render(request, 'schedule.html', context)

def term_grades(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect('http://127.0.0.1:8000/accounts/login/')
    subjects = SchoolSubject.objects.all()
    all_grades = {}
    avg_grade = {}
    start_date = datetime(2023, 12, 1)
    end_date = datetime(2023, 12, 25)
    res = pandas.date_range(
        min(start_date, end_date),
        max(start_date, end_date)
        ).strftime('%Y-%m-%d').tolist()
    for i in subjects:
        all_grades[i] = DayGrades.objects.filter(subject=i, student__user=user)
        avg_grade[i] = DayGrades.objects.filter(subject=i, student__user=user)
        subj_grades = []
        avg_subj_grades = []
        for date in res:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date() 
            current_grades = list(DayGrades.objects.filter(subject=i, date=date_obj, student__user=user).values_list('grade', flat=True))
            grades = ' '.join(map(str, current_grades))
            subj_grades.append(
                grades
            )
            avg_subj_grades.append(
                current_grades
            )
        all_grades[i] = subj_grades
        avg_subj_grades = [item for sublist in avg_subj_grades for item in sublist]
        if not avg_subj_grades:
            all_grades[i].insert(0, 'Нет оценок')
        else:
            all_grades[i].insert(0, round(statistics.mean(avg_subj_grades), 2))
        print(all_grades)
    context = {
        'avg_grades': avg_grade,
        'all_grades': all_grades,
        'dates': res 
    }
    return render(request, 'term-grades.html', context)


def endterm_grades(request):
    user = request.user
    if not user.is_authenticated:
        return HttpResponseRedirect('http://127.0.0.1:8000/accounts/login/')
    subjects = SchoolSubject.objects.all()
    term_grades = {}
    quarters = ('1', '2', '3', '4')
    for i in subjects:
        term_grades[i] = TermGrade.objects.filter(subject=i, student__user=user)
        subj_grades = []
        for quarter in quarters: 
            current_grades = list(TermGrade.objects.filter(subject=i, term=quarter, student__user=user).values_list('grade', flat=True))
            grades = ' '.join(map(str, current_grades))
            subj_grades.append(
                grades
            )
        term_grades[i] = subj_grades
    context = {
        'term_grades': term_grades,
        'quarters': quarters 
    }
    return render(request, 'endterm.html', context)
