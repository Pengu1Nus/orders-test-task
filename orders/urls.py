"""
URL для заказов.
"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter

from orders import views

router = DefaultRouter()
router.register(r'orders', views.OrderViewSet)
app_name = 'order'

urlpatterns = [
    path('', include(router.urls)),
]
