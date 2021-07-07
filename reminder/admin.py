from django.contrib import admin

# Register your models here.
from .models import User, Agenda, Partner, Reminder

admin.site.register(User)
admin.site.register(Agenda)
admin.site.register(Partner)
admin.site.register(Reminder)