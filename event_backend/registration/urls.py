from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views

router = DefaultRouter()
router.register(r'visitors', views.VisitorViewSet)
router.register(r'waves', views.EventWaveViewSet)
router.register(r'blacklist', views.BlackListView, basename='blacklist')

urlpatterns = [
    path('', include(router.urls)),
]
