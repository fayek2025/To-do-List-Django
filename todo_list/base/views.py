from typing import Any
from django.shortcuts import render , redirect
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView , FormView
from django.views.generic.edit import UpdateView  ,DeleteView
from django.contrib.auth.forms import UserCreationForm #this is to generate registration form
from django.contrib.auth import login
from django.http import HttpRequest, HttpResponse
from django.urls import reverse_lazy
from .models import Task

from django.contrib.auth.views import LoginView
from django.contrib.auth.mixins import LoginRequiredMixin
# Create your views here
#Here we are going to use classbased views 
#instead of function based views
#creating a view which displays which task are assigned or which not

#creating login view

class CustomLoginView(LoginView):
    template_name = 'base/login.html'
    fields = '__all__'
    redirect_authenticated_user = True
    
    def get_success_url(self):
        return reverse_lazy('tasks')

#here 'LoginRequiredMixin' view lets the site redirect to login page 
#if the user is not authenticated

class RegisterPage(FormView):
    template_name = 'base/register.html'
    form_class = UserCreationForm
    redirect_authenticated_user = True
    success_url = reverse_lazy("tasks") #if the registration is done successfully 
                                        #then we will redirect it to index page
                                        
    def form_valid(self, form):
        
        user = form.save()
        if user is not None:
            login(self.request , user)
        return super(RegisterPage , self).form_valid(form)
    
    
    def get(self, *args , **kwargs):
        if self.request.user.is_authenticated:
            return redirect('tasks')
        else:
             
            return super(RegisterPage , self).get( *args, **kwargs)
    
class TaskView(LoginRequiredMixin , ListView):
    model = Task
    context_object_name = 'Tasks'
    template_name = 'base/task.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['Tasks'] = context['Tasks'].filter(user = self.request.user)
        context['count'] = context['Tasks'].filter(complete = False).count()
        return context
#adding details to tasks
#here 'LoginRequiredMixin' is applied so that the user can not 
#go to url like 'task/task.id' without authentication
class TaskDetail(LoginRequiredMixin ,DetailView):
    model = Task
    context_object_name = 'task'
    
#adding an option to create new task
class TaskCreate(LoginRequiredMixin ,CreateView):
    model = Task
    fields = ['title' , 'description' , 'complete']#assinging the fields of our databases to the model
    success_url = reverse_lazy("tasks")
    
    def form_valid(self, form):
        
        form.instance.user = self.request.user
        return super(TaskCreate , self).form_valid(form)
    
#adding the option to update the task 
class TaskUpdate(LoginRequiredMixin ,UpdateView):
    model = Task
    fields = ['title' , 'description' , 'complete'] #assinging the fields of our databases to the model
    success_url = reverse_lazy("tasks")
    
class TaskDelete(LoginRequiredMixin ,DeleteView):
    model = Task
    context_object_name = 'task'                    #assinging the fields of our databases to the model
    success_url = reverse_lazy("tasks")
    