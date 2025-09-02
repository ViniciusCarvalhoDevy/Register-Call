from django.shortcuts import render,redirect
from django.views.generic import FormView, TemplateView
from django.http import HttpResponse
from django.contrib.auth import authenticate, login, logout
from .models import CustomerUser
from .forms import LoginForm
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
    
        return context

class RegisterPainel(TemplateView):
    template_name = 'registerPainel/registerPainel.html'
    
    def get_context_data(self, **kwargs) -> dict[str, any]:
        context = super().get_context_data(**kwargs)
        return context
    

    

class LogoutView(TemplateView):
    template_name = 'login/login.html'
    def get(self, request, *args, **kwargs):
        logout(request)
        return redirect('login')
