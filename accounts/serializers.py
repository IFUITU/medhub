from rest_framework import serializers

from .models import User


class UserRegSerializer(serializers.ModelSerializer): #registration serializer
    confirm_pass = serializers.CharField(max_length=50, write_only=True)
    class Meta:
        model = User
        fields = ("username", "password", "confirm_pass", "user_type")
        read_only_fields = ("id",)
        extra_kwargs = {
            'password': {'write_only': True}
        }
    
    def validate(self, data): #  validate password and confirm
        password = data.get("password")
        confirm = data.get("confirm_pass")
        if password != confirm:
            raise serializers.ValidationError("Confirmation password is not valid!")
        del data['confirm_pass']
        return data
    

    def create(self, validated_data):#to set hashed password
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ["username", 'user_type',]


class ChangePasswordSerializer(serializers.ModelSerializer):
    
    password = serializers.CharField(required=True, max_length=35, min_length=1)
    new = serializers.CharField(required=True, max_length=35, min_length=6, write_only=True)
    confirm = serializers.CharField(required=True, max_length=35, min_length=6, write_only=True)
    

    def validate(self, data):
        error = {}
        if not self.context['request'].user.check_password(data.get("password")):
            error['password'] = "Password is not valid!"
            raise serializers.ValidationError(error)
        
        if not data.get("new") == data.get("confirm"):
            error['confirm'] = "New password confirmation is not valid!"
            raise serializers.ValidationError(error)

        return data

    class Meta:
        model = User
        fields = ["password", 'new', 'confirm']