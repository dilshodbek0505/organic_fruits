from django.shortcuts import render
from django.contrib.auth import authenticate, login, logout
from django.db.models import Avg

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.status import HTTP_404_NOT_FOUND
from rest_framework.permissions import IsAuthenticated, IsAdminUser
from rest_framework.authtoken.models import Token

import requests
from random import randint

from .shortcuts import get_object_or_none
from .models import Commend, Customer, Rating
from .serializers import CustomerSerializer



class CustomerCreateUpdateApi(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser, )
    def post(self, request, *args, **kwargs):
        serializer = CustomerSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "data": serializer.data
        })
    
    def patch(self, request, username, *args, **kwargs):
        customer = get_object_or_none(Customer, username = username)
        if customer:
            serializer = CustomerSerializer(instance=customer, data=request.data, partial = True)
            serializer.is_valid(raise_exception=True)
            serializer.save()
            return Response({
                "data": serializer.data
            })
        return Response({
            "error": "Bunday foydalanuvchi topilmadi!"
        })
    

class CustomerApi(APIView):
    def get(self, request, username: str,*args, **kwargs):
        customer = get_object_or_none(Customer.objects.values().all(), username = username)
        if not customer:
            return Response({
                    "status": False,
                    "error": "Bunday foydalanuvchi toplmadi!"
            }, status=HTTP_404_NOT_FOUND)
        rating = Rating.objects.select_related(
            "customer",
        ).filter(
            customer_id = customer['id']
        ).aggregate(rating_total = Avg('number'))
        if rating['rating_total']:
            rating = round(rating['rating_total'],1)
        else:
            rating = 0

        return Response({
            "status": True,
            "data": {**customer,
                     "rating": rating}
        })
    
    def patch(self, request, username: str, *args, **kwargs):
        customer = get_object_or_none(Customer, username = username)
        if request.user.is_authenticated and request.user.is_staff:    
            if customer:
                serializer = CustomerSerializer(instance=customer, data=request.data, partial = True)
                serializer.is_valid(raise_exception=True)
                serializer.save()
                return Response({
                    "data": serializer.data
                })
            message = "Bunday foydalanuvchi topilmadi!"
        else:
            message = "Bu amalyotni bajarish uchun sizda ruxsat mavjud emas!"

        return Response({
            "error": message
        })
    
    def delete(self, request, username: str, *args, **kwargs):
        customer = get_object_or_none(Customer, username = username)
        if request.user.is_authenticated and request.user.is_staff:    
            if customer:
                customer.delete()
                return Response({
                    "status": True,
                    "message": "Foydalanuvchi o'chirildi!"
                })
            message = "Bunday foydalanuvchi topilmadi!"
        else:
            message = "Bu amalyotni bajarish uchun sizda ruxsat mavjud emas!"

        return Response({
            "error": message
        })


class AllCusomterApi(APIView):
    permission_classes = (IsAuthenticated, IsAdminUser, )
    
    def get(self, request, *args, **kwargs):
        customers = Customer.objects.values().all()
        customers_data = []
        for customer in customers:
            customers_data.append({**customer})
        return Response({
            "status": True,
            "data": customers_data
        })


class LoginApi(APIView):
    def post(self, request, *args, **kwargs):
        data = request.data
        username = data.get("username")
        password = data.get("password")
        if username and password:
            user = authenticate(request, username = username, password = password)
            if not user:
                return Response({
                    "error": "Taqdim qilingan ma'lumotlar bilan tizimga kirib bo'lmadi!"
                })
            token,_ = Token.objects.get_or_create(user = user)
            login(request, user=user)
            
            return Response({
                "data": {
                    "id": user.id,
                    "username": user.username,
                    "first_name": user.first_name,
                    "last_name": user.last_name,
                    "token": token.key,
                }
            })
        return Response({
            "error": "Ma'lumotlar to'liq kiritilmagan!"
        })
    
class LogoutApi(APIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, *args, **kwargs):
        request.user.auth_token.delete()
        logout(request)
        return Response({
            "data": "Foydalanuvchi tizimdan chiqidi!"
        })


class CustomerCommendApi(APIView):
    def get(self, request, username, *args, **kwargs):
        customer = get_object_or_none(Customer, username = username)
        commends = Commend.objects.select_related(
            'customer'
        ).filter(
            customer_id = customer.id
        ).values("full_name", "text")

        commends_data = []
        for commend in commends:
            commends_data.append({**commend})
        
        return Response({
            "data": commends_data
        })

    def post(self, request, username,  *args, **kwargs):
        customer  = get_object_or_none(Customer, username = username)
        data  = request.data
        full_name = data.get("full_name")
        text = data.get("text")
        message = ""
        if not customer:
            message = "Bunday mijoz toplmadi!"
        elif not full_name or not text:
            message = "Taqdim qilingan ma'lumotlar to'liq emas!"
        elif len(text) < 20:
            message = "Izoh matni 20 ta belgidan kam bo'lmasligi keark!"
        else:
            Commend.objects.create(
                full_name = full_name,
                customer = customer,
                text = text,
            )
            return Response({
                "status": False,
            })
        
        return Response({
            "error": message
        })

        
class CustomerRatingAPi(APIView):
    def get(self, request, username, *args, **kwargs):
        customer = get_object_or_none(Customer, username = username)
        
        rating = Rating.objects.select_related(
            "customer",
        ).filter(
            customer_id = customer.id
        ).aggregate(rating_total = Avg('number'))

        rating = round(rating['rating_total'],1)
    
        return Response({
            "data": {
                "rating": rating
            }

        })
    
    def post(self, request, username, *args, **kwargs):
        data = request.data
        customer = get_object_or_none(Customer, username = username)
        rating_number = data.get("rating")
        phone_number = data.get("phone_number")
        otp_code = data.get("otp_code")
        message = ""
        if rating_number and customer and phone_number:
            rating = get_object_or_none(Rating, phone_number = phone_number)
            if rating:
                message = "Telfon raqam oldin ro'yxatdan o'tgan"
            else:
                top_code = requests.post("http://127.0.0.1:8000/user/otp/code/", data={"otp_code": otp_code})
                top_code = top_code.json()
                top_code_status = top_code['status']
                if not top_code_status:
                    message = "OTP to'g'ri kelmadi" 
                else:
                    Rating.objects.create(
                        number = rating_number,
                        customer = customer,
                        phone_number = phone_number
                    )
                    return Response({
                        "data": {
                            "phone_number": phone_number,
                            "message": "Rayting saqlandi!"
                        }
                    })
        else:
            message = "Ma'lumotlar to'liq kiritlmagan"
        
        return Response({
            "error": message
        })

class OTPApi(APIView):
    def post(self, request,*args, **kwargs):
        otp_code = randint(10000,99999)
        print(otp_code)
        data = request.data
        user_otp_code = data.get("otp_code")
        status = bool(user_otp_code and otp_code == user_otp_code)
        return Response({
            "status": status,
        })



