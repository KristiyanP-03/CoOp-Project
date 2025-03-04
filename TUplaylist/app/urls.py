from django.urls import path, include

from app.views import *

urlpatterns = [

    path('admin_debug/', debug_page, name="debug_page")
]