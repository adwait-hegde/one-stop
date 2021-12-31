from django.urls import path
from django.contrib.auth import views as auth_views
from .views import *


urlpatterns = [
    path("", home_page, name="home-page"),
    path("jobs", jobs, name="jobs"),
    path("new_question", new_question, name="new_question"),
    path("new_job", new_job, name="new_job"),
    path("confirm_referral/<int:pk>", confirm_referral, name="confirm_referral"),
    path("internship", internship, name="internship"),
    path("new_internship", new_internship, name="new_internship"),
    path("new_referral", new_referral, name="new_referral"),
    path("give_referral", give_referral, name="give_referral"),
    path("login", login_student, name="login"),
    path("register", register_student, name="register"),
    path("profile", display_profile, name="profile"),
    path("logout", logout_student, name="logout"),
    path("Questions", QuestionListView.as_view(), name="Questions-list-view"),
    path("Question/<int:pk>/", QuestionDetailView, name="Questions-detail"),
    path(
        "Student/question/<int:pk>/",
        StudentQuestionListView,
        name="Student-question-list",
    ),
    path(
        "Student/answer/<int:pk>/",
        StudentAnswerListView,
        name="Student-answer-list",
    ),
    path("answers/<int:question_pk>/", answer_question, name="answers"),
    path("add_question/", add_question, name="add_question"),
    path("questions/search/", search, name="question_search"),
    # path("jobs", )
    # path('about/', views.about, name="books-about"),
]

# path('Question/new/', QuestionCreateView.as_view(), name="Questions-create"),
# path('Question/<int:pk>/update/', QuestionUpdateView.as_view(), name="Questions-update"),
# path('Question/<int:pk>/delete/', QuestionDeleteView.as_view(), name="Questions-delete"),
# path('Question/search/', views.search, name="Questions-search"),
