from django.urls import path
from . import  views

urlpatterns =[
    path('Dashboard',views.home),
    path('register',views.register),
    path('',views.user_login),
    path('logout',views.user_logout),
    path('profile',views.ViewProfile),
    path('editpro',views.EditProfile),
    path('propic',views.upload_image),
    path('forgotpass',views.Forgot_password),
    path('changepass',views.Change_password),
    path('viewblog',views.viewblog),
    path('verifypass',views.reset_password),
    path('createpro',views.CreateProfile),
    path('createblog',views.create_blog),
    path('details/<int:id>',views.View_details),
    path('update/<int:id>',views.update_blog),
    path('delete/<int:id>',views.delete_blog)


]