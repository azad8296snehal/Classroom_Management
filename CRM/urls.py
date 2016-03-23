from django.conf.urls import url

from . import views

app_name = 'CRM'
urlpatterns = [
    url(r'^$', views.home, name='home'),
    url(r'^index/$', views.index, name='index'),
    url(r'^index_stu/$', views.index_stu, name='index_stu'),
    url(r'^logout/$', views.logout, name='logout'),
    url(r'^BookExtra/$', views.BookExtra, name='BookExtra'),
    url(r'^BookRoom/$', views.BookRoom, name='BookRoom'),
    url(r'^extra_table/$', views.extra_table, name='extra_table'),
    url(r'^book_his/$', views.book_his, name='book_his'),
    url(r'^booksem/$', views.booksem, name='booksem'),
    url(r'^time_table/$', views.time_table, name='time_table'),
    url(r'^sem_his/$', views.sem_his, name='sem_his')
]