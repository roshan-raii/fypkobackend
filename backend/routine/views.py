# from .models import Routine
# from .serializers import *
# from rest_framework.views import APIView
# from rest_framework.response import Response
# from rest_framework.authentication import SessionAuthentication,TokenAuthentication

# class RoutineView(APIView):
#     authentication_classes = [SessionAuthentication,TokenAuthentication]
#     def get(self,request):
#         if not request.user.is_authenticated:
#             return Response({
#                 'success':0,
#                 'message':'Please provide token'
#             })
#         try:
#             # []
#             if request.user.user_type == "admin":
#                 fields = ['faculty','section','year']
#                 for field in fields:
#                     if not self.request.query_params.get(field):
#                         return Response({'success':0,'message':f'Please provide {field}'})
#                     # if request.data 
                
#                 # faculty = )
#             # faculty = self.request.query_params.get('faculty')

#             Routine = Routine.objects.all()
#             Routine_serializer = RoutineSerializer(Routine, many=True)
#             return Response({'success':1,'data':Routine_serializer.data})
#         except:
#             return Response({'success':0, 'message':'Something went wrong'})


#     def post(self,request):
#         if not request.user.is_authenticated:
#             return Response({
#                 'success':0,
#                 'message':'Please provide token'
#             })
#         # if request
#         if request.user.user_type != "admin":
#             return Response({'success':0,'message':'You aren\'t allowed to perform this action'})
#         try:
#             fields = ['year','day','time','module_id']
#             for field in fields:
#                 if field not in request.data:
#                     return Response({'success':0,'message':f'The {field} is required'})
#                 field_data = request.data[field]
#                 if field_data == "" or field_data == None:
#                     return Response({'success':0,'message':f'The {field} cannot be null or empty'})
#             serializer = RoutineSerializer(request.data)
#             if serializer.is_valid():
#                 serializer.save()
#                 return Response({'success':1,'message':'Successfully Saved Routine'})
#             return Response({'success':0,'message':'Error Saving data'})
#         except:
#             return Response({'success':0,'message':'Something wen\'t wrong'})