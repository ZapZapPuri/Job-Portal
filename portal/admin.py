from django.contrib import admin
from .models import Company, Category, Job, Application

admin.site.register(Company)
admin.site.register(Category)
admin.site.register(Job)
admin.site.register(Application)
