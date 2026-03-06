# from rest_framework.authentication import BasicAuthentication
# from rest_framework.exceptions import PermissionDenied

# class CustomAuthentication(BasicAuthentication):
#     def authenticate(self, request):
#         user_auth_tuple = super().authenticate(request)

#         if user_auth_tuple is None:
#             return None

#         user, auth = user_auth_tuple

#         if not user.is_active:
#             raise PermissionDenied({
#                 "status": -1,
#                 "message": "Your account is inactive. Please contact support."
#             })

#         return (user, auth)


# myapp/authentication.py
# norpro_app/authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed

class ActiveUserJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        result = super().authenticate(request)
        if result is None:
            return None

        user, validated_token = result

        if user.status=="Inactive":
            raise AuthenticationFailed('User account is inactive.')

        return user, validated_token

