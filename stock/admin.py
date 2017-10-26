from django.contrib import admin
from .models import Company, Historical_Price, Ratio

admin.site.register(Company)
admin.site.register(Ratio)
admin.site.register(Historical_Price)