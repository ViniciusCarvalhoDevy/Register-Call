from django.shortcuts import render,redirect
from django.views.generic import FormView, TemplateView
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import CustomerUser, CallRegister
from Company.models import Company
from Demand.models import Demand
from .forms import LoginForm,CallRegisterForm
from django.contrib import messages
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
        qtdCalls= CallRegister.objects.filter(user__user=self.request.user).count()
        
        context['qtdCalls'] = qtdCalls
    
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
    
    def form_valid(self, form):
        
        dateCall = form.cleaned_data.get('dateCall')
        compamy = form.cleaned_data.get('company')
        demand = form.cleaned_data.get('demand')
        colaborator = form.cleaned_data.get('colaborator')
        observation = form.cleaned_data.get('observation')
        call = createCallRegister(self.request.user,dateCall, compamy, demand, colaborator, observation)
        if call is not None:
            messages.add_message(self.request, messages.SUCCESS, 'Chamado cadastrado com sucesso!')
        return redirect('callRegister')
    
    def form_invalid(self, form):
        messages.add_message(self.request, messages.ERROR, 'Erro ao cadastrar o chamado. Verifique os dados informados.')
        return super().form_invalid(form)
    
class LogoutView(TemplateView):
    template_name = 'login/login.html'
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')




#Funcitions
def createCallRegister(userAuth,dateCallParam, companyId, demandId, colaboratorParam, observationParam):
    demand = Demand.objects.get(id=demandId)
    company = Company.objects.get(id=companyId)  
    customerUser = CustomerUser.objects.get(user=userAuth)   
    try:
        call = CallRegister.objects.create(user=customerUser,dateCall=dateCallParam, company=company, demand=demand, collaborator=colaboratorParam, observation=observationParam)
        call.save()
    except Exception as e:
        raise ValueError("Erro ao criar o chamado. Erro: " + str(e)) 
    return call
    