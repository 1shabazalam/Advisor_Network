from django.http import response
from rest_framework.serializers import Serializer
from users.models import User
from django.shortcuts import render
from rest_framework.views import APIView
from .serializers import BookingSerializer, UserSerializer, AdvisorSerializer
from rest_framework.response import Response 
from rest_framework.exceptions import AuthenticationFailed
from .models import Bookings, User,Advisors
import jwt, datetime
from rest_framework import viewsets
from rest_framework.decorators import api_view
# Create your views here.

#For registering a user 
class RegisterView(APIView):
    def post(self, request):
        serializer = UserSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        user = User.objects.filter(email=serializer.data['email']).first()
        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.utcnow()
        }
        token = jwt.encode(payload, 'secret' , algorithm="HS256")
        return Response({
            'jwt' : token,
            'user_id' : user.id
        })


#For Login 
class LoginView(APIView):
    def post(self, request):
        email = request.data['email']
        password = request.data['password']
        
        user = User.objects.filter(email=email).first()
        if user is None:
            raise AuthenticationFailed('User not Found!')
        if not user.check_password(password):
            raise AuthenticationFailed('Incorrect Password')

        payload = {
            'id' : user.id,
            'exp' : datetime.datetime.utcnow() + datetime.timedelta(minutes=60),
            'iat' : datetime.datetime.utcnow()
        }

        key = 'secret'
        token = jwt.encode(payload, key , algorithm="HS256")

        response = Response()
        response.set_cookie(key='jwt', value=token,httponly=True)
        response.data = {
            'jwt' : token,
            'user_id' : user.id
        }

        return response

#For viewing the logged in user
class UserView(APIView):
    def get(self, request):
        token = request.COOKIES.get('jwt')

        if not token:
            raise AuthenticationFailed('Unauthenticated!')
        
        try:
            payload = jwt.decode(token, 'secret', algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed('Unauthenticated!')

        user = User.objects.filter(id=payload['id']).first()
        serializer = UserSerializer(user)
        return Response(serializer.data)

#For Logout
class LogoutView(APIView):
    def post(self, request):
        response = Response()
        response.delete_cookie('jwt')
        response.data = {
            'message' : 'success'
        }


#For adding an advisor
class AddAdvisorView(APIView):
    def post(self, request):
        serializer = AdvisorSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response({
            "message" : "Success"
        })

#For viewing all the advisors        
class AdvisorListView(APIView):
    def get(self, request, user_id):
        user = User.objects.get(id=user_id)
        advisors = Advisors.objects.all()
        serializer = AdvisorSerializer(advisors, many=True)
        return Response(serializer.data)


#For booking an advisor
class BookAdvisorView(APIView):
    def post(self, request, user_id, advisor_id):
        advisor_obj = Advisors.objects.get(id = advisor_id)
        user_obj = User.objects.get(id = user_id)
        booking_serializer = BookingSerializer(data=request.data)
        booking_serializer.is_valid(raise_exception=True)
        booking_serializer.validated_data['advisor'] = advisor_obj
        booking_serializer.validated_data['user'] = user_obj
        booking_serializer.save()
        return Response({
            'message' : 'success'
        })      

#For viewing all booked advisors 
class BookedListView(APIView):
    def get(self, request, user_id):
        booking = Bookings.objects.all()
        booking_serializer = BookingSerializer(booking, many=True)
        return Response(booking_serializer.data)


