from auth_app.models import *
from main_app.imports import *
from auth_app.serializers import *

class CreateUserView(APIView):
    serializer_class = UserProfile_Serializer
    permission_classes = [permissions.AllowAny]

    def post(self,  request):
        try:
            serializer = User_Serializer(data=request.data)
            if serializer.is_valid():
                serializer.save()
                return Response({"message":"User created successfully"},status=status.HTTP_200_OK)
            return Response({"message":"Something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        except Exception as e:
            return Response({"message":"Something went wrong"},status=status.HTTP_500_INTERNAL_SERVER_ERROR)
