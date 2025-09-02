from django.shortcuts import render
from django.views.generic import FormView
from .forms import DemandFormModel

# Create your views here.
class DemandRegisterView(FormView):
    template_name = 'demandRegister.html'
    success_url = '/demand/register'
    form_class = DemandFormModel
    
    def form_valid(self, form):
        pass
        return super().form_valid(form)
    
    def form_invalid(self, form):
        pass
        return super().form_invalid(form)