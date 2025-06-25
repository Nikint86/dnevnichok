from datacenter.models import Schoolkid, Mark, Chastisement, Lesson, Commendation
from datetime import date
from random import choice


def fix_bad_marks(student_name):
    student = Schoolkid.objects.filter(full_name__contains=student_name).first()
    if not student:
        return f"Ученик '{student_name}' не найден"

    updated = Mark.objects.filter(
        schoolkid=student,
        points__in=[2, 3]
    ).update(points=5)

    return f"Исправлено {updated} оценок для {student.full_name}"


def remove_chastisements(student_name):
    student = Schoolkid.objects.filter(full_name__contains=student_name).first()
    if not student:
        return f"Ученик '{student_name}' не найден"

    deleted, _ = Chastisement.objects.filter(schoolkid=student).delete()
    return f"Удалено {deleted} замечаний для {student.full_name}"


def praise_student(student_name, subject_title, praise_text=None):
    student = Schoolkid.objects.filter(full_name__contains=student_name).first()
    if not student:
        return f"Ученик '{student_name}' не найден"

    lesson = Lesson.objects.filter(
        year_of_study=student.year_of_study,
        group_letter=student.group_letter,
        subject__title=subject_title
    ).order_by('-date').first()

    if not lesson:
        return f"Уроки по предмету '{subject_title}' не найдены"

    praises = [
        "Отлично справился с заданием!",
        "Проявил творческий подход!",
        "Показал глубокое понимание темы!"
    ]
    text = praise_text or choice(praises)

    Commendation.objects.create(
        text=text,
        created=date.today(),
        schoolkid=student,
        subject=lesson.subject,
        teacher=lesson.teacher
    )

    return f"Добавлена похвала: {text}"