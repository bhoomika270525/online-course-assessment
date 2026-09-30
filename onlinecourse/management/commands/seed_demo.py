from datetime import date

from django.core.management.base import BaseCommand
from django.contrib.auth.models import User

from onlinecourse.models import Choice, Course, Enrollment, Lesson, Question


class Command(BaseCommand):
    help = "Create demo data for the final-project assessment."

    def handle(self, *args, **options):
        demo_user, created = User.objects.get_or_create(
            username="demo",
            defaults={
                "first_name": "Demo",
                "last_name": "Learner",
                "email": "demo@example.com",
            },
        )
        if created:
            demo_user.set_password("Demo@12345")
            demo_user.save()

        course, _ = Course.objects.get_or_create(
            name="Django Fundamentals",
            defaults={
                "description": "Learn Django models, views, templates, URLs and assessment workflows.",
                "pub_date": date.today(),
            },
        )

        Lesson.objects.get_or_create(
            course=course,
            order=0,
            defaults={
                "title": "Django Models",
                "content": "Models define the data structure used by a Django application.",
            },
        )
        Lesson.objects.get_or_create(
            course=course,
            order=1,
            defaults={
                "title": "Django Views and Templates",
                "content": "Views process requests and templates render dynamic HTML.",
            },
        )

        q1, _ = Question.objects.get_or_create(
            course=course,
            content="Which file normally contains Django database models?",
            defaults={"grade": 50},
        )
        Choice.objects.get_or_create(
            question=q1, content="models.py",
            defaults={"is_correct": True}
        )
        Choice.objects.get_or_create(
            question=q1, content="urls.py",
            defaults={"is_correct": False}
        )

        q2, _ = Question.objects.get_or_create(
            course=course,
            content="Which Django feature provides the built-in administration interface?",
            defaults={"grade": 50},
        )
        Choice.objects.get_or_create(
            question=q2, content="django.contrib.admin",
            defaults={"is_correct": True}
        )
        Choice.objects.get_or_create(
            question=q2, content="django.contrib.photos",
            defaults={"is_correct": False}
        )

        Enrollment.objects.get_or_create(
            user=demo_user,
            course=course,
            defaults={"mode": "honor"},
        )

        self.stdout.write(self.style.SUCCESS(
            "Demo data ready. Login: demo / Demo@12345"
        ))
