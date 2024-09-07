from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Book



# Create your views here.
def home(request):
    mybooks = Book.objects.all().values()
    template = loader.get_template('home.html')
    context = {'mybooks': mybooks}
    return HttpResponse(template.render(context,request))