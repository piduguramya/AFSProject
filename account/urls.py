from django.urls import path
from . import views

urlpatterns = [
    path('adduser/',views.UserRegisterView.as_view()),
    path('loginuser/',views.UserLoginView.as_view()),
    path('allusers/',views.AllUsersView.as_view()),
    path('getuser/<int:pk>',views.SingleuserView.as_view()),
    path('forget/',views.ForgotPasswordView.as_view()),
    path('ValidateOtpView/',views.ValidateOtpView.as_view()),
    path('reset/',views.ResetPasswordView.as_view()),
    path('addaccountuser/',views.RegAccountUserView.as_view())
    ]



    