"""
URL configuration for netpanel project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path
from devices import views

urlpatterns = [
    path("admin/", admin.site.urls),
    path('',views.home,name="home"),
    path('add/',views.add_devices,name="add_devices"),
    path('online_devices/',views.online_devices,name="online_devices"),
    path('delete/<int:id>/',views.delete,name="delete"),
    path('edit_device/<int:id>',views.edit_device,name="edit_device"),
    path('api/devices/',views.device_list_api,name="device_list_api"),
    path('api/device/<int:id>/',views.device_detail_api,name="device_detail"),
    path('api/device/add/',views.add_device_api,name="add_device_api"),
]
