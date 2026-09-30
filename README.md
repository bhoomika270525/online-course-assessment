# Online Course Assessment - Django Final Project

This project implements the assessment feature for the IBM/Coursera Django Online Course final project.

## Requirements covered

1. `onlinecourse/models.py` contains `Question`, `Choice`, and `Submission`.
2. `onlinecourse/admin.py` imports seven model classes and implements `QuestionInline`, `ChoiceInline`, `QuestionAdmin`, and `LessonAdmin`.
3. Django admin displays **Authentication and Authorization** and **OnlineCourse**.
4. `course_details_bootstrap.html` displays course name, lessons, and an exam using Django template tags + Bootstrap.
5. `views.py` contains `submit` and `show_exam_result`.
6. `urls.py` contains routes for `submit` and `show_exam_result`.
7. `exam_result_bootstrap.html` displays Congratulations, score, and detailed exam results for a passing attempt.

## Run locally on Windows

```powershell
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
python manage.py makemigrations
python manage.py migrate
python manage.py createsuperuser
python manage.py seed_demo
python manage.py runserver
```

Open:
- Main site: http://127.0.0.1:8000/onlinecourse/
- Admin: http://127.0.0.1:8000/admin/

The `seed_demo` command creates a demo course, lessons, questions, choices, a demo learner, and an enrollment. The demo exam has two 50-point questions. Select all correct choices to get 100/100 and the Congratulations screen.

## Required screenshots

### `03-admin-site.png`
1. Run the server.
2. Log into `/admin/` using your superuser.
3. Capture the admin index page showing both:
   - Authentication and Authorization
   - OnlineCourse
4. Save the screenshot as exactly `03-admin-site.png`.

### `07-final.png`
1. Log into the site as the demo learner (`demo` / `Demo@12345`) or another enrolled user.
2. Open the demo course.
3. Start the exam.
4. Select the correct answer for every question.
5. Submit.
6. Capture the result page showing:
   - Congratulations
   - score (100/100)
   - Exam results
7. Save it as exactly `07-final.png`.

Do not use generated/fake screenshots as assignment evidence. Take the screenshots from the running Django application.

## GitHub submission

Push this whole project to your GitHub repository. Then use the GitHub file URLs for:
- `onlinecourse/models.py`
- `onlinecourse/admin.py`
- `onlinecourse/templates/onlinecourse/course_details_bootstrap.html`
- `onlinecourse/views.py`
- `onlinecourse/urls.py`

Example URL pattern:
`https://github.com/YOUR_USERNAME/YOUR_REPO/blob/main/onlinecourse/models.py`

The assignment asks for URLs to the files, not just the repository homepage.

## Important

This ZIP is a complete standalone implementation. If your course lab originally supplied additional files/features, keep those files when merging this implementation into your lab repository.
