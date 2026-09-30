import logging

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse
from django.views import generic

from .models import Choice, Course, Enrollment, Question, Submission

logger = logging.getLogger(__name__)


def extract_answers(request):
    submitted_answers = []
    for key, value in request.POST.items():
        if key.startswith("choice_"):
            submitted_answers.append(int(value))
    return submitted_answers


def submit(request, course_id):
    if not request.user.is_authenticated:
        return redirect("onlinecourse:login")

    course = get_object_or_404(Course, pk=course_id)
    enrollment = get_object_or_404(
        Enrollment, user=request.user, course=course
    )

    submission = Submission.objects.create(enrollment=enrollment)
    selected_choice_ids = extract_answers(request)
    choices = Choice.objects.filter(id__in=selected_choice_ids)
    submission.choices.set(choices)

    return HttpResponseRedirect(
        reverse(
            "onlinecourse:exam_result",
            args=(course_id, submission.id),
        )
    )


def show_exam_result(request, course_id, submission_id):
    course = get_object_or_404(Course, pk=course_id)
    submission = get_object_or_404(
        Submission, pk=submission_id, enrollment__course=course
    )
    choices = submission.choices.all()

    total_score = 0
    question_results = []

    for question in course.question_set.all().order_by("id"):
        correct_choices = set(
            question.choice_set.filter(is_correct=True)
        )
        selected_choices = set(
            choices.filter(question=question)
        )
        is_correct = correct_choices == selected_choices
        if is_correct:
            total_score += question.grade

        question_results.append(
            {
                "question": question,
                "choices": question.choice_set.all(),
                "selected_choices": selected_choices,
                "is_correct": is_correct,
            }
        )

    context = {
        "course": course,
        "grade": total_score,
        "choices": choices,
        "question_results": question_results,
    }
    return render(
        request,
        "onlinecourse/exam_result_bootstrap.html",
        context,
    )


def registration_request(request):
    context = {}
    if request.method == "GET":
        return render(request, "onlinecourse/user_registration_bootstrap.html", context)

    username = request.POST.get("username", "").strip()
    password = request.POST.get("psw", "")
    first_name = request.POST.get("firstname", "")
    last_name = request.POST.get("lastname", "")

    if User.objects.filter(username=username).exists():
        context["message"] = "User already exists."
        return render(request, "onlinecourse/user_registration_bootstrap.html", context)

    user = User.objects.create_user(
        username=username,
        first_name=first_name,
        last_name=last_name,
        password=password,
    )
    login(request, user)
    return redirect("onlinecourse:index")


def login_request(request):
    context = {}
    if request.method == "POST":
        username = request.POST.get("username", "")
        password = request.POST.get("psw", "")
        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("onlinecourse:index")

        context["message"] = "Invalid username or password."

    return render(request, "onlinecourse/user_login_bootstrap.html", context)


def logout_request(request):
    logout(request)
    return redirect("onlinecourse:index")


def check_if_enrolled(user, course):
    if not user.is_authenticated:
        return False
    return Enrollment.objects.filter(user=user, course=course).exists()


class CourseListView(generic.ListView):
    template_name = "onlinecourse/course_list_bootstrap.html"
    context_object_name = "course_list"

    def get_queryset(self):
        courses = Course.objects.order_by("-total_enrollment")[:10]
        for course in courses:
            course.is_enrolled = check_if_enrolled(self.request.user, course)
        return courses


class CourseDetailView(generic.DetailView):
    model = Course
    template_name = "onlinecourse/course_details_bootstrap.html"


def enroll(request, course_id):
    course = get_object_or_404(Course, pk=course_id)
    if request.user.is_authenticated:
        Enrollment.objects.get_or_create(
            user=request.user,
            course=course,
            defaults={"mode": "honor"},
        )
        course.total_enrollment += 1
        course.save(update_fields=["total_enrollment"])
    return HttpResponseRedirect(
        reverse("onlinecourse:course_details", args=(course.id,))
    )
