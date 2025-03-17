from django.shortcuts import render
from django.views.generic import FormView, TemplateView

# Create your views here.


class HomePage(TemplateView):
    template_name = "home.html"
