from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import Faculty
from .serializers import *
# Create your views here.


class FacultyView(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'success':0,'message':'Please provide token'})
        if request.user.user_type !="admin":
            return Response({'success':0,'message':'The admin doesn\'t exist'})
        try:     
            faculty = Faculty.objects.all()
            faculty_serializer =   FacultySerializer(faculty,many=True)
            return Response({'success':1,'data':faculty_serializer.data})
        except:
            return Response({'success':0,'message':'Something went wrong'})

    def post(self,request):
        if not request.user.is_authenticated:
            return Response({'success':0,'message':'Please provide token'})
        if request.user.user_type !="admin":
            return Response({'success':0,'message':'The admin doesn\'t exist'})
        try:
            fields = ['name']
            for field in fields:
                if field not in request.data:
                    return Response({'success':0,'message':f'The {field} should be provided'})
                if request.data[field] == "" or request.data[field] == None:
                    return Response({'success':0,'message':f'The {field} is empty'})
            name = request.data['name']
            faculty = Faculty.objects.filter(name=name)
            if list(faculty) != []:
                return Response({'success':0,'message':'The faculty already exist'})
            Faculty.objects.create(name=name).save()
            return Response({
                'success':1,
                'message':f'The faculty {name} has been added'
            })
        except:
            return Response({'success':0,'message':'Something went wrong'})
    def patch(self,request):
        if not request.user.is_authenticated:
            return Response({'success':0,'message':'Please provide token'})
        if request.user.user_type !="admin":
            return Response({'success':0,'message':'The admin doesn\'t exist'})
        try:
            fields = ['name','id']
            for field in fields:
                if field not in request.data:
                    return Response({'success':0,'message':f'The {field} should be provided'})
                if request.data[field] == "" or request.data[field] == None:
                    return Response({'success':0,'message':f'The {field} is empty'})
            name = request.data['name']
            id = request.data['id']
            faculty = Faculty.objects.filter(name=name)
            if list(faculty) != []:
                return Response({'success':0,'message':'The faculty already exist'})
            faculty = Faculty.objects.get(id=id)
            faculty_serializer = FacultySerializer(instance=faculty,data={'name':name},partial=True)
            if faculty_serializer.is_valid():
                faculty_serializer.save()
                return Response({
                    'success':1,
                    'message':f'The faculty {name} has been updated'
                })
            return Response({
                'success':0,
                'message':serializers.errors
            })
        except Faculty.DoesNotExist:
            return Response({'success':0,'message':'Faculty doesn\'t exist'})
        except:
            return Response({'success':0,'message':'Something went wrong'})
    def delete(self, request):
        if not request.user.is_authenticated:
            return Response({'success':0,'message':'Please provide token'})
        if request.user.user_type !="admin":
            return Response({'success':0,'message':'The admin doesn\'t exist'})
        try:
            fields = ['id']
            for field in fields:
                if field not in request.data:
                    return Response({'success':0,'message':f'The {field} should be provided'})
                if request.data[field] == "" or request.data[field] == None:
                    return Response({'success':0,'message':f'The {field} is empty'})     
            faculty = Faculty.objects.get(id=request.data['id'])
            faculty.delete()
            return Response({'success':1,'message':"Succesfully deleted faculty"})
        except Faculty.DoesNotExist:
            return Response({'success':0,'message':'Faculty doesn\'t exist'})
        except:
            return Response({'success':0,'message':'Something went wrong'})

   