from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('home', views.main, name='main'),
    path('agendas', views.agendas, name='agendas'),
    path('new', views.new, name='new'),
    path('calendar/<int:agenda_id>', views.calendar_json, name='calendar'),
    path('day/<int:day>/<int:month>/<int:year>/<int:agenda_id>', views.calendar_day, name='day'),
    path('create', views.new_reminder, name='create'),
    path('delete', views.delete_reminder, name='delete'),
    path('scratch/<int:reminder_id>', views.scratch_unscratch, name='scratch')
]