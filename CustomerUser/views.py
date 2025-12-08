from django.shortcuts import render,redirect
from django.views.generic import FormView, TemplateView
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import CustomerUser, CallRegister
from Company.models import Company
from Demand.models import Demand
from .forms import LoginForm,CallRegisterForm
from django.contrib import messages
from datetime import date
from django.db import models
# Create your views here.

class LoginView(FormView):
    template_name = 'login/login.html'
    success_url = '/user/home'
    form_class = LoginForm
        
    def form_valid(self, form):
        email = form.cleaned_data.get('email')
        password = form.cleaned_data.get('password')
        userCustomer = CustomerUser.objects.get(user__email=email).user
        user = authenticate(self.request, username=userCustomer, password=password)
        if user is not None:
            login(self.request, user)
            self.request.session['userAuthCustomerID'] = userCustomer.id
            self.request.session['userAuthDefaultID'] = user.id
            return redirect('home')
        else:
            return HttpResponse("Invalid credentials")  #TODO: Change to error message in form
    def form_invalid(self, form):
        pass
        return super().form_invalid(form)

class HomeView(TemplateView ):
    template_name = 'home/home.html'

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        callRegister = CallRegister.objects.filter(user__user=self.request.user)
        context['qtdCalls'] = callRegister.filter(dateCall=date.today()).count()
        context['totalValue'] = callRegister.filter(dateCall=date.today()).aggregate(models.Sum('value'))['value__sum'] or 0.00
        return context

class RegisterPainel(TemplateView):
    template_name = 'registerPainel/registerPainel.html'
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        return context
    
class CallRegisterView(FormView):
    template_name = 'callRegister/callRegister.html'
    form_class = CallRegisterForm
    success_url = '/'
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['form'] = CallRegisterForm()
        return context
    
    def form_valid(self, form):        
        dateCall = form.cleaned_data.get('dateCall')
        compamy = form.cleaned_data.get('company')
        demand = form.cleaned_data.get('demand')
        colaborator = form.cleaned_data.get('collaborator')
        observation = form.cleaned_data.get('observation')
        numberValue = form.cleaned_data.get('value')
        userAuth = self.request.session.get('userAuthCustomerID')

        call = createCallRegister(userAuth,dateCall, compamy, demand, colaborator, observation,numberValue )
        try:
            if call is not None:
                call.save()
                messages.add_message(self.request, messages.SUCCESS, 'Chamado cadastrado com sucesso!')
        except Exception as e:
            print("ERRO AO SALVAR CALLREGISTER: ", str(e))
            messages.add_message(self.request, messages.ERROR, 'Erro ao cadastrar o chamado.')
        return redirect('callRegister')
    
    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Erro ao cadastrar o chamado. Verifique os dados informados.')
        return super().form_invalid(form)
    
class LogoutView(TemplateView):
    template_name = 'login/login.html'
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')

class ReportsView(TemplateView):
    template_name = 'reports/reports.html'
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['demands'] = Demand.objects.all().order_by('description')
        context['companys'] = Company.objects.all().order_by('name')
        context['calls'] = CallRegister.objects.filter(user__user=self.request.user).order_by('-dateCall')
        return context


#Funcitions
def createCallRegister(userAuth,dateCallParam, companyName, demandDescription, colaboratorParam, observationParam, numberValueParam):
    customerUser = CustomerUser.objects.get(user__id=userAuth)
    try:
        callRegister = CallRegister()
        callRegister.dateCall = dateCallParam
        callRegister.company = companyName
        callRegister.demand = demandDescription
        callRegister.collaborator = colaboratorParam
        callRegister.observation = observationParam
        callRegister.value = numberValueParam
        callRegister.user = customerUser

        return callRegister
    except Exception as e:
        raise ValueError("Erro ao criar o objeto CallRegister. Erro: " + str(e)) 
    return None
    