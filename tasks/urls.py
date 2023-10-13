from django.urls import path
from .import views
urlpatterns =[
  path('',views.loginUser,name='loginUser'),
  path('home/',views.home,name='home'),
  path('createTask/',views.createTask,name='createTask'),
  path('updateTask/<str:pk>/',views.updateTask,name='updateTask'),
  path('deleteTask/<str:pk>/',views.deleteTask,name='deleteTask'),
  path('registerUser/',views.registerUser,name='registerUser'),
  path('logoutUser/',views.logoutUser,name='logoutUser'),
  path('completedTasks/',views.completedTasks,name='completedTasks'),
  path('pendingTasks/',views.pendingTasks,name='pendingTasks'),
  path('expiredTasks/',views.expiredTasks,name='expiredTasks'),
]