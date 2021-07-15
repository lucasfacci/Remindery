from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('login', views.login_view, name='login'),
    path('logout', views.logout_view, name='logout'),
    path('register', views.register, name='register'),
    path('actual_user', views.actual_user, name='actual_user'),
    path('home', views.main, name='main'),
    path('agendas', views.agendas, name='agendas'),
    path('partner_calendars', views.partner_calendars, name='partner_calendars'),
    path('new', views.new, name='new'),
    path('delete_calendar', views.delete_calendar, name='delete_calendar'),
    path('exit_calendar', views.exit_calendar, name='exit_calendar'),
    path('kick_calendar', views.kick_calendar, name='kick_calendar'),
    path('calendar/<int:agenda_id>', views.calendar_json, name='calendar'),
    path('day/<int:day>/<int:month>/<int:year>/<int:agenda_id>', views.calendar_day, name='day'),
    path('member/<int:agenda_id>', views.calendar_member, name='member'),
    path('create', views.new_reminder, name='create'),
    path('delete', views.delete_reminder, name='delete'),
    path('add_user', views.add_user, name='add_user'),
    path('scratch/<int:reminder_id>', views.scratch_unscratch, name='scratch')
]