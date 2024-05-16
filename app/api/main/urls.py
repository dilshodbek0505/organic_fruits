from django.urls import path
from .views import (
    CustomerApi,
    AllCusomterApi,
    LoginApi,
    LogoutApi,
    CustomerCommendApi,
    CustomerRatingAPi,
    OTPApi,
    CustomerCreateUpdateApi
)


urlpatterns = [
    path('customer/details/<str:username>/', CustomerApi.as_view()),
    path('customer/all/', AllCusomterApi.as_view()),
    path('user/login/',LoginApi.as_view()),
    path('user/logout/', LogoutApi.as_view()),
    path('customer/details/<str:username>/rating/',CustomerRatingAPi.as_view()),
    path('customer/details/<str:username>/commend/',CustomerCommendApi.as_view()),
    path('user/otp/code/', OTPApi.as_view()),
    path('customer/add/', CustomerCreateUpdateApi.as_view()),
    path('customer/details/<str:username>/update/', CustomerCreateUpdateApi.as_view())

]


