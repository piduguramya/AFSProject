from django.shortcuts import render
from .models import UserAccount
from .serializers import UserAccountSerializer
from rest_framework.views import APIView
from rest_framework import status
from rest_framework.response import Response
from django.core.mail import send_mail
from django.conf import settings
from django.utils import timezone
import random
import datetime
import json

# Create your views here.
class UserRegisterView(APIView):
    def post(self,request):
        create_user=UserAccountSerializer(data=request.data)

        if create_user.is_valid():
            try:
                create_user.save()
                return Response({
                    "message":"user credentials saved sucessfully",
                    "data":create_user.data},
                    status=status.HTTP_201_CREATED)
            except Exception as e:
                return Response({
                    "error":e    #useralready exist      
                },status=status.HTTP_409_conflict)
        else:
            return Response(create_user.errors,status=status.HTTP_400_BAD_REQUEST)


class UserLoginView(APIView):
    def post(self,request):
        try:
            data=json.loads(request.body.decode('utf-8'))
            username=data.get('user_name')
            password=data.get('password')

            if not username or not password:
                return Response({'please provide username and mailid'},status=status.HTTP_400_BAD_REQUEST)

            try:
                check=UserAccount.objects.get(user_name=username,password=password)
                return Response({'user lgin successful'},status=status.HTTP_200_OK)

            except Exception as e:
                return Response({
                    'message':'user not exist',
                    'error':str(e)},status=status.HTTP_401_UNAUTHORIZED)
        except Exception as e:
            return Response({
                'message':"the data provided is not application/json(not a valid data)",
                'error':str(e)},status=status.HTTP_400_BAD_REQUEST)


class AllUsersView(APIView):
    def get(self,request):
        queryset=UserAccount.objects.all()
        data=UserAccountSerializer(queryset,many=True).data
        print(data)

        return Response(data)


class SingleuserView(APIView):
    def get(self,request,pk=None):
        if pk:
            try:
                queryset=UserAccount.objects.get(user_id=pk)
                data=UserAccountSerializer(queryset).data

                return Response(data)

            except Exception as e:
                return Response(str(e))

class ForgotPasswordView(APIView):
    def post(self, request):
        data = request.data
        mailid = data.get('user_mailid')
        username = data.get('user_name')

        if not username or not mailid:
            return Response(
                {'error': 'Please provide both username and mail ID.'},
                status=status.HTTP_400_BAD_REQUEST
            )

        try:
            user = UserAccount.objects.get(user_name=username, user_mailid=mailid)

            print("hiiiiiiiiiiii")

            otp = random.randint(100000, 999999)
            expiry_time = timezone.now() + datetime.timedelta(minutes=10)

            print("Inside ForgotPasswordView, OTP generated:", otp)  

            user.otp = otp
            user.otp_expires_at = expiry_time
            user.save()

            send_mail(
                'Your OTP Code',
                f'Your OTP for password reset is: {otp}. It expires in 10 minutes.',
                settings.EMAIL_HOST_USER,
                [mailid],
                fail_silently=False,
            )

            return Response(
                {'message': 'OTP sent to your email.'},
                status=status.HTTP_200_OK
            )

        except UserAccount.DoesNotExist:
            return Response(
                {'error': 'Invalid username or mail ID.'},
                status=status.HTTP_404_NOT_FOUND
            )


class ValidateOtpView(APIView):
    def post(self, request):
        data = request.data
        username = data.get('user_name')
        entered_otp = data.get('otp')

        # if not username or not entered_otp:
        #     return Response(
        #         {'error': 'Please provide username and OTP.'},
        #         status=status.HTTP_400_BAD_REQUEST
        #     )

        try:
            user = UserAccount.objects.get(user_name=username)

            if user.otp_expires_at is None or timezone.now() > user.otp_expires_at:
                return Response(
                    {'error': 'OTP has expired.'},
                    status=status.HTTP_408_REQUEST_TIMEOUT
                )

            print("Stored OTP:", user.otp)
            print("Entered OTP:", str(entered_otp))
            print("Equal?", user.otp == str(entered_otp))


            if user.otp.strip() == str(entered_otp):
                user.otp = None
                user.otp_expires_at = None
                user.save()
                return Response(
                    {'message': 'OTP validated successfully.'},
                    status=status.HTTP_200_OK
                )
            else:
                return Response(
                    {'error': 'Incorrect OTP.'},
                    status=status.HTTP_401_UNAUTHORIZED
                )

        except UserAccount.DoesNotExist:
            return Response(
                {'error': 'Invalid username.'},
                status=status.HTTP_404_NOT_FOUND
            )

class ResetPasswordView(APIView):
    def post(self,request):
        data=request.data
        user_mailid=data.get("mailid")
        password=data.get('password')
        reenter_password=data.get('re-password')

        try:
            user=UserAccount.objects.get(user_mailid=user_mailid)

            print(password,reenter_password,type(reenter_password),type(password))
            if password == reenter_password:
                user.password=str(password)
                user.save()

                return Response('password saved sucessfully')
            else:
                return Response("passwords not matching enter again")

        except Exception as e:
            return Response(str(e))







