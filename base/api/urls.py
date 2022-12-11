from django.urls import path
from . import views
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi
from django.urls import re_path
from rest_framework import routers

from rest_framework.authtoken.views import ObtainAuthToken



schema_view = get_schema_view(
    openapi.Info(
        title="StudyBud API",
        default_version='v1',
        description="This is the API for StudyBud, a study room discussion forum application",
    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)


urlpatterns = [
    path('user', view=views.UserViewSet.as_view({'get': 'get_user'})),
    path('rooms/', views.RoomViewSet.as_view({'get': 'list'})),
    path('rooms/<str:pk>/messages/', views.RoomMessagesViewSet.as_view({'get': 'list', 'post': 'create'})),
    path('token/', ObtainAuthToken.as_view()),
    re_path(r'^swagger(?P<format>\.json|\.yaml)$',
            schema_view.without_ui(cache_timeout=0), name='schema-json'),
    re_path(r'^swagger/$', schema_view.with_ui('swagger',
            cache_timeout=0), name='schema-swagger-ui'),
    re_path(r'^redoc/$', schema_view.with_ui('redoc',
            cache_timeout=0), name='schema-redoc'),
]
