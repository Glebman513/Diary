from django.views.generic import ListView
from school.models import Lesson, Grade
from datetime import datetime, timedelta
from django.shortcuts import render

from django.utils import timezone

def week_schedule(request):
    now = timezone.now()
    start_of_week = now - timezone.timedelta(days=now.weekday())
    end_of_week = start_of_week + timezone.timedelta(days=6)
    lessons = Lesson.objects.filter(date__gte=start_of_week, date__lte=end_of_week)
    grades = Grade.objects.filter(lesson__in=lessons)
    return render(request, 'week_schedule.html', {'lessons': lessons, 'grades': grades})