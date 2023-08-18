from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib.auth.models import User
from django.db import IntegrityError
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from .models import Company
from .forms import CompanyForm

from django.core.serializers import serialize
from django.http import HttpResponse

# Create your views here.
# Main public view
def home(request):
    return render(request, 'home.html')

def home_data_json(request):
    if request.method == 'GET':
        data = Company.objects.all()
        data = serialize("json", data, fields=('name', 'sector', 'risk_rating'))
        return HttpResponse(data, content_type="application/json")
    
def company_data_json(request, company_id):
    if request.method == 'GET':
        data = Company.objects.filter(pk=company_id)
        if len(data) == 1:
            data = serialize("json", data, fields=('name','sector','risk_rating'))
        else:
            data = [{"code":"500", "message": "No hemos encontrado la información de la empresa"}]

    return HttpResponse(data, content_type="application/json")

# REGISTER (create a new user account)
def signup(request):
    if request.method == 'GET':
        return render(request, 'signup.html', {"form": UserCreationForm})
    else:

        if request.POST["password1"] == request.POST["password2"]:
            try:
                user = User.objects.create_user(
                    request.POST["username"], password=request.POST["password1"])
                user.save()
                login(request, user)
                return redirect('companies')
            except IntegrityError:
                return render(request, 'signup.html', {"form": UserCreationForm, "error": "El nombre de usuario ya existe."})

        return render(request, 'signup.html', {"form": UserCreationForm, "error": "Las contraseñas no coinciden."})

# LOGIN
def signin(request):
    if request.method == 'GET':
        return render(request, 'signin.html', {"form": AuthenticationForm})
    else:
        user = authenticate(
            request, username=request.POST['username'], password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html', {"form": AuthenticationForm, "error": "Usuario o contraseña incorrectos."})

        login(request, user)
        return redirect('companies')
    
# LOGOUT (close session)
@login_required
def signout(request):
    logout(request)
    return redirect('home')

# GET ALL COMPANIES
@login_required
def companies(request):
    companies = Company.objects.filter(user=request.user)
    return render(request, 'companies.html', {"data": companies})

# CREATE COMPANIES
@login_required
def company_create(request):
    if request.method == "GET":
        return render(request, 'company_create.html', {"form": CompanyForm})
    else:
        try:
            form = CompanyForm(request.POST)
            new_company = form.save(commit=False)
            new_company.user = request.user
            new_company.save()
            return redirect('companies')
        except ValueError:
            return render(request, 'company_create.html', {
                "form": CompanyForm, 
                "error": "Ocurrio un error al crear la empresa."
            })
 
# GET A COMPANY BY ID
@login_required
def company_detail(request, company_id):
    if request.method == 'GET':
        company = get_object_or_404(Company, pk=company_id, user=request.user)
        form = CompanyForm(instance=company)
        return render(request, 'company_detail.html', {
            'data': company, 'form': form
        })
    else:
        try:
            company = get_object_or_404(Company, pk=company_id, user=request.user)
            form = CompanyForm(request.POST, instance=company)
            form.save()
            return redirect('companies')
        except ValueError:
            return render(request, 'company_detail.html', {
                'company': company, 'form': form, 'error': 'Ocurrio un error al actualizar la empresa.'
            })

# DELETE A COMPANY
@login_required
def company_delete(request, company_id):
    company = get_object_or_404(Company, pk=company_id, user=request.user)
    if request.method == 'POST':
        company.delete()
        return redirect('companies')