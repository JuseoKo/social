from rest_framework import routers
from user import views


def UrlRouter():
    router = routers.DefaultRouter()
    # user 모델
    router.register(r"users", views.UserViewSet)
    return router
