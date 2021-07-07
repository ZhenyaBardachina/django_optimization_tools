from django.urls import path
import authapp.views as authapp

app_name = 'authapp'

urlpatterns = [
    path('login/', authapp.login, name='login'),
    path('logout/', authapp.logout, name='logout'),
    path('user/profile/', authapp.edit, name='edit'),
    path('user/register/', authapp.register, name='register'),
    path('verify/<email>/<key>/', authapp.verify, name='verify'),
]


