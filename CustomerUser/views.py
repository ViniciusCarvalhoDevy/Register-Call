from django.shortcuts import render,redirect
from django.views.generic import FormView, TemplateView
from django.http import JsonResponse
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
        # Try to get the CustomerUser instance; handle missing user gracefully
        try:
            customer = CustomerUser.objects.get(user__email=email)
        except CustomerUser.DoesNotExist:
            messages.add_message(self.request, messages.ERROR, 'Usuário não encontrado.')
            return redirect('login')
        # Authenticate using the auth user's username string
        auth_user = authenticate(self.request, username=customer.user.username, password=password)
        if auth_user is not None:
            login(self.request, auth_user)
            # Store the CustomerUser id in session so forms can filter by it
            self.request.session['userAuthCustomerID'] = customer.id
            return redirect('home')
        else:
            messages.add_message(self.request, messages.ERROR, 'Credenciais inválidas.')
            return redirect('login')
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
    def get(self, request, *args, **kwargs):
        customerID = request.session.get('userAuthCustomerID')
        if not customerID:
            messages.add_message(request, messages.ERROR, 'Você precisa fazer login para acessar essa página.')
            return redirect('login')
        return super().get(request, *args, **kwargs)

    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        customerID = self.request.session.get('userAuthCustomerID')
        context['form'] = CallRegisterForm(customer=customerID)
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
        dateCall = form.cleaned_data.get('dateCall')
        compamy = form.cleaned_data.get('company')
        demand = form.cleaned_data.get('demand')
        print("Demand:", demand)
        print("Company:", compamy)
        colaborator = form.cleaned_data.get('collaborator')
        observation = form.cleaned_data.get('observation')
        numberValue = form.cleaned_data.get('value')
        print(dateCall, compamy, demand, colaborator, observation, numberValue)
        return super().form_invalid(form)
    
class LogoutView(TemplateView):
    template_name = 'login/login.html'
    def get(self, request, *args, **kwargs):
        self.request.session.clear()
        logout(request)
        return redirect('login')

class ReportsView(TemplateView):
    template_name = 'reports/reports.html'
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        context['demands'] = Demand.objects.all().order_by('description')
        context['companys'] = Company.objects.all().order_by('name')
        context['calls'] = None
        return context
    def get(self, request, *args, **kwargs):
        userAuth = self.request.session.get('userAuthCustomerID')
        callsRetorn = None
        dataFilter = {
            'dateCall': request.GET.get('filterDate'),
            'demand_id': request.GET.get('filterDemands'),
            'company_id': request.GET.get('filterCompany')  
        }
        filterGet = {chave: valor for chave, valor in dataFilter.items() if  valor not in [None, '']}
        callsRetornUser = CallRegister.objects.filter(user_id=userAuth).order_by('-dateCall')
        if callsRetornUser is not None:
            callsRetorn = callsRetornUser.filter(**filterGet)
            calls = self.get_context_data()
            calls['calls'] = callsRetorn
            calls['qtdCalls'] = callsRetorn.count()
            totalValue = callsRetorn.aggregate(models.Sum('value'))['value__sum'] or 0.00
            calls['totalValue'] = totalValue
            calls['dateFilter'] = dataFilter['dateCall']
            calls['filterDemands'] = dataFilter.get('demand_id', '')
            calls['filterCompany'] = dataFilter.get('company_id', '')
        return render(request, self.template_name, calls)
    
#Funcitions
def createCallRegister(userAuth,dateCallParam, companyName, demandDescription, colaboratorParam, observationParam, numberValueParam):
    try:
        callRegister = CallRegister()
        callRegister.dateCall = dateCallParam
        callRegister.company = companyName
        callRegister.demand = demandDescription
        callRegister.collaborator = colaboratorParam
        callRegister.observation = observationParam
        callRegister.value = numberValueParam
        # assign by id to avoid passing wrong object type
        print("Assigning CallRegister user_id:", userAuth)
        callRegister.user_id = userAuth

        return callRegister
    except Exception as e:
        raise ValueError("Erro ao criar o objeto CallRegister. Erro: " + str(e)) 
    return None
    