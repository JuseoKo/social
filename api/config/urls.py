from django.contrib import admin
from django.urls import path, include
from drf_yasg import openapi
from drf_yasg.views import get_schema_view
from config.url_router import UrlRouter

router = UrlRouter()

schema_view = get_schema_view(
    openapi.Info(
        title="Social API",
        default_version="v1",
        description="Socail 결제 플렛폼 API 입니다.",
    ),
    public=True,
)
# # 토큰 인증 해더
# token_param = openapi.Parameter(
#     "Authorization",
#     openapi.IN_HEADER,
#     description="Bearer Token",
#     type=openapi.TYPE_STRING,
# )
from user.views import UserTokenObtainPairSerializer
from rest_framework_simplejwt.views import (
    TokenObtainPairView,
    TokenRefreshView,
)
urlpatterns = [
    path("", include(router.urls)),
    path('token/',  TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path(
        "api/",
        schema_view.with_ui("swagger", cache_timeout=0),
        name="schema-swagger-ui",
    ),
    path("admin/", admin.site.urls),
]
