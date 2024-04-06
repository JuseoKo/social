from rest_framework import serializers
from models.models.service.user import User


class UserSerializer(serializers.HyperlinkedModelSerializer):
    phone_number = serializers.CharField(required=False)

    class Meta:
        model = User
        fields = ["user_id", "email", "nickname", "phone_number", "password"]