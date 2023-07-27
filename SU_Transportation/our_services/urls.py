from django.urls import path

from SU_Transportation.our_services.views import ServicesView

urlpatterns = [
    path('', ServicesView.as_view(), name='services details')
]