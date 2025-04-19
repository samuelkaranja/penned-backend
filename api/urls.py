from django.urls import path, include
from rest_framework.routers import DefaultRouter
from .views import BlogViewSet, SignupAPIView, LoginView

router = DefaultRouter()
router.register(r'blogs', BlogViewSet)

urlpatterns = [
    path('', include(router.urls)),
    path('signup/', SignupAPIView.as_view(), name='signup'),
    path('login/', LoginView.as_view(), name='login'),
]
