from typing import Any, Dict
from django.forms.models import BaseModelForm
from django.http import HttpResponse
from django.shortcuts import render, redirect

from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, UpdateView, DeleteView, FormView
from django.contrib.auth.views import LoginView, LogoutView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login



from .models import Task

from django.urls import reverse_lazy

from django.contrib.auth.mixins import LoginRequiredMixin

# Create your views here.

# we could also use decorators like in CRM project but lets try new

class TaskList(LoginRequiredMixin, ListView):
    model= Task
    #The django class requires the default template name like for the TaskList class it maps to task_list.html,
    # we can also override it
    context_object_name= "task"

    def get_context_data(self, **kwargs):
        context= super().get_context_data(**kwargs)
        context['task']= context['task'].filter(user= self.request.user)
        context['count']= context['task'].filter(complete= False).count()

        search_input= self.request.GET.get('search-area') or ''
        if search_input:
            context['task']= context['task'].filter(title__icontains= search_input)            
            context['search_input']= search_input

        return context

class TaskDetail(LoginRequiredMixin, DetailView):
    model= Task
    context_object_name= "task"
    template_name= "todo/detail.html"


class TaskCreate(LoginRequiredMixin, CreateView):
    model= Task
    fields= ['title','description', 'complete']
    success_url= reverse_lazy('task')
    template_name= 'todo/create.html'

    def form_valid(self, form):
        form.instance.user= self.request.user
        return super(TaskCreate, self).form_valid(form)


class TaskUpdate(LoginRequiredMixin, UpdateView):
    model= Task
    fields= ['title','description', 'complete']
    success_url= reverse_lazy('task')
    template_name= 'todo/create.html'


class TaskDelete(LoginRequiredMixin, DeleteView):
    model= Task    
    context_object_name= "task"
    success_url= reverse_lazy('task')
    template_name= 'todo/delete.html'

class TaskLogin(LoginView):
    template_name= "todo/login.html"
    fields= "__all__" 
    redirect_authenticated_user= False
    
    def get_success_url(self):
        return reverse_lazy('task')
    
class TaskRegister(FormView):
    template_name= 'todo/register.html'
    form_class= UserCreationForm
    redirect_authenticated_users= True
    success_url= reverse_lazy('task')

    def form_valid(self, form):
        user= form.save()
        if(user is not None):
            login(self.request, user)
        return super(TaskRegister, self).form_valid(form)
    
    def get(self, *args, **kwargs):
        if self.request.user.is_authenticated:
            return redirect('task')
        return super(TaskRegister, self).get(*args, **kwargs)