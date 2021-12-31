import requests
from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from .models import *
from django.http import HttpResponse
from django.db import models
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login
from django.contrib import messages
from django.shortcuts import redirect
from django.contrib.auth.models import User
from django.db.models import Q
from django.core.mail import send_mail
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from StudentProject import settings
from django.contrib.auth import logout
from django.contrib.auth.mixins import LoginRequiredMixin, UserPassesTestMixin
from django.views.generic import (
    ListView,
    DetailView,
    CreateView,
    UpdateView,
    DeleteView,
    UpdateView,
)

# Create your views here.

# class UserQuestionListView(ListView):
#     model = Question
#     template_name = 'Questions/user_Questions.html'  # <app>/<model>_<viewtype>.html
#     context_object_name = 'Question'
#     ordering = ['-date_posted']
#     paginate_by = 5

#     def get_queryset(self):
#         user = get_object_or_s404(User, username=self.kwargs.get(
#             'username'))  # gets the username from url
#         return Question.objects.filter(user=user).order_by("price")


class QuestionListView(ListView):
    model = Question
    # <app>/<model>_<viewtype>.html
    context_object_name = "Question"
    ordering = ["-date_posted"]


def QuestionDetailView(request, pk):
    context = {
        "question": Question.objects.filter(pk=pk).first(),
        "answers": Answer.objects.filter(question__pk=pk),
    }
    return render(request, "main/Question_detail.html", context)


def StudentQuestionListView(request, pk):
    context = {
        "student": Student.objects.filter(user__pk=pk).first(),
        "questions": Question.objects.filter(student__pk=pk),
    }
    print("in student")
    return render(request, "main/profile.html", context)


def StudentAnswerListView(request, pk):
    context = {
        "student": Student.objects.filter(user__pk=pk).first(),
        "answers": Answer.objects.filter(student__pk=pk),
    }
    print("in student")
    return render(request, "main/profile_ans.html", context)


class QuestionCreateView(LoginRequiredMixin, CreateView):
    model = Question
    fields = ["title", "description"]

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


def home_page(request):
    return render(request, "main/home.html")


def login_student(request):
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect("home-page")

        else:
            messages.error(request, "Invalid credentials")
            return redirect("login")

    else:
        return render(request, "main/login.html")


def register_student(request):
    if request.method == "POST":
        username = request.POST.get("username")
        email = request.POST.get("email")
        university = request.POST.get("university")
        year = request.POST.get("g_year")
        password = request.POST.get("password")
        password_again = request.POST.get("confirm_password")

        if password != password_again:
            messages.error(request, "Passwords do not match")
            return redirect("register")

        if User.objects.filter(username=username).exists():
            messages.error(request, "Username taken")
            return redirect("register")

        if User.objects.filter(email=email).exists():
            messages.error(request, "E-Mail taken")
            return redirect("register")

        new_user = User.objects.create_user(
            username=username, email=email, password=password
        )
        new_user.save()

        if University.objects.filter(name=university).exists():
            university_obj = University.objects.filter(name=university).first()

        else:
            university_obj = University(name=university)
            university_obj.save()

        new_student = Student(
            user=new_user, university=university_obj, graduation_year=year
        )
        new_student.save()

        login(request, new_user)

        return redirect("home-page")

    else:
        return render(request, "main/register.html")


def logout_student(request):
    logout(request)
    return redirect("home-page")


@login_required
def answer_question(request, question_pk):
    if request.method == "POST":
        description = request.POST.get("answer")

        new_ans = Answer.objects.create(
            description=description,
            student=request.user,
            question=Question.objects.filter(pk=question_pk).first(),
            date_posted=datetime.datetime.now(),
        )
        new_ans.save()

    return redirect("Questions-list-view")
    # redirect_to = "Question/" + str(question_pk) + "/"
    # return redirect(redirect_to)


@login_required
def display_profile(request):
    context = {
        "student": Student.objects.filter(user__pk=pk).first(),
        "questions": Question.objects.filter(student__pk=pk),
    }
    print("in student")
    return render(request, "main/profile.html", context)


def jobs(request):
    jobs = Job.objects.all()
    return render(request, "main/jobs.html", {"jobs": jobs})


def internship(request):
    internships = Internship.objects.all()
    return render(request, "main/internship.html", {"internships": internships})


@login_required
def ask_referrals(request):
    return render(request, "main/ask_referrals.html")


def new_job(request):
    if request.method == "POST":
        company_name = request.POST.get("company_name")
        position = request.POST.get("position")
        link = request.POST.get("link")
        print(company_name, position, link)
        newJob = Job.objects.create(
            company_name=company_name,
            author=request.user,
            position=position,
            link=link,
            date_posted=datetime.datetime.now(),
        )
        newJob.save()
        return redirect("/jobs")
        # duration = request.POST.get("duration")
        # stipend = request.POST.get("stipend")
        # allowed_batch = request.POST.get("allowed_batch")
    else:
        return render(request, "main/new_job.html")


