from django.contrib import admin
from .models import Company

class CompanyAdmin(admin.ModelAdmin):
  readonly_fields = ('created', )

# Register your models here.
admin.site.register(Company, CompanyAdmin)