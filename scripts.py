from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation
from datetime import date
from random import choice

PRAISES = [
    "Отлично справился с заданием!",
    "Проявил творческий подход!",
    "Показал глубокое понимание темы!",
    "Блестяще выполнил работу!",
    "Проявил инициативу на уроке!"
]


def get_student(student_name):
    return Schoolkid.objects.get(full_name=student_name)


def get_last_lesson(student, subject_title):
    return Lesson.objects.filter(
        year_of_study=student.year_of_study,
        group_letter=student.group_letter,
        subject__title=subject_title
    ).latest('date')


def fix_bad_marks(student_name):
    student = get_student(student_name)
    updated = Mark.objects.filter(
        schoolkid=student,
        points__in=[2, 3]
    ).update(points=5)
    return f"Исправлено {updated} оценок для {student.full_name}"


def remove_chastisements(student_name):
    student = get_student(student_name)
    deleted, _ = Chastisement.objects.filter(schoolkid=student).delete()
    return f"Удалено {deleted} замечаний для {student.full_name}"


def praise_student(student_name, subject_title, praise_text=None):
    student = get_student(student_name)
    lesson = get_last_lesson(student, subject_title)

    text = praise_text or choice(PRAISES)

    Commendation.objects.create(
        text=text,
        created=date.today(),
        schoolkid=student,
        subject=lesson.subject,
        teacher=lesson.teacher
    )
    return f"Добавлена похвала: {text}"