from datetime import date
from rest_framework import viewsets
from .models import *
from .serializers import *
from .pagination import CustomPagination
from rest_framework_simplejwt.views import TokenObtainPairView
from .serializers import CustomTokenObtainPairSerializer
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from django.contrib.auth.hashers import check_password
from django.contrib.auth.password_validation import validate_password
from django.core.exceptions import ValidationError
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from firebase_admin import credentials,messaging
from firebase_admin.exceptions import FirebaseError
from django.conf import settings
import firebase_admin
from norpro_app.authentication import ActiveUserJWTAuthentication
from django.http import FileResponse, Http404
import os
import mimetypes


try:
    cred = credentials.Certificate("lib/firebase.json")
    firebase_admin.initialize_app(cred)
except Exception:
    print("WARNING: Firebase credentials not found. Push notifications disabled.")
    firebase_admin.initialize_app()

# History ViewSets - returns all records ordered by updated_at
class AlertsHistoryViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class = AlertsSerializer
    pagination_class = CustomPagination
    authentication_classes=[ActiveUserJWTAuthentication]

    def get_queryset(self):
        user = self.request.user

        # Check if user is inactive
        
        # Ensure the user has an associated id_card
        if hasattr(self.request.user, 'id_card') and self.request.user.user_type == "Team":
            user_departments = self.request.user.id_card.department.all()  # Get user's departments
        else:
            return News.objects.none()  # Return empty queryset if no id_card or user is not 'Team'

        # Filter news where department matches any of the user's departments
        return Alerts.objects.filter(department__in=user_departments).order_by('-updated_at')

class AnnouncementHistoryViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class = AnnouncementSerializer
    pagination_class = CustomPagination
    authentication_classes=[ActiveUserJWTAuthentication]

    def get_queryset(self):
        # Ensure the user has an associated id_card
        if hasattr(self.request.user, 'id_card') and self.request.user.user_type == "Team":
            user_departments = self.request.user.id_card.department.all()  # Get user's departments
        else:
            return News.objects.none()  # Return empty queryset if no id_card or user is not 'Team'

        # Filter news where department matches any of the user's departments
        return Announcement.objects.filter(department__in=user_departments).order_by('-updated_at')

class GreetingBannerHistoryViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    serializer_class = GreetingBannerSerializer
    pagination_class = CustomPagination
    authentication_classes=[ActiveUserJWTAuthentication]

    def get_queryset(self):
        # Ensure the user has an associated id_card
        if hasattr(self.request.user, 'id_card') and self.request.user.user_type == "Team":
            user_departments = self.request.user.id_card.department.all()  # Get user's departments
        else:
            return News.objects.none()  # Return empty queryset if no id_card or user is not 'Team'

        # Filter news where department matches any of the user's departments
        return Greeting_banner.objects.filter(department__in=user_departments).order_by('-updated_at')

class NewsHistoryViewSet(viewsets.ModelViewSet):
    permission_classes = [IsAuthenticated]
    serializer_class = NewsSerializer
    pagination_class = CustomPagination
    authentication_classes=[ActiveUserJWTAuthentication]

    def get_queryset(self):
        # Ensure the user has an associated id_card
        if hasattr(self.request.user, 'id_card') and self.request.user.user_type == "Team":
            user_departments = self.request.user.id_card.department.all()  # Get user's departments
        else:
            return News.objects.none()  # Return empty queryset if no id_card or user is not 'Team'

        # Filter news where department matches any of the user's departments
        return News.objects.filter(department__in=user_departments).order_by('-updated_at')

# Overview ViewSets - filters records based on Expire_date >= today
class AlertsOverviewViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    authentication_classes=[ActiveUserJWTAuthentication]
    def get_queryset(self):
        today = date.today()

        if hasattr(self.request.user, 'id_card'):
            user_departments = self.request.user.id_card.department.all()  # Get user's departments
            print(user_departments,"************")
        else:
            return Alerts.objects.none()

        return Alerts.objects.filter(Expire_date__gte=today,department__in=user_departments).order_by('-updated_at')

    serializer_class = AlertsSerializer

class AnnouncementOverviewViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    authentication_classes=[ActiveUserJWTAuthentication]
    def get_queryset(self):
        today = date.today()

        if hasattr(self.request.user, 'id_card'):
            user_departments = self.request.user.id_card.department.all()  # Get user's departments
            print(user_departments,"************")
        else:
            return Announcement.objects.none()
        
        return Announcement.objects.filter(Expire_date__gte=today,department__in=user_departments).order_by('-updated_at')

    serializer_class = AnnouncementSerializer


class download_announcement_file(APIView):
    def post(self, request, pk):
        try:
            id = request.GET.get("id")
            announcement = AnnouncementFile.objects.get(announcement=pk, id=id)
            if not announcement.file:
                raise Http404("No file found.")
            
            file_path = announcement.file.path
            file_name = os.path.basename(file_path)
            
            # More aggressive MIME type detection
            content_type, _ = mimetypes.guess_type(file_path)
            
            # Fallback to checking file extension manually
            if not content_type:
                ext = os.path.splitext(file_path)[1].lower()
                if ext in ['.jpg', '.jpeg']:
                    content_type = 'image/jpeg'
                elif ext == '.png':
                    content_type = 'image/png'
                elif ext == '.pdf':
                    content_type = 'application/pdf'
                elif ext == '.doc' or ext == '.docx':
                    content_type = 'application/msword'
                elif ext == '.xls' or ext == '.xlsx':
                    content_type = 'application/vnd.ms-excel'
                else:
                    content_type = 'application/octet-stream'
            
            # Force binary mode and use FileResponse for proper handling
            response = FileResponse(
                open(file_path, 'rb'),
                content_type=content_type,
                as_attachment=True
            )
            
            # More explicit Content-Disposition header
            from urllib.parse import quote
            response['Content-Disposition'] = f'attachment; filename="{quote(file_name)}"'
            
            # Add additional headers that might help
            response['Access-Control-Expose-Headers'] = 'Content-Disposition'
            
            return response

        except AnnouncementFile.DoesNotExist:
            raise Http404("File not found.")
        except Exception as e:
            import traceback
            print(str(e), 'error')
            print(traceback.format_exc())  # More detailed error logging
            raise Http404("Error accessing file.")


