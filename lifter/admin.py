from django.contrib import admin

# Register your models here.
from lifter.models import Lifter
from lifter.models import License
from lifter.models import District
from lifter.models import Club

admin.site.register(Lifter)
admin.site.register(License)
admin.site.register(District)
admin.site.register(Club)