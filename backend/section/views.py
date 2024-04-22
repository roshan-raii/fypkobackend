from django.shortcuts import render

from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from .models import Section,YearSection
from .serializers import * 
from collections import defaultdict
from rest_framework.authentication import SessionAuthentication,TokenAuthentication
# from .

class ViewAllSections(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get(self,request):
        try:
            if not request.user.is_authenticated:
                return Response({'success':0,'message':'Please provide token'})
            if request.user.user_type !="admin":
                return Response({'success':0,'message':'The admin doesn\'t exist'})
            section = Section.objects.all().order_by('name')
            section_serializer = SectionSerializer(section,many=True)
            return Response({
                'success':1,
                'data':section_serializer.data
            })
        except:
            return Response(
                {
                    'success':0,
                    'message':'Something wen\'t wrong'
                }
            )  

class FacultyYearView(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({'success': 0, 'message': 'Please provide token'})
        if request.user.user_type != "admin":
            return Response({'success': 0, 'message': 'The admin doesn\'t exist'})
        # year_sections = YearSection.objects.all().select_related('year', 'section', 'faculty')
        # year_section_dict = defaultdict(list)
        # for year_section in year_sections:
        #     year_section_dict[year_section.year.name].append({
        #             "id": year_section.faculty.id,
        #             "name": year_section.faculty.name
        #     })
        # formatted_data = {year: sections for year, sections in year_section_dict.items()}
        year = Year.objects.all()
        year_serializer = YearSerializer(year,many=True)
        faculty = Faculty.objects.all()
        faculty_serializer = FacultySerializer(faculty,many=True)
        return Response({
            "success":1,
            "data":{
                'years':year_serializer.data,
                'faculty': faculty_serializer.data
            }
        })
        # return Response({"success": 1, "data": formatted_data})
class YearSectionView(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get(self, request, pk=None):
        if not request.user.is_authenticated:
            return Response({'success': 0, 'message': 'Please provide token'})
        if request.user.user_type != "admin":
            return Response({'success': 0, 'message': 'The admin doesn\'t exist'})
        if pk:
            try:
                year_section = YearSection.objects.get(pk=pk)
                serializer = FetchYearSecationSerializer(year_section)
                return Response({"success": 1, "data": serializer.data})
            except YearSection.DoesNotExist:
                return Response({"success": 0, "message": "YearSection doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

        year_sections = YearSection.objects.all().select_related('year', 'section', 'faculty')
        year_section_dict = defaultdict(list)
        for year_section in year_sections:
            year_section_dict[year_section.year.name].append({  
                    "id": year_section.section.id,
                    "name": year_section.section.name
                
            })
        formatted_data = {year: sections for year, sections in year_section_dict.items()}
        return Response({"success": 1, "data": formatted_data})
    def post(self, request):
        if not request.user.is_authenticated:
            return Response({'success':0,'message':'Please provide token'})
        if request.user.user_type !="admin":
            return Response({'success':0,'message':'The admin doesn\'t exist'})
        try:
            fields = ['year','faculty','section']
            for field in fields:
                if field not in request.data:
                    return Response({'success':0,'message':f'The {field} should be provided'})
                if request.data[field] == "" or request.data[field] == None:
                    return Response({'success':0,'message':f'The {field} is empty'})
            serializer = YearSectionSerializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"success": 1, "message": "YearSection created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"success": 0, "message": "Failed to create YearSection", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except:
            return Response({'success':0,'message':'Something wen\'t wrong'})
        
    def patch(self, request):
        if not request.user.is_authenticated:
            return Response({'success':0,'message':'Please provide token'})
        if request.user.user_type !="admin":
            return Response({'success':0,'message':'The admin doesn\'t exist'})
        try:
            if 'id' not in request.data:
                return Response({'success':0,'message':"Please provide id"})
            if request.data['id'] == "" or request.data['id'] == None:
                return Response({'success':0,'message':'Id cannot by null'})
            year_section = YearSection.objects.get(pk=request.data['id'])
            serializer = YearSectionSerializer(year_section, data=request.data, partial=True)
            if serializer.is_valid():
                serializer.save()
                return Response({"success": 1, "message": "YearSection updated successfully", "data": serializer.data})
            return Response({"success": 0, "message": "Failed to update YearSection", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except YearSection.DoesNotExist:
            return Response({"success": 0, "message": "YearSection doesn't exist"}, status=status.HTTP_404_NOT_FOUND)

    def delete(self, request):
        if not request.user.is_authenticated:
            return Response({'success':0,'message':'Please provide token'})
        if request.user.user_type !="admin":
            return Response({'success':0,'message':'The admin doesn\'t exist'})
        try:
            if 'id' not in request.data:
                return Response({'success':0,'message':"Please provide id"})
            if request.data['id'] == "" or request.data['id'] == None:
                return Response({'success':0,'message':'Id cannot by null'})
            year_section = YearSection.objects.get(pk=request.data['id'])
            year_section.delete()
            return Response({"success": 1, "message": 
"YearSection deleted successfully"})
        except YearSection.DoesNotExist:
            return Response({"success": 0, "message": "YearSection doesn't exist"}, status=status.HTTP_404_NOT_FOUND)



class SectionView(APIView):
    authentication_classes = [SessionAuthentication,TokenAuthentication]
    def get(self, request):
        if not request.user.is_authenticated:
            return Response({'success':0,'message':'Please provide token'})
        if request.user.user_type !="admin":
            return Response({'success':0,'message':'The admin doesn\'t exist'})
        try:     
            year = self.request.query_params.get('year')
            faculty = self.request.query_params.get('faculty')
            year_section = YearSection.objects.filter(year=year,faculty=faculty)
            print(year_section)
            serializer = FetchYearSecationSerializer(year_section,many=True)
            return Response({'success':1,'data':{
                "section":serializer.data
            }})
        except Exception as e:
            print(e)
            return Response({'success':0,'message':'Something went wrong'})

    def post(self,request):
        if not request.user.is_authenticated:
            return Response({'success':0,'message':'Please provide token'})
        if request.user.user_type !="admin":
            return Response({'success':0,'message':'The admin doesn\'t exist'})
        try:
            fields = ['year','faculty','name']
            for field in fields:
                if field not in request.data:
                    return Response({'success':0,'message':f'The {field} should be provided'})
                if request.data[field] == "" or request.data[field] == None:
                    return Response({'success':0,'message':f'The {field} is empty'})
            name = request.data['name']
            section_filter = Section.objects.filter(name=name)
            if list(section_filter) != []:
                return Response({'success':0,'message':'The section already exist'})
            section = Section.objects.create(name=name)
            section.save()
            field_data = {
                'section':section.id,
                'year':request.data['year'],
                'faculty':request.data['faculty']
            }
            serializer = YearSectionSerializer(data=field_data)
            if serializer.is_valid():
                serializer.save()
                return Response({"success": 1, "message": "YearSection created successfully", "data": serializer.data}, status=status.HTTP_201_CREATED)
            return Response({"success": 0, "message": "Failed to create YearSection", "errors": serializer.errors}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e)
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
            faculty = Section.objects.filter(name=name)
            if list(faculty) != []:
                return Response({'success':0,'message':'The faculty already exist'})
            faculty = Section.objects.get(id=id)
            faculty_serializer = SectionSerializer(instance=faculty,data={'name':name},partial=True)
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
        except Section.DoesNotExist:
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
            section = Section.objects.get(id=request.data['id'])
            section.delete()
            return Response({'success':1,'message':"Succesfully deleted faculty"})
        except Section.DoesNotExist:
            return Response({'success':0,'message':'Section doesn\'t exist'})
        except:
            return Response({'success':0,'message':'Something went wrong'})

   