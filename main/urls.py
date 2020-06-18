from django.urls import path
from .views import \
    user_show,\
    about,\
    stud_question,\
    redirect_user,\
    UserLoginView,\
    UserLogoutView,\
    show_page_question,\
    QuestionCreate,\
    QuestionUpdate,\
    delete_question,\
    detail_check,\
    static_page_answer,\
    static_detail_page

app_name = 'main'
urlpatterns = [
    path('select_user/', redirect_user, name='user_choice'),
    path('stud_question/', stud_question, name='stud'),
    path('auth_teach/', UserLoginView.as_view(), name='teach'),
    path('logout_teach/', UserLogoutView.as_view(), name='logout_teach'),
    path('show_page_question/', show_page_question, name='show_page_question'),
    path('static_page_answer/', static_page_answer, name='static_page_answer'),
    path('static_detail_page/<str:file_text_id>/<str:pk>/', static_detail_page, name='static_detail_page'),
    path('detail_page/<int:pk>', detail_check, name='detail'),
    path('add_question/', QuestionCreate.as_view(), name='add_question'),
    path('update_question/<str:pk>/', QuestionUpdate.as_view(), name='update_question'),
    path('delete_question/<str:pk>/', delete_question, name='delete_question'),
    path('about/', about, name='about'),
    path('', user_show, name='index'),
]
