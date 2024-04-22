from rest_framework.authentication import SessionAuthentication,TokenAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import *
from .serializers import YearSerializer


class YearView(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'success':0,'message':'Please provide token'})
        if request.user.user_type !="admin":
            return Response({'success':0,'message':'The admin doesn\'t exist'})
        try:     
            faculty = Year.objects.all()
            faculty_serializer =   YearSerializer(faculty,many=True)
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
            faculty = Year.objects.filter(name=name)
            if list(faculty) != []:
                return Response({'success':0,'message':'The faculty already exist'})
            Year.objects.create(name=name).save()
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
            # if id == "" or id == None:
            #     return Response({'success':0,'message':'Id cannot ne null'})
            faculty = Year.objects.filter(name=name)
            if list(faculty) != []:
                return Response({'success':0,'message':'The faculty already exist'})
            faculty = Year.objects.get(id=id)
            faculty_serializer = YearSerializer(instance=faculty,data={'name':name},partial=True)
            if faculty_serializer.is_valid():
                faculty_serializer.save()
                return Response({
                    'success':1,
                    'message':f'The faculty {name} has been updated'
                })
            return Response({
                'success':0,
                'message':faculty_serializer.errors
            })
        except Year.DoesNotExist:
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
            faculty = Year.objects.get(id=request.data['id'])
            faculty.delete()
            return Response({'success':1,'message':"Succesfully deleted faculty"})
        except Year.DoesNotExist:
            return Response({'success':0,'message':'Faculty doesn\'t exist'})
        except:
            return Response({'success':0,'message':'Something went wrong'})
