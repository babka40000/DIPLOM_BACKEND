from django.http import HttpResponse, JsonResponse
from django.utils.decorators import method_decorator
from django.contrib.auth import authenticate, login, logout, get_user_model
from django.contrib.auth.models import User
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework.viewsets import ModelViewSet
from app.models import FilesAndFolders
from app.serializers import FilesAndFoldersSerializer, UserSerializer, AdminOperationsSerializer
from django.contrib.auth.decorators import login_required
import json
from rest_framework.parsers import MultiPartParser, FormParser, JSONParser


def home_view(request):
    return HttpResponse('PRIVETULI!!!')


@api_view(['GET'])
@permission_classes((AllowAny,))
def auth_getcurrenuser_view(request):
    if (request.user is None) | (request.user.id is None):
        return JsonResponse({
            "errors": {
                "detail": "You are not login"
            }
        }, status=400)
    else:
        return JsonResponse(
            {"name": request.user.first_name,
             "admin": request.user.is_superuser | request.user.is_staff,
             "id": request.user.id})


@api_view(['POST'])
@permission_classes((AllowAny,))
def auth_login_view(request):
    data = json.loads(request.body)
    username = data.get('username')
    password = data.get('password')
    if username is None:
        return JsonResponse({
            "errors": {
                "detail": "Please enter username"
            }
        }, status=400)
    elif password is None:
        return JsonResponse({
            "errors": {
                "detail": "Please enter password"
            }
        }, status=400)

    # authentication user
    user = authenticate(username=username, password=password)
    if user is not None:
        login(request, user)
        return JsonResponse({"result": "success", "name": user.first_name, "admin": user.is_superuser | user.is_staff})
    return JsonResponse(
        {"errors": "Invalid credentials"},
        status=400,
    )


@api_view(['GET'])
@permission_classes((AllowAny,))
def auth_logout_view(request):
    logout(request)
    return JsonResponse({"result": "success"})


@api_view(['POST'])
@permission_classes((AllowAny,))
def auth_register_view(request):
    serializer = UserSerializer(data=request.data)
    if serializer.is_valid():
        user = serializer.save()
        if user:
            return JsonResponse(serializer.data, status=201)
    else:
        return JsonResponse(serializer.errors, status=400)


class FilesAndFoldersViewSet(ModelViewSet):
    queryset = FilesAndFolders.objects.all()
    serializer_class = FilesAndFoldersSerializer
    parser_classes = (MultiPartParser, FormParser, JSONParser)

    def get_queryset(self):
        queryset = self.queryset

        if 'link' in self.request.query_params:
            query_set = queryset.filter(link=self.request.query_params['link'])
            return query_set

        if 'usr' in self.request.query_params and (self.request.user.is_staff or self.request.user.is_superuser):
            my_user = self.request.query_params['usr']
        else:
            my_user = self.request.user

        if 'parent' in self.request.query_params:
            query_set = queryset.filter(user=my_user, parent=self.request.query_params['parent'])
        else:
            query_set = queryset.filter(user=my_user, parent=None)

        return query_set

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super().dispatch(*args, **kwargs)


class AdminOperationsViewSet(ModelViewSet):
    queryset = User.objects.all()
    serializer_class = AdminOperationsSerializer
