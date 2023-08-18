from django.forms import ModelForm
from .models import Company

class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = [
            'name',
            'sector',
            'risk_qualifier',
            'risk_type',
            'risk_rating'
        ]