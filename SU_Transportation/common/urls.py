from django.contrib.auth.decorators import login_required
from django.urls import path, include

from SU_Transportation.common import views
from SU_Transportation.common.views import IndexView, ContactUsView, MessageView, ReadView, DeleteMessageView

urlpatterns = [
    path('', IndexView.as_view(), name='home page'),
    path('drive-for-us/', views.driver_application_view, name='driver apply'),
    path('contact-us/', ContactUsView.as_view(), name='contact us'),
    path('messages/', include([
        path('', login_required(MessageView.as_view()), name='messages'),
        path('<int:pk>/read/', login_required(ReadView.as_view()), name='message read'),
        path('<int:pk>/delete/', login_required(DeleteMessageView.as_view()), name='message delete')
    ])),
]

