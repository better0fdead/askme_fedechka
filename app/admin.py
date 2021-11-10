from django.contrib import admin
from app.models import *
# Register your models here.

admin.site.register(Question)
admin.site.register(Profile)
admin.site.register(Like)
admin.site.register(Tag)
admin.site.register(Comment)