from django.shortcuts import render
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from users.serializers import UserAdminSerializer
from users.models import *
from django.contrib.auth.hashers import make_password
from teacher.serializers import *
from student.serializers import *
from section.models import *
from year.models import *
from faculty.models import *


class TeacherView(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get(self,request):
        try:
            teacher = Teacher.objects.all()
            teacher_serializer = FetchTeacherSerializer(
                teacher,
                many=True
            )
            return Response({
                "success":1,
                "data":{
                    'teachers':teacher_serializer.data
                }
            })
        except: 
            return Response({
                "success":0,
                "message":"Something wen't wrong"
            })
class AdminLogin(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def post(self,request):
        try:
            # if not request.user.is_authenticated:
            #     return Response({'success':0,'message':'Please provide token'})

            fields = ['email','password']
            for field in fields:
                if field not in request.data:
                    return Response({'success':0,"message":f"Please provide the field {field}"})
                if request.data[field] == "" or request.data[field] == None:
                    return Response({'success':0,"message":f"THe field {field} cannot be empty"})
            email = request.data['email']
            password = request.data['password']
            base_user = BaseUser.objects.get(email=email)
            if base_user.user_type != 'admin':
                return Response({'success':0,'message':'You are not allowed to do this'})
            
            if not base_user.check_password(password):
            # hashed_password = make_password(password) 
            # # print(hashed_password)   
            # # print(base_user.password)
            # if hashed_password != base_user.password:
                return Response({'success':0,'message':'Credentials didn\'t match'}) 
            token,created = Token.objects.get_or_create(user=base_user)  

            return Response({'success':1,'message':"Successfully Logged In",'token':token.key})
        except BaseUser.DoesNotExist:
            return Response({'success':0,'message':f'Admin doesn\'t exit'})
        except:
            return Response({'success':0,"message":"Something wen't wrong"})
        

class CreateTeacher(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    def delete(self,request):
        try:
            if not request.user.authenticated:
                return Response({
                    'success':0,
                    'message':'The user doesn\'t exist'
                })
            if 'id' not in request.data:
                return Response({
                    'success':0,
                    'message':'Id is missing'
                })
            teacher = Teacher.objects.get(id = request.data['id'])
            teacher.delete()
            return Response({
                'success':1,
                'message':'Successfully deleted'
            })
        except Teacher.DoesNotExist:
            return Response({
                'success':0,
                'message':'Teacher doesn\'t exist'
            })
        except:
            return Response({
                'success':0,
                'message':'Something wen\'t wrong'
            })
        
    def post(self, request):
        try:
            print(request.data)
            # fields = ['faculty','dob','gender','contactNumber','address','joinDate','collegeMail','email','full_name','image']
            if not request.user.is_authenticated:
                return Response({'success':0,'message':'Please provide token'})
            if request.user.user_type != "admin":
                return Response({'success':0,'message':'You aren\'t allowed for this action'})

            data = {
                'faculty':request.data['faculty'],
                'dob':request.data['dob'],
                'gender':request.data['gender'],
                'contactNumber':request.data['contactNumber'],
                'address':request.data['address'],
                'joinDate':request.data['joinDate'],
                'collegeMail':request.data['collegeMail'],
                'email':request.data['collegeMail'],
                'full_name':request.data['full_name'],
                'image':request.data['image'],
                'qualification':request.data['qualification'],
                'experience':request.data['experience'],
            }
            hash_pass = make_password(data['dob'])
            data['password'] = hash_pass
            base_user = BaseUser.objects.filter(email = data['email'])
            if list(base_user) != []:
                return Response({
                    'success':0,
                    'message':"The teacher already exists"
                })

            data['user_type'] = 'teacher'
            teacher_serializer = TeacherSerializer(data=data,many=False)
            if teacher_serializer.is_valid():
                teacher_serializer.save()
                return Response({'success':1,'message':'Successfully saved'})
            return Response({'success':0,'message':teacher_serializer.errors})
        except Exception as e:
            # print(e)
            print(f"This is the exception {e}")
            return Response({
                'success':0,'message':'Something wen\'t wrong'
            })

class ViewYearSection(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    def get(self,request):
        if not request.user.is_authenticated:
            return Response({'success':0,'message':'Please provide token'})
        year_section = YearSection.objects.all().order_by('year__name').distinct()
        for year in year_section:
            print(f"THe year  {year.year.name}")
            print(f"THe section  {year.section.name}")
        data = {}
        sections = []
        name = ""
        for year_sec in year_section:
                current_name = year_sec.year.name
                if name != current_name:
                    if sections:
                        data[name] = sections
                        sections = []  
                    name = current_name
                sections.append({
                    'id': year_sec.section.id,
                    'name': year_sec.section.name
                })
        if sections:
                data[name] = sections
        return Response({
            "success":1,
            "data":data
        })
class ViewUsers(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    def get(self,request):
        student = Student.objects.all()
        teacher = Teacher.objects.all()
        student_serializer = FetchStudentSerializer(student,many=True)
        teacher_serializer = FetchTeacherSerializer(teacher,many=True)
        return Response({
            'success':1,
            'data':{
                'student':student_serializer.data,
                'teacher':teacher_serializer.data
            }
        })

# class 

class CreateStudent(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    def delete(self, request):
        try:
            if not request.user.authenticated:
                return Response({
                    'success':0,
                    'message':'The user does\'t exist'
                })
            if 'id' not in request.data:
                return Response({
                    'success':0,
                    'message':'Id is missing'
                })
            student = Student.objects.get(id = request.data['id'])
            student.delete()
        except Student.DoesNotExist:
            return Response({
                'success':0,
                'message':'Student doesn\'t exist'
            })
        except:
            return Response({
                'success':0,
                'message':'Something wen\'t wrong'
            })

    def get(self,request):
        try:
    
            id = self.request.query_params.get('id')
            if not id:
                return Response({
                    'success':0,
                    'message':'Please provide id'
                })
            user = BaseUser.objects.get(id=id)
            if user.user_type == 'student':
                student = Student.objects.get(email=user.email)
                student_serializer = FetchStudentSerializer(student)
                return Response({
                    'success':1,
                    'data':student_serializer.data
                })
            if user.user_type == "teacher":
                teacher = Teacher.objects.get(email=user.email)

                teacher_serializer = FetchTeacherSerializer(teacher)
                return Response({
                    'success':1,
                    'data':teacher_serializer.data
                })
            if user.user_type == "admin":
                return Response({
                    'success':0,
                    'message':"The user doesn't exist"
                })
        except BaseUser.DoesNotExist:
                return Response({'success':0,'message':'User doesn\'t exist'})
        except Exception as e:
                print(e)
                return Response({'success':0,'message':'Something wen\'t wrong'})
    def post(self, request):    
        try:
            print("ada");
            fields = ['faculty','dob','gender','contactNumber','section','year','address','joinDate','collegeMail','email','full_name','image']
            if not request.user.is_authenticated:
                return Response({'success':0, "message":'Please Provide token'})
            if request.user.user_type != 'admin':
                return Response({"success":0, "message":"You aren\'t allowed for this action"})
            
            data = {
                'dob':request.data['dob'],
                'contactNumber':request.data['contactNumber'],
                # 'section':request.data['section'],
                'address':request.data['address'],
                'joinDate':request.data['joinDate'],
                'collegeMail':request.data['collegeMail'],
                'email':request.data['email'],
                'full_name':request.data['full_name'],
                'gender':request.data['gender'],
                'image':request.data['image'],
            }
            # print(request.data['image'])
            print(f"This is the image {request.data['image']}")
            # print(data)
            # for field in fields:
            #     if field not in request.data:
            #         return Response({'success':0, "message":f"Please provide the field {field}"})
            #     if request.data[field] == "" or request.data[field] == None:
            #         return Response({'success':0 , "message":f"The field {field} cannot be empty"})
            # data = dict(request.data)

            year_section = YearSection.objects.filter(section__id=request.data['section'])
            # print(request.data['section'])
            # request.data[]
            # data['section'] = year_section
            year_sec = year_section[0]
            data['section'] = year_sec.section.id
            data['year'] = year_sec.year.id
            data['faculty'] = year_sec.faculty.id
            hash_pass = make_password(request.data['dob'])
            data['password'] = hash_pass
            base_user = BaseUser.objects.filter(email = request.data['email'])
            if list(base_user) != []:
                print("adada")
                return Response({
                    'success':0,
                    'message':"The student already exists"
                })
            
            data['user_type'] = 'student'
            # print(request.data)
            student_serializer = StudentSerializer(data = data)
            print("THis is ")
            if student_serializer.is_valid():
                student_serializer.save()
                print("Herae")
                return Response({'success':1, 'message':'Successfully saved'})
            print(student_serializer.errors)
            return Response({'success':0,'message':student_serializer.errors})
        except Section.DoesNotExist:
            print("Herew")
            return Response({
                "success":0,
                "message":"Section Doesn't exist"
            })
        except Exception as e:
            print("THis isthat ")
            print(e)
            return Response({
                'success':0,'message':'Something wen\'t wrong'
            })