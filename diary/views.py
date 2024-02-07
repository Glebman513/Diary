from django.views.generic import ListView
from school.models import Lesson, Grade, DaySchedule, DayGrades, SchoolSubject, TermGrade, Quarter
from datetime import datetime, timedelta
from django.shortcuts import render
import pandas

week_days = [
            ('Monday', 'Понедельник'),
            ('Tuesday', 'Вторник'),
            ('Wednesday', 'Среда'),
            ('Thursday', 'Четверг'),
            ('Friday', 'Пятница'),
            ('Saturday', 'Суббота'),
            ('Sunday', 'Воскресенье'),
            ]

def login(request):
    return 1

def schedule_view(request):
    weekdays = ['Понедельник', 'Вторник', 'Среда', 'Четверг', 'Пятница', 'Суббота', 'Воскресенье']
    schedule = {}
    grades = []
    current_week = datetime.now().isocalendar()[1]
    for day in week_days:
        schedule[day[1]] = DaySchedule.objects.filter(day_of_week = day[0]).first()
    context = {
        'schedule': schedule,
    }
    return render(request, 'schedule.html', context)

def term_grades(request):
    subjects = SchoolSubject.objects.all()
    all_grades = {}
    avg_grade = {}
    start_date = datetime(2023, 12, 1)
    end_date = datetime(2023, 12, 25)
    res = pandas.date_range(
        min(start_date, end_date),
        max(start_date, end_date)
        ).strftime('%Y-%m-%d').tolist()
    date_grades = {}
    for i in subjects:
        all_grades[i] = DayGrades.objects.filter(subject=i)
        avg_grade[i] = DayGrades.objects.filter(subject=i)
        subj_grades = []
        avg_subj_grades = []
        average = 0
        count = 0
        for date in res:
            date_obj = datetime.strptime(date, '%Y-%m-%d').date() 
            current_grades = list(DayGrades.objects.filter(subject=i, date=date_obj).values_list('grade', flat=True))
            grades = ' '.join(map(str, current_grades))
            subj_grades.append(
                grades
            )
            avg_subj_grades.append(
                current_grades
            )
        for j in avg_subj_grades:
            for n in j:
                average += int(n)
        for o in avg_subj_grades:
            if o:
                count +=1
        all_grades[i] = subj_grades
        if count == 0:
            all_grades[i].insert(0, 'Нет оценок')
        else:
            all_grades[i].insert(0, (average/count))
        print(average)
        print(count) 
        print(all_grades)
    context = {
        'avg_grades': avg_grade,
        'all_grades': all_grades,
        'dates': res 
    }
    return render(request, 'term-grades.html', context)


def endterm_grades(request):
    subjects = SchoolSubject.objects.all()
    term_grades = {}
    for i in subjects:
        term_grades[i] = TermGrade.objects.filter(subject=i)
    context = {
        'grades': term_grades,
    }
    return render(request, 'endterm.html', context)
