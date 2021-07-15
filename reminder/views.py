import calendar
from datetime import date, datetime, timezone, timedelta
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.db import IntegrityError
from django.http import HttpResponse, HttpResponseRedirect, JsonResponse
from django.shortcuts import render
from django.urls import reverse
import json

from .models import User, Agenda, Partner, Reminder

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
            usernameExists = User.objects.filter(username=username)
            emailsExists = User.objects.filter(email=email)
            if len(usernameExists) > 0:
                return render(request, 'reminder/register.html', {
                    'message': 'O nome de usuário inserido já está em uso.'
                })
            elif len(emailsExists) > 0:
                return render(request, 'reminder/register.html', {
                    'message': 'O email inserido já está em uso.'
                })
            user = User.objects.create_user(username, email, password)
            user.save()
        except IntegrityError:
            return render(request, 'reminder/register.html', {
                'message': 'Ocorreu um erro.'
            })
        login(request, user)
        return HttpResponseRedirect(reverse('main'))
    elif request.method == 'GET':
        return render(request, 'reminder/register.html')
    else:
        return JsonResponse({'error': 'GET or POST request required.'}, status=400)

    
@login_required
def actual_user(request):
    if request.method == 'GET':
        actualUser = {
            'user': str(request.user)
        }
        return JsonResponse(actualUser, safe=False)
    else:
        return JsonResponse({'error': 'GET request required.'}, status=400)


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
def partner_calendars(request):
    if request.method == 'GET':
        partner = Partner.objects.filter(user=request.user)
        calendars = []
        for i in range(len(partner)):
            calendar = {
                'id': partner[i].agenda.id,
                'title': partner[i].agenda.title,
                'description': partner[i].agenda.description,
                'color': partner[i].agenda.color,
                'creator': str(partner[i].agenda.creator)
            }
            calendars.append(calendar)
        return JsonResponse(calendars, safe=False)
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
def delete_calendar(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            calendar_id = data.get('calendar',)
            Agenda.objects.get(id=calendar_id, creator=request.user).delete()

            return JsonResponse({'message': 'Calendar deleted successfully.'}, status=201)
        except:
            return JsonResponse({'error': 'Request error'}, status=400)
    else:
        return JsonResponse({'error': 'POST request required.'}, status=400)


@login_required
def exit_calendar(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            calendar_id = data.get('calendar',)

            currentCalendar = Agenda.objects.get(id=calendar_id)

            if currentCalendar.creator == request.user:
                try:
                    partners = Partner.objects.filter(agenda=calendar_id)
                    user = User.objects.get(id=partners[0].user.id)
                    Partner.objects.get(agenda=calendar_id, user=partners[0].user).delete()
                    currentCalendar.creator = user
                    currentCalendar.save()
                except:
                    currentCalendar.delete()
                return JsonResponse({'message': 'Exited from calendar successfully'}, status=201)
            
            Partner.objects.get(agenda=calendar_id, user=request.user).delete()
            
            return JsonResponse({'message': 'Exited from calendar successfully'}, status=201)
        except:
            return JsonResponse({'error': 'Request error'}, status=400)
    else:
        return JsonResponse({'error': 'POST request required.'}, status=400)


@login_required
def kick_calendar(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            
            calendar_id = data.get('calendar',)
            member = data.get('member',)

            user = User.objects.get(username=member)
            Partner.objects.get(agenda=calendar_id, user=user).delete()

            return JsonResponse({'message': 'User kicked from the calendar successfully'}, status=201)
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
        day = datetime.now(timeZoneSP).day

        cal = calendar.HTMLCalendar(calendar.SUNDAY).formatmonth(year, month)
        agenda = Agenda.objects.get(id=agenda_id)
        beg = cal.find('<tr><th colspan')
        end = cal.find('<tr><th class')
        cal = cal[:beg] + cal[end:]
        monthCalendar = {
            'calendar': cal,
            'title': agenda.title,
            'agenda': agenda.id,
            'color': agenda.color,
            'creator': str(agenda.creator),
            'year': year,
            'month': month,
            'day': day
        }
        return JsonResponse(monthCalendar)
    elif request.method == 'POST':
        try:
            data = json.loads(request.body)

            month = data.get('month',)
            year = data.get('year',)
            
            cal = calendar.HTMLCalendar(calendar.SUNDAY).formatmonth(int(year), int(month))
            day = datetime.now().day
            agenda = Agenda.objects.get(id=agenda_id)
            beg = cal.find('<tr><th colspan')
            end = cal.find('<tr><th class')
            cal = cal[:beg] + cal[end:]
            monthCalendar = {
                'calendar': cal,
                'agenda': agenda.id,
                'title': agenda.title,
                'color': agenda.color,
                'creator': str(agenda.creator),
                'year': year,
                'month': month,
                'day': day
            }
            return JsonResponse(monthCalendar)
        except:
            return JsonResponse({'error': 'Request error'}, status=400)
    else:
        return JsonResponse({'error': 'GET or POST request required.'}, status=400)


@login_required
def calendar_day(request, day, month, year, agenda_id):
    if request.method == 'GET':
        day = date(year, month, day)
        
        reminders = Reminder.objects.filter(date=day, agenda=agenda_id)
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
def calendar_member(request, agenda_id):
    if request.method == 'GET':
        calendar = Agenda.objects.get(id=agenda_id)
        data = Partner.objects.filter(agenda=agenda_id).order_by('-user')
        isMember = False
        members = []
        if str(calendar.creator) == str(request.user):
            isMember = True
        member = {
            'user': str(calendar.creator)
        }
        members.append(member)
        for i in data:
            if str(i.user) == str(request.user):
                isMember = True
            member = {
                'user': str(i.user)
            }
            members.append(member)
        if isMember == True:
            return JsonResponse(members, safe=False)
        else:
            return JsonResponse({'error': "You're not a member of this calendar."})
    else:
        return JsonResponse({'error': 'GET request required.'}, status=400)


@login_required
def transfer_admin(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            calendar_id = data.get('calendar',)
            member = data.get('member',)

            currentCalendar = Agenda.objects.get(id=calendar_id)
            calendar = Agenda.objects.get(id=calendar_id, creator=request.user)
            user = User.objects.get(username=member)

            Partner.objects.get(agenda=calendar_id, user=user).delete()
            currentCalendar.creator = user
            currentCalendar.save()
            Partner(agenda=calendar, user=request.user).save()

            return JsonResponse({'message': 'Administrator transfered successfully.', 'owner': str(user)}, status=201)
        except:
            return JsonResponse({'error': 'Request error'}, status=400)
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
        try:
            data = json.loads(request.body)
            calendar = data.get('calendar',)
            reminder = data.get('reminder',)
            try:
                Partner.objects.get(agenda=calendar, user=request.user)
                Reminder.objects.get(id=reminder, agenda=calendar).delete()
            except:
                try:
                    Agenda.objects.get(id=calendar, creator=request.user)
                    Reminder.objects.get(id=reminder, agenda=calendar).delete() 
                except:
                    return JsonResponse({'error': 'Request error'}, status=400)

            return JsonResponse({'message': 'Reminder deleted successfully.'}, status=201)
        except:
            return JsonResponse({'error': 'Request error'}, status=400)
    else:
        return JsonResponse({'error': 'POST request required.'}, status=400)


@login_required
def add_user(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)

            calendar = data.get('calendar',)
            username = data.get('username',)

            if username == str(request.user):
                return JsonResponse({'message': "Você já é membro deste calendário.", 'ok': False}, status=201)

            try:
                agenda = Agenda.objects.get(id=calendar, creator=request.user)

                if request.user != agenda.creator:
                    return JsonResponse({'message': "Você não pode adicionar membros a este calendário pois você não é o administrador.", 'ok': False}, status=201)
                    
                user = User.objects.get(username=username)
                Partner.objects.get(agenda=agenda, user=user)
                return JsonResponse({'message': 'O usuário inserido já é membro deste calendário.', 'ok': False}, status=201)
            except:
                try:
                    agenda = Agenda.objects.get(id=calendar, creator=request.user)
                    user = User.objects.get(username=username)
                    Partner(agenda=agenda, user=user).save()
                except:
                    return JsonResponse({'message': 'O usuário inserido não existe.', 'ok': False}, status=201)

            return JsonResponse({'message': 'Usuário adicionado com sucesso.', 'ok': True}, status=201)
        except:
            return JsonResponse({'error': 'Request error'}, status=400)
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