from .serializers import UserSerializer


def jwt_response_payload_handler(token, user=None, request=None):
    user = UserSerializer(user, context={'request': request}).data
    return {
        'token': token,
        'id': user['id'],
        'email': user['email'],
        'username': user['username'],
        'first_name': user['first_name'],
        'last_name': user['last_name'],
        'is_staff': user['is_staff'],
        'is_active': user['is_active'],
    }
