from rest_framework import serializers
from .models import User
from django.utils.encoding import smart_str, force_bytes, DjangoUnicodeDecodeError
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django.contrib.auth.tokens import PasswordResetTokenGenerator

class UserRegisterationSerializer(serializers.ModelSerializer):
    password2 = serializers.CharField(style={'input_type' :'password'},write_only=True)
    class Meta:
        model = User
        fields = ['name', 'email', 'password', 'password2', 'tc']
        extra_kwargs = {
            'password' : {'write_only' : True}
        }
    
    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        
        if password != password2:
            raise serializers.ValidationError("Password fields doesn't match.")
        
        if len(password) < 8:
            raise serializers.ValidationError("Password length must be atleast 8 characters.")

        return attrs
    
    def create(self, validated_data):
        return User.objects.create_user(**validated_data)

class LoginSerializer(serializers.ModelSerializer):
    email = serializers.EmailField(max_length=255)

    class Meta:
        model = User
        fields = ['email', 'password']

class UserProfileSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'email', 'name']

class UserChangePasswordSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255,style={
        'input_type' : 'password'}, write_only=True)
    
    password2 = serializers.CharField(max_length = 255,style={
        'input_type' : 'password'}, write_only=True)
    
    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        user = self.context.get('user')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm password doesn't match")
    
        user.set_passowrd(password)
        user.save()
        return attrs

class SendPasswordResetEmailSerializer(serializers.Serializer):
    email = serializers.EmailField(max_length=255)
    class Meta:
        fields = ['email']
    def validate(self, attrs):
        email = attrs.get('email')
        if not User.objects.filter(email=email).exists():
            raise serializers.ValidationError("Email not registered")
        
        user = User.objects.get(email=email)
        uid = urlsafe_base64_encode(force_bytes(user.id))
        token = PasswordResetTokenGenerator().make_token(user=user)
        link = f'http://localhost/api/forgotpassword/{uid}/{token}'
        print('Reset Link: ',link)
        return attrs

class  UserPasswordResetSerializer(serializers.Serializer):
    password = serializers.CharField(max_length = 255,style={
        'input_type' : 'password'}, write_only=True)
    
    password2 = serializers.CharField(max_length = 255,style={
        'input_type' : 'password'}, write_only=True)
    
    class Meta:
        fields = ['password', 'password2']

    def validate(self, attrs):
        password = attrs.get('password')
        password2 = attrs.get('password2')
        uid = self.context.get('uid')
        token = self.context.get('token')

        if password != password2:
            raise serializers.ValidationError("Password and Confirm password doesn't match")

        id = smart_str(urlsafe_base64_decode(uid))

        if not User.objects.filter(id=id).exists():
            raise serializers.ValidationError("Invalid data")
        
        user = User.objects.get(id=id)

        if not PasswordResetTokenGenerator().check_token(user, token):
            raise serializers.ValidationError("Signature Error")

        user.set_password(password)
        user.save()
        return attrs