from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth.models import User
from rest_framework_simplejwt.tokens import RefreshToken
from drf_spectacular.utils import extend_schema, OpenApiExample
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
from decouple import config

# Genera el par de tokens JWT (access y refresh) para un usuario ya
# verificado. SimpleJWT se encarga de firmarlos.
def get_tokens_for_user(user):
    """Genera par de tokens JWT para el usuario dado."""
    refresh = RefreshToken.for_user(user)
    return {
        'refresh': str(refresh),
        'access': str(refresh.access_token),
    }


# Endpoint principal de autenticacion. El flujo es:
# 1. Recibe el id_token que Google genera cuando el usuario inicia sesion
# 2. Verifica que el token sea valido usando la libreria google-auth
# 3. Extrae el email, nombre y apellido del token verificado
# 4. Busca el usuario en la base de datos, si no existe lo crea
# 5. Genera y devuelve un par de tokens JWT (access y refresh)
# El endpoint es publico (AllowAny) porque es la puerta de entrada,
# aun no hay JWT con que autenticarse
@extend_schema(
    summary="Autenticación con Google",
    description=(
        "Recibe un token de Google (id_token) obtenido desde el cliente con Google Sign-In. "
        "Verifica el token, crea o recupera el usuario, y devuelve un par de tokens JWT."
    ),
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'token': {'type': 'string', 'description': 'id_token de Google'}
            },
            'required': ['token'],
        }
    },
    responses={
        200: {
            'type': 'object',
            'properties': {
                'access': {'type': 'string'},
                'refresh': {'type': 'string'},
                'email': {'type': 'string'},
                'nombre': {'type': 'string'},
            }
        }
    },
    examples=[
        OpenApiExample(
            'Ejemplo de request',
            value={'token': 'eyJhbGciOiJSUzI1NiIsImtpZCI6...'},
            request_only=True,
        )
    ],
    tags=['Autenticación'],
)
@api_view(['POST'])
@permission_classes([AllowAny])



#POST /auth/google
#Verifica el id_token de Google y retorna tokens JWT.
def google_login(request):
    
    token = request.data.get('token')
    if not token:
        return Response(
            {'error': 'El campo token es requerido.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    try:
        id_info = id_token.verify_oauth2_token(
            token,
            google_requests.Request(),
            config('GOOGLE_CLIENT_ID'),
        )
    except ValueError as e:
        return Response(
            {'error': 'Token de Google inválido.', 'detalle': str(e)},
            status=status.HTTP_401_UNAUTHORIZED
        )

    email = id_info.get('email')
    nombre = id_info.get('given_name', '')
    apellido = id_info.get('family_name', '')

    if not email:
        return Response(
            {'error': 'No se pudo obtener el email del token de Google.'},
            status=status.HTTP_400_BAD_REQUEST
        )

    user, created = User.objects.get_or_create(
        username=email,
        defaults={
            'email': email,
            'first_name': nombre,
            'last_name': apellido,
        }
    )

    tokens = get_tokens_for_user(user)

    return Response({
        **tokens,
        'email': email,
        'nombre': f'{nombre} {apellido}'.strip(),
        'nuevo_usuario': created,
    }, status=status.HTTP_200_OK)
