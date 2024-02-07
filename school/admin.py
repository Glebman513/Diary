from django.contrib import admin
from .models import Teacher, Student, Parent, School, SchoolSubject, SchoolClass, SchoolRoom, Lesson, Grade, DaySchedule, DayGrades, TermGrade, Quarter

admin.site.register(Teacher)
admin.site.register(Student)
admin.site.register(Parent)
admin.site.register(School)
admin.site.register(SchoolSubject)
admin.site.register(SchoolClass)
admin.site.register(SchoolRoom)
admin.site.register(Lesson)
admin.site.register(Grade)
admin.site.register(DaySchedule)
admin.site.register(DayGrades)
admin.site.register(TermGrade)
admin.site.register(Quarter)