class GreetingBannerOverviewViewSet(viewsets.ModelViewSet):
    permission_classes=[IsAuthenticated]
    authentication_classes=[ActiveUserJWTAuthentication]
    def get_queryset(self):
        today = date.today()

        # Ensure user has an associated id_card
        if hasattr(self.request.user, 'id_card'):
            user_departments = self.request.user.id_card.department.all()  # Get user's departments
            print(user_departments,"************")
        else:
            return Greeting_banner.objects.none()  # Return empty queryset if no id_card

        # Filter Greeting_banner by departments associated with the user
        return Greeting_banner.objects.filter(
            Expire_date__gte=today,
            department__in=user_departments
        ).order_by('-updated_at')

    serializer_class = GreetingBannerSerializer

class CustomTokenObtainPairViewSet(TokenObtainPairView):
    serializer_class = CustomTokenObtainPairSerializer


class ChangePasswordView(APIView):
    permission_classes = [IsAuthenticated]  # JWT Authentication

    def post(self, request):
        user = request.user

        # Ensure the user is of type "Team"
        if user.user_type != "Team":
            return Response({"status": 0, "message": "You are not authorized to change the password"}, status=status.HTTP_403_FORBIDDEN)

        # Extract fields from request
        current_password = request.data.get("current_password")
        new_password = request.data.get("new_password")
        confirm_password = request.data.get("confirm_password")

        # Check if fields are provided
        if not current_password or not new_password:
            return Response({"status": 0, "message": "Current password and new password are required"}, status=status.HTTP_400_BAD_REQUEST)
        # 🔒 Check if new_password and confirm_password match
        if new_password != confirm_password:
            return Response(
                {"status": 0, "message": "New password and confirm password do not match"},
                status=status.HTTP_400_BAD_REQUEST,
            )
        # Verify the current password
        if not check_password(current_password, user.password):
            return Response({"status": 0, "message": "Current password is incorrect"}, status=status.HTTP_400_BAD_REQUEST)
        
        # Validate new password security
        try:
            validate_password(new_password, user)
        except ValidationError as e:
            return Response({"status": 0, "message": "New password does not meet security requirements", "errors": list(e)}, status=status.HTTP_400_BAD_REQUEST)

        # Change password
        user.set_password(new_password)
        user.changed_pwd = True
        user.save()
        return Response({"status": 1, "message": "Password changed successfully!"}, status=status.HTTP_200_OK)


class LogoutAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            refresh_token = request.data.get("refresh")

            if not refresh_token:
                return Response({"status": 0, "message": "Refresh token is required"}, status=status.HTTP_400_BAD_REQUEST)

            # Blacklist the access token
            token = RefreshToken(refresh_token)
            token.blacklist()

            user = request.user
            id_card_instance = id_card.objects.filter(user=user).first()
            print(id_card_instance,"-----------------------idcardinstance")
            if id_card_instance:
                id_card_instance.fcm_token = ""
                id_card_instance.save()

            return Response({"status": 1, "message": "Logout successful"}, status=status.HTTP_200_OK)

        except TokenError:
            return Response({"status": 0, "message": "User is not currently logged in"}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print(e,'checkeeee')
            return Response({"status": 0, "message": "An error occurred during logout"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class SendNotificationCron(APIView):
    CRON_SECRET_KEY = settings.CRON_SECRET_KEY

    def get(self, request):
        token = request.GET.get("token")

        if not token:
            return Response({"error": "Token is required"}, status=400)

        if token != self.CRON_SECRET_KEY:
            return Response({"error": "Unauthorized"}, status=403)

        # Fetch the first *pending* notification
        notification = NotificationPool.objects.filter(status='pending').first()

        if not notification:
            return Response({"message": "No pending notifications to send."})

        try:
            data = notification.data
            fcm_token = str(data.get("fcm_token", "")).strip()

            if not fcm_token:
                notification.status = "failed"
                notification.save()
                return Response({"error": "FCM token missing for user"}, status=400)

            image_url = data.get("image", "")
            image_ = f"https://admin.tomahawk141.com/media/{image_url}"

            message = messaging.Message(
                notification=messaging.Notification(
                    title=data.get("title", "Notification"),
                    body=data.get("description", ""),
                    image=image_
                ),
                data={
                    "image": image_,
                },
                token=fcm_token,
            )

            response = messaging.send(message)
            print(f"Sent notification to {notification.team.name}: {response}")

            # Mark as success
            notification.status = "sent"
            notification.save()

            return Response({
                "message": "Notification sent successfully!",
                "images": image_url,
                "response": response
            })

        except FirebaseError as e:
            notification.status = "failed"
            notification.save()
            return Response({"error": "Firebase Error", "details": str(e)}, status=500)

        except Exception as e:
            notification.status = "failed"
            notification.save()
            return Response({"error": "Unexpected error", "details": str(e)}, status=500)
