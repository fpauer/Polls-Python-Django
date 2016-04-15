from django.conf.urls import url

from . import views

app_name = 'polls'
urlpatterns = [
    url(r'^login/$', views.login_user, name='login'),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/'}, name='logout'),
    url(r'^register/$', views.register, name='register'),
    url(r'^$', views.IndexView.as_view(), name='index'),
    url(r'^(?P<pk>[0-9]+)/$', views.DetailView.as_view(), name='detail'),
    url(r'^(?P<pk>[0-9]+)/results/$', views.ResultsView.as_view(), name='results'),
    url(r'^(?P<question_id>[0-9]+)/vote/$', views.vote, name='vote'),
    url(r'^polls/(?P<pk>[0-9]+)/$', views.QuestionChoiceList.as_view(), name='question_choices'),
    url(r'^polls/$', views.createQuestion, name='create_question'),
]