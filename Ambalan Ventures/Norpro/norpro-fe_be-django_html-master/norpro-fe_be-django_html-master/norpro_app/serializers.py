from rest_framework import serializers
from .models import *
from rest_framework_simplejwt.serializers import TokenObtainPairSerializer
from django.contrib.auth.hashers import check_password
from django.contrib.auth import authenticate




class AlertsSerializer(serializers.ModelSerializer):

    class Meta:
        model = Alerts
        fields = '__all__'

class AnnouncementFileSerializer(serializers.ModelSerializer):
    class Meta:
        model = AnnouncementFile
        fields = '__all__'

class AnnouncementSerializer(serializers.ModelSerializer):
    files = AnnouncementFileSerializer(many=True, read_only=True)

    class Meta:
        model = Announcement
        fields = '__all__'

class GreetingBannerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Greeting_banner
        fields = '__all__'

class NewsSerializer(serializers.ModelSerializer):

    class Meta:
        model = News
        fields = '__all__'

class CustomTokenObtainPairSerializer(TokenObtainPairSerializer):
    email = serializers.EmailField()
    password = serializers.CharField(write_only=True)
    fcm_token = serializers.CharField(required=False, allow_blank=True)

    def validate(self, attrs):
        email = attrs.get("email")
        password = attrs.get("password")
        fcm_token = attrs.get("fcm_token", "")

        # Authenticate user using Django's built-in authentication system
        user = authenticate(username=email, password=password)

        if not user or user.user_type != "Team" or not user.is_active:
            raise serializers.ValidationError({
                "status": 0,
                "message": "Invalid email or password"
            })
        if user.status=="Inactive":
            raise serializers.ValidationError({
                "status":0,
                "message":"User is inactive"
            })
            

        # Ensure the user has an associated id_card
        id_card_instance = id_card.objects.filter(user=user).first()
        if not id_card_instance:
            raise serializers.ValidationError({
                "status": 0,
                "message": "User does not have an associated ID card"
            })

        # Update FCM token if provided
        if fcm_token:
            id_card_instance.fcm_token = fcm_token
            id_card_instance.save()

        # Generate JWT token
        refresh = self.get_token(user)
        print(user.changed_pwd,'checkuserrrrrrr')

        return {
            "status": 1,
            "message": "Login successful!",
            "data": {
                "access_token": str(refresh.access_token),
                "refresh_token": str(refresh),
                "fcm_token": id_card_instance.fcm_token,
                "change_pwd":user.changed_pwd
            }
        }

    @classmethod
    def get_token(cls, user):
        """
        Generates a JWT token including additional user details.
        """
        token = super().get_token(user)
        token["email"] = user.email
        token["user_type"] = user.user_type
        return token