@login_required
def new_internship(request):
    if request.method == "POST":
        company_name = request.POST.get("company_name")
        position = request.POST.get("position")
        link = request.POST.get("link")
        print(company_name, position, link)
        duration = request.POST.get("duration")
        stipend = request.POST.get("stipend")
        allowed_batch = request.POST.get("allowed_batch")
        newInternship = Internship.objects.create(
            duration=duration,
            stipend=stipend,
            batches_allowed=allowed_batch,
            company_name=company_name,
            author=request.user,
            position=position,
            appln_form=link,
            date_posted=datetime.datetime.now(),
        )
        newInternship.save()
        return redirect("/internship")
    else:
        return render(request, "main/new_internship.html")


@login_required
def new_referral(request):
    if request.method == "POST":
        company_name = request.POST.get("company_name")
        position = request.POST.get("position")
        job_id = request.POST.get("job_id")
        newReferral = Referral.objects.create(
            company_name=company_name,
            posted_by=request.user,
            position=position,
            job_id=job_id,
            date_posted=datetime.datetime.now(),
        )
        newReferral.save()

        messages.success(request, "Request posted successfully")

        return redirect("new_referral")
    else:
        return render(request, "main/new_referral.html")


@login_required
def give_referral(request):
    all_referrals = Referral.objects.filter(status=False).filter(
        ~Q(posted_by=request.user)
    )
    return render(request, "main/give_referral.html", {"referrals": all_referrals})


def add_question(request):
    if request.method == "POST":
        title = request.POST.get("question_title")
        description = request.POST.get("question_description")

        new_question = Question.objects.create(
            title=title,
            description=description,
            student=request.user,
            date_posted=datetime.datetime.now(),
        )
        new_question.save()

    return redirect("Questions-list-view")


def send_mail(subject, html_template, user, context):

    subject = subject
    html_template = html_template
    to_email = user.email
    from_email = settings.DEFAULT_FROM_EMAIL
    html_message = render_to_string(html_template, context)
    message = EmailMessage(subject, html_message, from_email, [to_email])
    message.content_subtype = "html"
    message.send()

    url = "https://email-sender1.p.rapidapi.com/"
    querystring = {
        "txt_msg": "test of the body",
        "to": user.email,
        "from": "one-stop",
        "subject": subject,
        "html_msg": html_message,
    }

    payload = '{\r\n    "key1": "value",\r\n    "key2": "value"\r\n}'
    headers = {
        "content-type": "application/json",
        "x-rapidapi-host": "email-sender1.p.rapidapi.com",
        "x-rapidapi-key": "b5270f85e6mshe7e8deadf438372p19932ejsn5d3cedb41a34",
    }

    response = requests.request(
        "POST", url, data=payload, headers=headers, params=querystring
    )

    print(response.text)


def confirm_referral(request, pk):
    if request.method == "POST":
        message = request.POST.get("r_message")

        curr_referral = Referral.objects.get(pk=pk)

        # Send mail
        send_mail(
            subject="Congrats, Referral Recieved!",
            html_template="main/mail_referral.html",
            user=curr_referral.posted_by,
            context={"msg": message, "ref": curr_referral, "giver": request.user},
        )
        # send to: posted_by
        # sender: we
        # referral giver: current user
        curr_referral.status = True
        curr_referral.save()

    return redirect("give_referral")


@login_required
def new_question(request):
    if request.method == "POST":
        title = request.POST.get("question_title")
        description = request.POST.get("question_description")

        new_question = Question.objects.create(
            title=title,
            description=description,
            student=request.user,
            date_posted=datetime.datetime.now(),
        )
        new_question.save()

        messages.success(request, "Question posted successfully")
        return redirect("new_question")

    else:
        return render(request, "main/new_question.html")


def search(request):
    title = request.GET["question_search"].lower()

    all_question_with_title = Question.objects.filter(
        description__contains=title
    ) | Question.objects.filter(title__contains=title)

    print(all_question_with_title)

    number_of_results = Question.objects.filter(title__contains=title).count()
    all_job_with_company = Job.objects.filter(company_name__contains=title)
    number_of_results += Job.objects.filter(company_name__contains=title).count()

    all_internship_with_company = Internship.objects.filter(
        company_name__contains=title
    )
    number_of_results += Internship.objects.filter(company_name__contains=title).count()

    context = {
        "questions": all_question_with_title,
        "jobs": all_job_with_company,
        "internships": all_internship_with_company,
        "search_title": title,
        "number_questions_found": number_of_results,
    }
    return render(request, "main/search.html", context)
    # return HttpResponse("hello whter")
