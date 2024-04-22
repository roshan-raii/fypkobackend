from .models import *
from .serializers import *
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from faculty.models import *
from year.models import *
from faculty.serializers import *
from year.serializers import *


class ModuleTeacherView(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get(self,request):
        if not request.user.is_authenticated:
            return Response({'success':0,'message':'The user isn\'t authenticated'})
        try:
            module = self.request.query_params.get('module')
            module_teacher = ModuleTeacher.objects.filter(module__id=module)
            serializer = FetchModuleTeacherSerializer(module_teacher,many=True)
            return Response({
                "success":1,
                "data":{
                    "module":serializer.data
                }
            })
        except:
            return Response({
                "success":0,
                "message":"Something wen't wrong"
            })
    def delete(self,request):
        if not request.user.is_authenticated:
            return Response({
                "success":0,
                "message":"The user isn\'t authenticated"
            })
        try:
            fields = ['id']
            for field in fields:
                if field not in request.data:
                    return Response({
                        "success":0,
                        "message":f"Please provide the field {field}"
                    })
                data = request.data[field]
                if data == "" or data == None:
                    return Response({
                        "success":0,
                        "message":f"The {field} cannot be empty "
                    })
            module_teacher = ModuleTeacher.objects.get(id = request.data['id']).delete()
            return Response({
                "succcess":1,
                "message":'Successfully deleted module teacher'
            })
        except ModuleTeacher.DoesNotExist:
            return Response({
                "success":0,
                "message":"The Module Teacher doesnt exist"
            })
        except:
            return Response({
                "success":0,
                "message":"Something wen't wrong"
            })
    def post(self,request):
        if not request.user.is_authenticated:
            return Response({'success':0,'message':'The user isn\'t authenticated'})
        try:
            fields = ['module','teacher']
            for field in fields:
                if field not in request.data:
                    return Response({
                        "success":0,
                        "message":f"Please provide the field {field}"
                    })
                data = request.data[field]
                if data == "" or data == None:
                    return Response({
                        "success":0,
                        "message":f"The {field} cannot be empty "
                    })
            module_teacher = ModuleTeacherSerializer(data=request.data)
            if module_teacher.is_valid():
                module_teacher.save()
                return Response({
                    "success":1,
                    "message":"Successfully Added Teacher"
                })
            print(module_teacher.errors)
            return Response({
                "success":0,
                "message":"Error Saving data"
            })
        except Exception as e:
            print(e)
            return Response({
                "success":0,
                "message":"Something wen't wrong"
            })
class ModuleView(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    def get(self,request):
        if not request.user.is_authenticated:
            return Response({'success':0,'message':'The user isn\'t authenticated'})
        try:
            faculty = self.request.query_params.get('faculty')
            year = self.request.query_params.get('year')
            if not faculty:
                faculty = Faculty.objects.all()
                year = Year.objects.all()
                faculty_serializer = FacultySerializer(faculty,many=True)
                year_serializer = YearSerializer(year,many=True)
                return Response({
                    "success":1,
                    "data":{
                        "faculty":faculty_serializer.data,
                        "years":year_serializer.data
                    }
                })
            module_year = ModuleYear.objects.filter(year__name = year,faculty__id = faculty)
            module_serializer = ModuleYearSerialier(module_year,many=True)
            return Response({'success':1,'data':
            {
                          'module':module_serializer.data  
            }
                             })
        except Exception as e:
            print(e) 
            return Response({'success':0,'message':'Something wen\'t wrong'})

    def post(self,request):
        if not request.user.is_authenticated:
            return Response({'success':0,'message':'Please provide token'})
        if request.user.user_type != "admin":
            return Response({'success':0,'message':'You need to be an admin'})
        try:
            fields = ['year','faculty','module_name','module_start_date','module_end_date','description']
            for field in fields:
                if field not in request.data:
                    return Response({'success':0,'message':f'The {field} should be provided'})
                field_data = request.data[field]
                if field_data == "" or field_data == None:
                    return Response({'success':0,'message':f'The {field} cannot be null or empty'})
            
            serializer = ModuleSerialier(data=request.data)
            if serializer.is_valid():
                serializer.save()
                year = request.data['year']
                faculty = request.data['faculty']
                module_start_date = request.data['module_start_date']
                module_end_date = request.data['module_end_date']
                data = {
                   'year':year,
                   'faculty':faculty,
                   'module_start_date':module_start_date,
                   'module_end_date':module_end_date,
                   'module':serializer.data['id'] 
                }
                print(data)
                module_serializer = ModuleYearSingleSerializer(data=data)
                if module_serializer.is_valid():

                    module_serializer.save()
                else:
                    print(module_serializer.errors)
                return Response({'success':1,'message':'The module has been saved'})          
            return Response({'success':0,'message':'Error saving data'})
        except Exception as e:
            print(e)
            return Response({'success':0,'message':'Something wen\'t wrong'})
    
    def patch(self,request):
        if not request.user.is_authenticated:
            return Response({'success':0,'message':'Please provide token'})
        if request.user.user_type != "admin":
            return Response({'success':0,'message':'You need to be an admin'})
        try:
            fields = ['id']
            for field in fields:
                if field not in request.data:
                    return Response({'success':0,'message':f'The {field} should be provided'})
                field_data = request.data[field]
                if field_data == "" or field_data == None:
                    return Response({'success':0,'message':f'The {field} cannot be null or empty'})
            module = Module.objects.get(id=request.data['id'])
            serializer = ModuleSerialier(instance = module,data=request.data,partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({'success':1,'message':'The module has been saved'})
            return Response({'success':0,'message':'Error saving data'})
        except Module.DoesNotExist:
            return Response({'success':0,'message':'The module doesn\'t exist'})
        except: 
            return Response({'success':0,'message':'Something wen\'t wrong'})
    
    def delete(self,request):
        if not request.user.is_authenticated: 
            return Response({'success':0,'message':'User not validated'})
        if request.user.user_type != "admin":
            return Response({'success':0,'message':'You need to be an admin'})
        try:
            fields = ['id']
            for field in fields:
                if field not in request.data:
                    return Response({'success':0,'message':f'The {field} should be provided'})
                field_data = request.data[field]
                if field_data == "" or field_data == None:
                    return Response({'success':0,'message':f'The {field} cannot be null or empty'})
            module = Module.objects.get(id = request.data['id'])
            module.delete()    
            return Response({'success':1,'message':'Module has been deleted'})
        except: 
            return Response({'success':0,'message':'Something wen\'t wrong'})