from django.shortcuts import render
from rest_framework.views import APIView
from student.serializers import *
from rest_framework.response import Response
from rest_framework.authtoken.models import Token
from users import email as otp_gen
from .models import *


class StudentForgotPassword(APIView):
    def post(self,request):
        try:
            first_fields = ['email']
            first_fields.sort()
            second_fieds = ['otp','email']
            second_fieds.sort()
            third_fields = ['otp','email','password']
            third_fields.sort()
            if 'email' not in request.data:
                return Response({'success':0,'message':'Please provide the email'})
            email = request.data['email']
            base_user = BaseUser.objects.get(email=email)
            print(base_user.user_type)
            if base_user.user_type != 'student':
                return Response({'success':0,'message':'You aren\'t allowed to do this'})
            data = dict(request.data)
            fields = list(data.keys())
            fields.sort()
            print(fields)
            otp = otp_gen.generate_otp()
            if fields == first_fields:
                for field in first_fields:
                    if request.data[field]== "" or request.data[field] == None:
                        return Response({'success':0,'message':f'The {field} cannot be empty, or null.'})
                    base_user.otp = otp
                    base_user.save()
                    otp_gen.send_otp_email(email=email,otp=otp)
                    return Response({'success':1,'message':"Successfully sent otp"})
            if fields == second_fieds:
                user_otp = request.data['otp']
                for field in second_fieds:
                    if request.data[field]== "" or request.data[field] == None:
                        return Response({'success':0,'message':f'The {field} cannot be empty, or null.'})
                    if user_otp != base_user.otp:
                        return Response({'success':0,'message':'The otp doesn\'t match'})
                    return Response({'success':1,'message':'Successfully Verified Otp'})
            if fields == third_fields:
                user_otp = request.data['otp']
                for field in third_fields:
                    if request.data[field]== "" or request.data[field] == None:
                        return Response({'success':0,'message':f'The {field} cannot be empty, or null.'})
                    if user_otp != base_user.otp:
                        return Response({'success':0,'message':'The otp doesn\'t match'})
                
                print(f"Password was {base_user.password}")
                new_pass = make_password(request.data['password'])
                base_user.password = new_pass
                base_user.save()
                print(f"THe password is ${base_user.password}")
                return Response({'success':1,'message':'Successfully changed password'})
            return Response({"success":0,"message":"One or two fields missing"})
        except BaseUser.DoesNotExist:
            return Response({'success':0,'message':'The student doesn\'t exist'})
        except Exception as e:
            print(f"This is the exception {e}")
            return Response({'success':0,'message':'Something wen\'t wrong'})
        

class StudentLogin(APIView):
    def post(self, request):
        try:
            fields = ['email', 'password']
            for field in fields:
                if field not in request.data:
                    return Response({'success': 0, "message": f"Please provide the field {field}"})
                if request.data[field] == "" or request.data[field] == None:
                    return Response({'success':0,"message":f"The field {field} cannot be empty"})
            email = request.data['email']
            password = request.data['password']  
            print(password)
            base_user = BaseUser.objects.get(email=email)
            # print(base_user.password)
            print(f"The current pass if ${base_user.password}")
            if base_user.user_type != 'student':
                return Response({'success': 0, 'message': 'You are not allowed to do this'})
            
            # print(request.data['password'])
            password = request.data['password']
            if not base_user.check_password(password):
                return Response({'success': 0, 'message': 'Credentials didn\'t match'}) 
            token, created = Token.objects.get_or_create(user=base_user)  
            print(password)
            return Response({'success': 1, 'message': "Successfully Logged In", 'token': token.key})
        except BaseUser.DoesNotExist:
            return Response({'success': 0, 'message': 'Student doesn\'t exist'})
        except Exception as e:
            return Response({'success': 0, "message": "Something went wrong"})
