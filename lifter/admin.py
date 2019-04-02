from django.contrib import admin

# Register your models here.
from .models import Lifter
from .models import License
from .models import District
from .models import Club

admin.site.register(Lifter)
admin.site.register(License)
admin.site.register(District)
admin.site.register(Club)