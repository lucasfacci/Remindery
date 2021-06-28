import calendar
from datetime import date, datetime, timezone, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json

from .models import User, Agenda, Reminder

def index(request):
    if request.method == 'GET':
        if request.user.is_authenticated:
            return HttpResponseRedirect(reverse('main'))
        else:
            return render(request, 'reminder/index.html')
    else:
        return JsonResponse({'error': 'GET request required.'}, status=400)


def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return HttpResponseRedirect(reverse('main'))
        else:
            return render(request, 'reminder/login.html', {
                'message': 'Usuário e/ou senha inválido(s).'
            })
    elif request.method == 'GET':
        return render(request, 'reminder/login.html')
    else:
        return JsonResponse({'error': 'GET or POST request required.'}, status=400)


def logout_view(request):
    if request.method == 'GET':
        logout(request)
        return HttpResponseRedirect(reverse('index'))
    else:
        return JsonResponse({'error': 'GET request required.'}, status=400)

def register(request):
    if request.method == 'POST':
        username = request.POST["username"]
        email = request.POST['email']
        password = request.POST['password']
        confirmation = request.POST['confirmation']

        if password != confirmation:
            return render(request, 'reminder/register.html', {
                'message': 'As senhas não se correspondem.'
            })

        try:
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'reminder/register.html', {
                'message': 'Este email já foi utilizado.'
            })
        login(request, user)
        return HttpResponseRedirect(reverse('main'))
    elif request.method == 'GET':
        return render(request, 'reminder/register.html')
    else:
        return JsonResponse({'error': 'GET or POST request required.'}, status=400)


@login_required
def main(request):
    if request.method == 'GET':
        return render(request, 'reminder/main.html')
    else:
        return JsonResponse({'error': 'GET request required.'}, status=400)


@login_required
def agendas(request):
    if request.method == 'GET':
        data = Agenda.objects.filter(creator=request.user)
        agendas = []
        for i in data:
            agenda = {
                'id': i.id,
                'title': i.title,
                'description': i.description,
                'color': i.color,
                'creator': str(i.creator)
            }
            agendas.append(agenda)
        return JsonResponse(agendas, safe=False)
    else:
        return JsonResponse({'error': 'GET request required.'}, status=400)


@login_required
def new(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            title = data.get('title',)
            description = data.get('description',)
            color = data.get('color',)

            if title == '' or color == '':
                return JsonResponse({'error': 'Empty input'}, status=400)

            Agenda(title=title, description=description, color=color, creator=request.user).save()
            return JsonResponse({'message': 'Agenda created successfully.'}, status=201)
        except:
            return JsonResponse({'error': 'Request error'}, status=400)
    else:
        return JsonResponse({'error': 'POST request required.'}, status=400)


@login_required
def calendar_json(request, agenda_id):
    if request.method == 'GET':
        difference = timedelta(hours = -3)
        timeZoneSP = timezone(difference)
        year = datetime.now(timeZoneSP).year
        month = datetime.now(timeZoneSP).month

        cal = calendar.HTMLCalendar(calendar.SUNDAY).formatmonth(year, month)
        agenda = Agenda.objects.get(id=agenda_id)
        monthCalendar = {
            "calendar": cal,
            "agenda": agenda.id,
            "year": year,
            "month": month
        }
        return JsonResponse(monthCalendar)
    else:
        return JsonResponse({'error': 'GET request required.'}, status=400)


@login_required
def calendar_day(request, day, month, year, agenda_id):
    if request.method == 'GET':
        day = date(year, month, day)
        
        reminders = Reminder.objects.filter(date=day, creator=request.user, agenda=agenda_id)
        remindersJson = []

        if len(reminders) > 0:
            for reminder in reminders:
                weekDay = datetime.weekday(reminder.date)
                if weekDay == 0:
                    weekDay = 'Segunda-feira'
                elif weekDay == 1:
                    weekDay = 'Terça-feira'
                elif weekDay == 2:
                    weekDay = 'Quarta-feira'
                elif weekDay == 3:
                    weekDay = 'Quinta-feira'
                elif weekDay == 4:
                    weekDay = 'Sexta-feira'
                elif weekDay == 5:
                    weekDay = 'Sábado'
                elif weekDay == 6:
                    weekDay = 'Domingo'
                dateBrasil = reminder.date.strftime('%d/%m/%Y')
                reminderJson = {
                    'reminder': reminder.id,
                    'content': reminder.content,
                    'scratched': reminder.scratched,
                    'date': dateBrasil,
                    'weekDay': weekDay
                }
                remindersJson.append(reminderJson)
        else:
            weekDay = datetime.weekday(day)
            dateBrasil = day.strftime('%d/%m/%Y')
            if weekDay == 0:
                weekDay = 'Segunda-feira'
            elif weekDay == 1:
                weekDay = 'Terça-feira'
            elif weekDay == 2:
                weekDay = 'Quarta-feira'
            elif weekDay == 3:
                weekDay = 'Quinta-feira'
            elif weekDay == 4:
                weekDay = 'Sexta-feira'
            elif weekDay == 5:
                weekDay = 'Sábado'
            elif weekDay == 6:
                weekDay = 'Domingo'
            reminderJson = {
                'date': dateBrasil,
                'weekDay': weekDay
            }
            remindersJson.append(reminderJson)
        return JsonResponse(remindersJson, safe=False)
    else:
        return JsonResponse({'error': 'GET request required.'}, status=400)


@login_required
def new_reminder(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            content = data.get('content',)
            agenda = data.get('agenda',)
            day = int(data.get('day',))
            month = int(data.get('month',))
            year = int(data.get('year',))

            thisDate = date(year, month, day)
            agenda = Agenda.objects.get(id=agenda)

            Reminder(content=content, date=thisDate, creator=request.user, agenda=agenda).save()
            return JsonResponse({'message': 'Reminder created successfully.'}, status=201)
        except:
            return JsonResponse({'error': 'Request error'}, status=400)
    else:
        return JsonResponse({'error': 'POST request required.'}, status=400)


@login_required
def delete_reminder(request):
    if request.method == 'POST':
        pass
    else:
        return JsonResponse({'error': 'POST request required.'}, status=400)


@login_required
def scratch_unscratch(request, reminder_id):
    if request.method == 'PUT':
        reminder = Reminder.objects.get(creator=request.user, id=reminder_id)
        data = json.loads(request.body)
        if data.get('scratched',) is not None:
            reminder.scratched = data['scratched']
        reminder.save()
        return HttpResponse(status=204)
    else:
        return JsonResponse({'error': 'PUT request required.'}, status=400)