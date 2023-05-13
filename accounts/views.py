from .serializers import *
from .models import User
from .permission import IsProfileOwnerOrSuperUser

from rest_framework.generics import CreateAPIView, RetrieveUpdateDestroyAPIView
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from rest_framework.authtoken.models import Token
from rest_framework.validators import ValidationError

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate


class RegUserView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserRegSerializer
    permission_classes = [~IsAuthenticated,]

    def get_serializer_class(self):
        if self.request.method == "PATCH" or self.request.method == "PUT":
            return UserSerializer
        return UserRegSerializer


class UserRetrieveView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsProfileOwnerOrSuperUser,]


class ChangePassView(APIView):#change my own password

    def patch(self, request):
        try:
            user_obj = request.user
        except User.DoesNotExist:
            return Response({"error":"User not Found!"})

        serialized = ChangePasswordSerializer(instance=request.user, data=request.data, context={"request":request})
        # print(serialized.initial_data)
        if serialized.is_valid():
            user_obj.set_password(serialized.validated_data.get('new'))
            user_obj.save()
            return Response({"data":serialized.data,"ok":True}, status=200)
        return Response({"data":serialized.errors,"ok":False}, status=404)


class LogApi(APIView):
    
    def get_permissions(self):
        if self.request.method == "DELETE":
           self.permission_classes = [IsAuthenticated]
        elif self.request.method == 'POST':
            self.permission_classes = [~IsAuthenticated]
        return [permission() for permission in self.permission_classes]

    def post(self, request):
        username = request.data.get("username", None)
        password=request.data.get("password", None)
        if not (username and password):
            raise ValidationError("These fields are required username and password!")
        user = authenticate(username=username, password=password)
        
        if user is None:
            return Response({'error':"User or password is not valid!"}, status=404)
        token, create = Token.objects.get_or_create(user=user) #creates token for authenticated user
        return Response({"token":token.key, 
                         "user":{'username':user.username,'id':user.id}
                         }, status=200)
    
    def delete(self, request):
        if request.user.is_authenticated:
            request.auth.delete() #removes authenticated token
            return Response({"data":"Come back soon!"}, status=200)
        return Response({"data":"Something wrong!"}, status=404)





