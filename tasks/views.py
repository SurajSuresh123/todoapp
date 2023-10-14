from django.shortcuts import render,redirect
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.utils import timezone
from .models import *
from .forms import CreateUserForm 
def registerUser(request):
  if request.user.is_authenticated:
    return redirect('home')
  form=CreateUserForm()
  
  if request.method=='POST':
    form=CreateUserForm(request.POST)
    if form.is_valid():
      form.save()
      messages.success(request, 'Registration successful. You can now log in.')
      return redirect('home')
    else:
       for field, errors in form.errors.items():
                for error in errors:
                    messages.error(request, f'Error in {form.fields[field].label}: {error}')
  context={'form':form}
  return render(request,'tasks/registerform.html',context)
   

def loginUser(request):
  if request.user.is_authenticated:
    return redirect('home')
  else:
    username=request.POST.get('username')
    password=request.POST.get('password')
    user=authenticate(request,username=username,password=password)
    if user is not None:
      login(request,user)
      return redirect('home')
   
      
    context={}
    return render(request,'tasks/loginpage.html',context)

def logoutUser(request):
  logout(request)
  return redirect('loginUser')

@login_required(login_url='loginUser')
def home(request):
  if request.user.is_authenticated:  
    tasks = Tasks.objects.filter(user=request.user)
  context={'tasks':tasks}
  return render(request,'tasks/home.html',context)

@login_required(login_url='loginUser')
def createTask(request):
  if request.method =='POST':
    user=request.user
    task=request.POST.get('task')
    tocomplete_date=request.POST.get('tocomplete_date')
    completed=request.POST.get('completed','false')
    Tasks.objects.create(user=user,task=task,tocompleted_date=tocomplete_date,completed=completed.lower() == 'true')
    return redirect('home')
  return render(request,'tasks/form.html')  

@login_required(login_url='loginUser')
def updateTask(request,pk):
  task=Tasks.objects.get(id=pk)
  if request.method =='POST':
    task.task=request.POST.get('task')
    task.tocompleted_date=request.POST.get('tocomplete_date')
    task.completed=request.POST.get('completed','false').lower()=='true'
    task.save()
    return redirect('home')
  context={'task':task}
  return render(request,'tasks/updateform.html',context)

@login_required(login_url='loginUser')
def deleteTask(request,pk):
  task=Tasks.objects.get(id=pk)
  if request.method=='POST':
    task.delete()
    return redirect('home')
  context={'task':task}
  return render(request,'tasks/delete.html',context)

@login_required(login_url='loginUser')
def completedTasks(request):
  if request.user.is_authenticated:  
    completed_task=Tasks.objects.filter(user=request.user,completed=True)
  context={'completed_task':completed_task}
  return render(request,'tasks/completedtasks.html',context)

@login_required(login_url='loginUser')
def pendingTasks(request):
  if request.user.is_authenticated:  
    pending=Tasks.objects.filter(user=request.user,completed=False)
  context={'pending':pending}
  return render(request,'tasks/pendingtasks.html',context)

@login_required(login_url='loginUser')
def expiredTasks(request):
  if request.user.is_authenticated:
    current_date=timezone.now().date()  
    expired=Tasks.objects.filter(user=request.user,tocompleted_date__lt=current_date)
  context={'expired':expired}
  return render(request,'tasks/expiredtasks.html',context)