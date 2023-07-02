from django.urls import path
from .views import *

urlpatterns = [
    path('', TaskList.as_view(), name='task'),
    path('task/<int:pk>/', TaskDetail.as_view(), name='detail'),
    path('create', TaskCreate.as_view(), name='create'),
    path('update/<int:pk>/', TaskUpdate.as_view(), name='update'),
    path('delete/<int:pk>/', TaskDelete.as_view(), name='delete'),

    path('register/', TaskRegister.as_view(), name= "register"),
    path('login/', TaskLogin.as_view(), name= "login"),
    path('logout/', LogoutView.as_view(next_page='login'), name= "logout"), 
    # the next_page is used to redirect to the login page after logging out, default it takes us to django admin logout page
]
