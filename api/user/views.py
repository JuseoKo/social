from drf_yasg import openapi
from drf_yasg.utils import swagger_auto_schema
from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.response import Response
from models.models.service.user import User
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import UserSerializer


class UserViewSet(viewsets.ViewSet):
    queryset = User.objects

    @swagger_auto_schema(tags=["User"], operation_description="모든 유저 목록을 반환하는 API 입니다.")
    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["User"], operation_description="특정 유저의 정보를 반환하는 API 입니다."
    )
    @action(detail=False, methods=["get"], url_path="(?P<user_id>[^/.]+)")
    def check_user_nickname(self, request, nickname=None):
        queryset = User.objects.filter(user_id=nickname)
        serializer = UserSerializer(queryset, many=True)
        return Response(serializer.data)

    @swagger_auto_schema(
        tags=["User"],
        operation_description="유저를 생성하는 API 입니다.",
        request_body=openapi.Schema(
            type=openapi.TYPE_OBJECT,
            required=[
                "user_id",
                "email",
                "nickname",
                "phone_number",
                "password",
            ],  # 필수 필드 지정
            properties={
                "user_id": openapi.Schema(
                    type=openapi.TYPE_STRING, description="유저 아이디"
                ),
                "email": openapi.Schema(type=openapi.TYPE_STRING, description="이메일"),
                "nickname": openapi.Schema(type=openapi.TYPE_STRING, description="닉네임"),
                "phone_number": openapi.Schema(
                    type=openapi.TYPE_STRING, description="전화번호"
                ),
                "password": openapi.Schema(
                    type=openapi.TYPE_STRING, description="비밀번호"
                ),
            },
        ),
    )
    def create(self, request):
        """
        유저생성 api
        :param request:
        :return:
        """
        serializer = UserSerializer(data=request.data)
        if serializer.is_valid():
            User.objects.create_user(**serializer.validated_data)
            return Response(serializer.data)
        return Response(serializer.errors)


class UserTokenObtainPairSerializer(TokenObtainPairSerializer):
    @classmethod
    def get_token(cls, user):
        token = super().get_token(user)

        # Add custom claims
        token['username'] = user.username
        # ...

        return token

class UserTokenObtainPairView(TokenObtainPairView):
    serializer_class = UserTokenObtainPairSerializer